# ⚡ FiveM CFX Finder & IP Resolver

විශ්වසනීය, නවීන හා ද්විභාෂා (English & Sinhala) වෙබ් යෙදුමකි. මෙය ඕනෑම **FiveM CFX Join Code** එකක් (උදා: `cfx.re/join/y4lg95`) භාවිතයෙන්, එම සේවාදායකයේ (server) සෘජු IP ලිපිනය සහ කෙවෙනිය (port), සජීවී සේවාදායක තොරතුරු, resource ලැයිස්තුව, සැකසුම් (config convars) හා සක්‍රිය ක්‍රීඩක තොරතුරු ක්ෂණිකව සොයාගැනීමට උපකාරී වේ.

---

## 🇱🇰 සිංහලෙන් (Sinhala)

මෙය FiveM සේවාදායක (servers) පිළිබඳ තොරතුරු සහ ඒවායේ සෘජු IP ලිපින ක්ෂණිකව සොයාගත හැකි අති නවීන වෙබ් මෙවලමකි. ඔබ ඇතුළත් කරන ඕනෑම FiveM join link එකක් හෝ අකුරු/ඉලක්කම් වලින් යුත් code එකක් මඟින්:

* සේවාදායකයේ සැබෑ සෘජු IP ලිපිනය සහ port එක සොයාගැනීම.
* සක්‍රියව ක්‍රීඩා කරන ක්‍රීඩකයින්ගේ සවිස්තරාත්මක ලැයිස්තුව (ID, Name, Ping, Discord සහ Steam identifiers).
* සේවාදායකය තුළ ධාවනය වන scripts / resources ලැයිස්තුව බැලීම සහ පිටපත් කරගැනීම.
* Game build, Locale, Server software (artifacts) වැනි සියලු සැකසුම් (config) තොරතුරු බැලීම.

---

## ✨ විශේෂාංග (Features)

1. **ද්විත්ව විභේදන තාක්ෂණය (Dual-Layered Resolution)**
   * **ප්‍රථම පියවර:** Cfx.re join link backend එකට සුදුසු headers භාවිතයෙන් සම්බන්ධ වී, සේවාදායක නම, ක්‍රීඩක ගණන සහ ලාංඡන රූපය විශ්ලේෂණය කිරීම.
   * **දෙවන පියවර:** විභේදනය කළ IP එක ඔස්සේ සේවාදායකයේ දේශීය endpoints (`info.json`, `players.json`, `dynamic.json`) වලින් සම්පූර්ණ, අඩු ප්‍රමාදයේ දත්ත ලබාගැනීම!
2. **ලස්සන ද්විභාෂා මුහුණත (Bilingual UI)**
   * එක ක්ලික් එකකින් **English** සහ **Sinhala (සිංහල)** අතර ක්ෂණිකව මාරු වීමට ඉඩ සලසයි.
3. **FiveM වර්ණ කේත විශ්ලේෂණය (Caret Color Parsing)**
   * FiveM caret වර්ණ සංකේත (`^1`, `^2`, `^3` ...) ස්වයංක්‍රීයව විශ්ලේෂණය කර, GTA client එකේ මෙන් බබළන වර්ණයෙන් යුත් HTML spans වලින් පෙන්වයි.
4. **මෑතකදී සෙවූ දේ සහ ඉතිහාසය (Recent Searches & History)**
   * අදාළ බ්‍රව්සරයේ localStorage තුළ මෑතකදී විශ්ලේෂණය කළ සේවාදායක සුරකිමින්, පසුව එක ක්ලික් එකකින් පිවිසීමට ඉඩ සලසයි.
5. **අන්තර්ක්‍රියාත්මක ටැබ් (Interactive Tabs)**
   * **Players List:** නම හෝ ID මඟින් සක්‍රිය ක්‍රීඩක පොරේතු කිරීම.
   * **Resources Grid:** සියලු scripts බැලීම, ඒවා පොරේතු කිරීම සහ ලැයිස්තුව පිටපත් කිරීම.
   * **Server Config (Convars):** OneSync, game build වැනි තාක්ෂණික විස්තර.
   * **Raw JSON:** සම්පූර්ණ අමු JSON දත්ත යාගත කිරීම සඳහා (developer diagnostics).

---

## 📁 ගොනු ව්‍යුහය (Project Structure)

