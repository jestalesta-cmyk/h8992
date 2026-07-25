import re
import requests

def download_file_from_google_drive(url, destination):
    # Extract the file ID from the URL
    file_id_match = re.search(r'/file/d/([^/]+)', url)
    if not file_id_match:
        # Check if it's of format id=...
        file_id_match = re.search(r'id=([^&]+)', url)
    if not file_id_match:
        print("Could not find file ID in URL.")
        return False
    
    file_id = file_id_match.group(1)
    print(f"File ID found: {file_id}")
    
    DOWNLOAD_URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(DOWNLOAD_URL, params={'id': file_id}, stream=True)
    
    token = get_confirm_token(response)
    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(DOWNLOAD_URL, params=params, stream=True)
        
    save_response_content(response, destination)
    return True

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

url = "https://drive.google.com/file/d/1obNjskJTSt3RpV1kgsycN4Kf9pGIiYDX/view?usp=sharing"
download_file_from_google_drive(url, "downloaded_file")
