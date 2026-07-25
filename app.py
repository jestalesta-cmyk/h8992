import os
import re
import json
import logging
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Standard high-reputation headers to bypass potential blocks
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

def clean_fivem_colors(text):
    if not text:
        return ""
    return re.sub(r'\^[0-9;r]', '', text)

def extract_cfx_code(input_str):
    """
    Extracts the CFX code from a string or link, PRESERVING CASE.
    CFX codes are case-sensitive! (e.g., cfx.re/join/vjarme is distinct from VJARME).
    """
    input_str = input_str.strip()
    
    # Extract code from cfx.re/join/XXXXXX link (supports standard 6-char or custom vanity names)
    match = re.search(r'(?:join\/|cfx\.re\/join\/)?([a-zA-Z0-9_-]+)', input_str)
    if match:
        extracted = match.group(1)
        # Avoid matching URL query parameters if they exist
        if '?' in extracted:
            extracted = extracted.split('?')[0]
        return extracted
    
    return input_str if input_str else None

@app.route('/')
@app.route('/index.html')
def home():
    return render_template('home.html')

@app.route('/resolver')
@app.route('/resolver.html')
def resolver():
    return render_template('index.html')

@app.route('/console')
@app.route('/scanner')
@app.route('/scanner.html')
@app.route('/h89-dev')
def console():
    return render_template('console.html')

@app.route('/api/resolve', methods=['POST'])
def resolve_server():
    data = request.json or {}
    input_str = data.get('code', '')
    
    code = extract_cfx_code(input_str)
    if not code:
        return jsonify({
            'success': False,
            'error': 'invalid_code',
            'message': 'වැරදි CFX Code එකක්. කරුණාකර අකුරු හෝ ඉලක්කම් 6ක code එකක් හෝ cfx.re link එකක් ඇතුලත් කරන්න.'
        }), 400
        
    logging.info(f"Resolving CFX code (Case-Preserved): {code}")
    
    # --- APPROACH A: Query Cfx.re Master Frontend API ---
    master_api_url = f"https://frontend.cfx-services.net/api/servers/single/{code}"
    
    try:
        master_res = requests.get(master_api_url, headers=HEADERS, timeout=5)
        if master_res.status_code == 200:
            master_data = master_res.json()
            inner_data = master_data.get('Data', {})
            
            # Extract endpoint (IP & Port) from connectEndPoints list inside 'Data' dict
            endpoints_list = inner_data.get('connectEndPoints', [])
            endpoint = endpoints_list[0] if endpoints_list else None
            
            # Construct Server Icon URL
            icon_version = inner_data.get('iconVersion')
            icon_url = f"https://frontend.cfx-services.net/api/servers/icon/{code}/{icon_version}.png" if icon_version else None
            
            # Format server details
            server_data = {
                'code': code,
                'join_url': f"https://cfx.re/join/{code}",
                'endpoint': endpoint,
                'clean_endpoint': endpoint,
                'join_token': code,
                'online': True,
                'source': 'cfx_master_api',
                'html_fallback': {
                    'title': inner_data.get('hostname', ''),
                    'players': f"people_outline {inner_data.get('clients', 0)}",
                    'icon_url': icon_url
                },
                'details': {
                    'resources': inner_data.get('resources', []),
                    'vars': inner_data.get('vars', {}),
                    'server': inner_data.get('server', 'FXServer'),
                    'icon': inner_data.get('icon') # base64 if available
                },
                'players_list': inner_data.get('players', []),
                'dynamic_info': {
                    'clients': inner_data.get('clients', 0),
                    'sv_maxclients': inner_data.get('sv_maxclients', 32),
                    'gametype': inner_data.get('gametype', 'Roleplay'),
                    'mapname': inner_data.get('mapname', 'San Andreas')
                },
                'owner': {
                    'name': inner_data.get('ownerName'),
                    'profile': inner_data.get('ownerProfile'),
                    'avatar': inner_data.get('ownerAvatar')
                },
                'upvote_power': inner_data.get('upvotePower', 0),
                'last_seen': inner_data.get('lastSeen')
            }
            
            return jsonify({
                'success': True,
                'data': server_data
            })
            
    except Exception as e:
        logging.warning(f"Approach A (Master API) failed: {e}. Falling back to Approach B...")

    # --- APPROACH B: Fallback Scraper and Direct IP Query ---
    # Used as a backup for brand-new, unlisted, or private servers
    join_url = f"https://cfx.re/join/{code}"
    try:
        response = requests.get(join_url, headers=HEADERS, timeout=5)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'cfx_request_failed',
            'message': f'CFX.re වෙත සම්බන්ධ වීමට නොහැකි විය: {str(e)}'
        }), 500

    if response.status_code == 404:
        return jsonify({
            'success': False,
            'error': 'not_found',
            'message': f'මෙම CFX Code ({code}) එක සොයාගත නොහැකි විය. සේවාදායකය (Server) අක්‍රිය (Offline) හෝ වැරදි code එකක් විය හැක.'
        }), 404
        
    if response.status_code != 200:
        return jsonify({
            'success': False,
            'error': f'cfx_http_error_{response.status_code}',
            'message': f'CFX.re සේවාදායකය වැරදි ප්‍රතිචාරයක් ලබා දුන්නේය: HTTP {response.status_code}'
        }), response.status_code

    join_token = response.headers.get('x-citizenfx-join-token')
    endpoint_url = response.headers.get('x-citizenfx-url')
    
    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    html_title = ""
    title_tag = soup.find('title')
    if title_tag:
        html_title = title_tag.text.strip()
        if html_title.endswith(' / Cfx.re'):
            html_title = html_title[:-9]
            
    html_players = ""
    players_span = soup.find('span', class_='players')
    if players_span:
        html_players = players_span.text.strip()
        
    html_icon = ""
    img_tag = soup.find('img')
    if img_tag and img_tag.get('src'):
        html_icon = img_tag.get('src')
        
    server_data = {
        'code': code,
        'join_url': join_url,
        'endpoint': endpoint_url,
        'join_token': join_token,
        'online': True,
        'html_fallback': {
            'title': html_title,
            'players': html_players,
            'icon_url': html_icon
        },
        'source': 'cfx_metadata',
        'details': None,
        'players_list': None,
        'dynamic_info': None,
        'owner': None
    }
    
    if endpoint_url:
        if not endpoint_url.endswith('/'):
            endpoint_url += '/'
            
        server_data['clean_endpoint'] = endpoint_url
        info_json_url = f"{endpoint_url}info.json"
        players_json_url = f"{endpoint_url}players.json"
        dynamic_json_url = f"{endpoint_url}dynamic.json"
        
        try:
            info_res = requests.get(info_json_url, headers=HEADERS, timeout=2.5)
            if info_res.status_code == 200:
                server_data['details'] = info_res.json()
                server_data['source'] = 'local_api'
        except Exception:
            pass
            
        try:
            players_res = requests.get(players_json_url, headers=HEADERS, timeout=2.5)
            if players_res.status_code == 200:
                server_data['players_list'] = players_res.json()
        except Exception:
            pass
            
        try:
            dynamic_res = requests.get(dynamic_json_url, headers=HEADERS, timeout=2.5)
            if dynamic_res.status_code == 200:
                server_data['dynamic_info'] = dynamic_res.json()
        except Exception:
            pass
            
    return jsonify({
        'success': True,
        'data': server_data
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
