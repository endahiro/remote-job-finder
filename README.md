# RemoteJob Finder 🌍💻

RemoteJob Finder is a small web app that helps users discover **real remote jobs** from the web using the public [RemoteOK](https://remoteok.com/) API.

The app focuses on:
- A **practical purpose** – finding real remote work opportunities.
- **API integration** – consuming and displaying live data from an external API.
- **Meaningful interaction** – search, filtering, and sorting of job data.
- **Deployment** – running on two web servers behind a load balancer.

---

## Demo 🎥

Short demo video:

👉 **Demo video:** https://www.youtube.com/watch?v=LKvi1anG4qo

The video shows:
- Running the app **locally**
- Accessing the app via the **load balancer**
- Basic search, filter, and sort interactions

🌐 **Live App (Load Balancer):**  
http://100.26.206.96

---

## Features ✨

- Fetches live remote jobs from the **RemoteOK API**
- Displays a curated set of jobs on the home page (recent, meaningful results)
- Users can:
  - 🔍 **Search** by keyword (e.g. “Python”, “designer”, “marketing”)
  - 🏷 **Filter by category** (e.g. dev / design / marketing / other)
  - 📅 **Sort by date or salary**
- Each job links to the **original RemoteOK posting**
- Responsive UI with:
  - Hero section
  - LIVE status indicator
  - Clean job cards
  - Empty state messaging

---

## Tech Stack 🧱

**Backend:**
- Python
- Flask
- Requests

**Frontend:**
- HTML (Jinja templates)
- CSS

**Deployment:**
- Ubuntu 20.04 servers:
  - **web-01:** `32.192.227.92`
  - **web-02:** `3.87.14.177`
  - **lb-01:** `100.26.206.96`
- Gunicorn runs the Flask app
- Nginx acts as a reverse proxy
- HAProxy load balances traffic between both web servers

---

## Deployment Process 🚀

The application was deployed using the following steps:

1. The project was copied to both web servers (`web-01` and `web-02`) using `scp`.
2. A Python virtual environment was created on each server.
3. Dependencies were installed using `pip install -r requirements.txt`.
4. The application was served using **Gunicorn** on port `5000`.
5. A **systemd service** (`remote-finder`) was created to keep the app running.
6. **Nginx** was configured to:
   - Listen on port `80`
   - Proxy requests to Gunicorn (`127.0.0.1:5000`)
   - Serve static files from `/static/`
7. On the load balancer (`lb-01`):
   - **HAProxy** was configured in `roundrobin` mode
   - Traffic is distributed between:
     - `web-01:80`
     - `web-02:80`

---

## Repository Structure 📁

```text
remote-job-finder/
├── README.md
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── static/
│   ├── style.css          # Custom styles
│   └── script.js          # Optional front-end behavior
└── templates/
    └── index.html         # Main UI template