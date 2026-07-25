# Deploy — FiveM CFX Finder & IP Resolver

This app is a Flask server. It queries `cfx.re` and `frontend.cfx-services.net`
to resolve FiveM servers, so it **requires outbound internet access** from the host.

> ⚠️ **Important (Sinhala):** PythonAnywhere FREE (Beginner) plan blocks outbound
> HTTP to non-whitelisted sites — the resolver will fail with network errors.
> Use a **paid plan** (Hacker, ~$5/mo) OR deploy on **Render / Railway** (free tiers
> allow outbound requests and work without this restriction).

---

## Option A — PythonAnywhere (paid plan recommended)

1. **Push code to GitHub** (or upload via the Files tab):
   `app.py`, `templates/`, `static/`, `requirements.txt`, `Procfile`.
   Or in a PA Bash console: `git clone <repo-url> ~/mysite`

2. **Create the web app**
   Dashboard → **Web** → **Add a new web app** → **Manual configuration** →
   choose Python 3.11.

3. **Install dependencies** (Bash console):
   ```bash
   mkvirtualenv --python=python3.11 myenv
   pip install -r ~/mysite/requirements.txt
   ```

4. **Configure WSGI** — replace the WSGI file contents
   (`/var/www/<user>_pythonanywhere_com_wsgi.py`):
   ```python
   import sys
   path = '/home/<user>/mysite'
   if path not in sys.path:
       sys.path.append(path)
   from app import app as application
   ```
   Replace `<user>` with your PythonAnywhere username.

5. **Map static files** (Web → Static files):
   - URL: `/static/` → Directory: `/home/<user>/mysite/static`

6. **Reload** (Web → Reload) and open `https://<user>.pythonanywhere.com`.

---

## Option B — Render (free, outbound works)

1. Push the repo to GitHub (already includes `Procfile` + `requirements.txt`).
2. render.com → **New → Web Service** → connect the repo.
3. Build command: `pip install -r requirements.txt`
   Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
4. Deploy → you get a free `*.onrender.com` URL.

---

## How the app binds

`app.py` reads the port from the `PORT` environment variable (defaults to 5000)
and runs without debug in production:

```python
port = int(os.environ.get('PORT', 5000))
debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
app.run(host='0.0.0.0', port=port, debug=debug)
```

Local run:
```bash
pip install -r requirements.txt
python3 app.py        # http://localhost:5000
```