```text
├── app.py                  # Flask backend (Python)
├── templates/
│   └── index.html          # Tailwind CSS භාවිතයෙන් සකස් කළ dark-themed responsive UI
├── static/
│   ├── logo.png            # 3D-style logo icon
│   └── tailwind.min.css    # දේශීයව compiled කළ Tailwind CSS
├── requirements.txt        # අවශ්‍ය Python packages
├── run.sh                  # එක ක්ලික් එකකින් යෙදුම ආරම්භ කිරීමට විධානය
└── README.md               # ඔබ දැන් කියවන්නේ මෙයයි
```

---

## 🚀 භාවිතා කරන ආකාරය (How to Run)

පහත පියවර අනුගමනය කරමින් ඔබේ පරිගණකයේ (local environment) යෙදුම ධාවනය කරන්න:

### 1. Run විධානය මඟින් (එක ක්ලික් එකකින්)
ටර්මිනලයේ පහත විධානය ක්‍රියාත්මක කරන්න:
```bash
./run.sh
```

### 2. අතින් ආරම්භ කිරීම (Manual Start)
ඔබට අතින් ආරම්භ කිරීමට කැමති නම්:
```bash
# අවශ්‍ය packages පිහිටුවීම
pip install -r requirements.txt

# Flask app එක ආරම්භ කිරීම
python3 app.py
```

### 3. බ්‍රව්සරයෙන් පිවිසීම
ආරම්භ කිරීමෙන් පසු, ඔබේ බ්‍රව්සරය ඔස්සේ පහත URL එකට පිවිසෙන්න:
**[http://localhost:5000](http://localhost:5000)**

---

## 🛠️ භාවිතා කළ තාක්ෂණවේදය (Tech Stack)

* **Backend:** Python 3, Flask, Requests, BeautifulSoup4
* **Frontend:** HTML5, CSS3, Tailwind CSS, FontAwesome Icons, Google Fonts (Ubuntu & Fira Code)
* **Database/Cache:** Browser `localStorage` (ඉතිහාසය සුරැකීම සඳහා)

---

## 🌐 Hosting / Deployment

The app is a Flask server. It queries `cfx.re` and `frontend.cfx-services.net` to
resolve servers, so the host **must allow outbound internet access**.

> ⚠️ **Note:** PythonAnywhere's **free (Beginner) plan blocks outbound HTTP** to
> non-whitelisted sites — the resolver will fail there. Use a **paid plan** (Hacker,
> ~$5/mo) **or deploy on Render / Railway** (free tiers allow outbound requests).

The project is deployment-ready: `app.py` reads the port from the `PORT` env var
(defaults to 5000) and runs without debug; `Procfile` and `requirements.txt`
(incl. `gunicorn`) are included.

### PythonAnywhere (paid plan)
1. Push the repo to GitHub (or upload via the Files tab).
2. Web → Add a new web app → Manual configuration → Python 3.11.
3. Bash console: `mkvirtualenv --python=python3.11 myenv` then `pip install -r ~/mysite/requirements.txt`.
4. Replace the WSGI file with:
   ```python
   import sys
   path = '/home/<user>/mysite'
   if path not in sys.path:
       sys.path.append(path)
   from app import app as application
   ```
5. Map static files: URL `/static/` → `/home/<user>/mysite/static`. Reload.

### Render (free, outbound works)
1. Push to GitHub.
2. New → Web Service → connect repo.
3. Build: `pip install -r requirements.txt` · Start: `gunicorn app:app --bind 0.0.0.0:$PORT`.
4. Deploy → free `*.onrender.com` URL.

Full details in **`DEPLOY.md`**.

---

## 🖥️ Live Instance (Hosting Details)

> Fill these in **after** you deploy the app. For a hosted website these values
> are public anyway (that's how visitors reach it), but avoid pasting SSH keys
> or private credentials here.

| Detail | Value |
| --- | --- |
| Public IP | `<your-server-ip>` |
| VPS / Provider | `<e.g. Contabo / DigitalOcean / Hetzner / Render>` |
| Hostname / Domain | `<your-domain-or-hostname>` |
| Access URL | `https://<domain>` |

* Render / Railway: the hostname is the auto-assigned `*.onrender.com` / `*.up.railway.app` URL.
* Own VPS: use the provider-assigned IP and the hostname/domain you point at it.
