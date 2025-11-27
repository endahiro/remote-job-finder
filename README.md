# RemoteJob Finder 🌍💻

RemoteJob Finder is a small web app that helps users discover **real remote jobs** from the web using the public [RemoteOK](https://remoteok.com/) API.

The app focuses on:
- A **practical purpose** – finding real remote work opportunities.
- **API integration** – consuming and displaying live data from an external API.
- **Meaningful interaction** – search, filtering, and sorting of job data.
- **Deployment** – running on two web servers behind a load balancer.

---

## Demo 🎥

Short demo video (max 2 minutes):

👉 **Demo video:** `ADD_LINK_HERE`

The video shows:
- Running the app **locally**
- Accessing the app via the **load balancer IP** (e.g. `http://98.93.207.196/`)
- Basic search, filter, and sort interactions

---

## Features ✨

- Fetches live remote jobs from the **RemoteOK API**
- Displays a curated set of jobs on the home page (recent, meaningful results)
- Users can:
  - 🔍 **Search** by keyword (e.g. “Python”, “designer”, “marketing”)
  - 🏷 **Filter by category** (e.g. dev / design / marketing / other)
  - 📅 **Sort by date** (e.g. newest first)
- Each job links out to the **original RemoteOK posting** in a new tab
- Simple, responsive UI with:
  - Hero header
  - LIVE status badge
  - Clean job cards
  - Empty state messaging when nothing matches

---

## Tech Stack 🧱

**Backend:**
- Python
- Flask
- Requests (for HTTP calls to the RemoteOK API)

**Frontend:**
- HTML (Jinja templates)
- CSS (custom styling)

**Deployment:**
- Ubuntu 20.04 servers:
  - `web-01` and `web-02` running:
    - Flask app via Gunicorn (`remote-finder` systemd service)
    - Nginx as a reverse proxy
  - `lb-01` running HAProxy as the load balancer
- Load balancer distributes traffic between `web-01` and `web-02`

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
