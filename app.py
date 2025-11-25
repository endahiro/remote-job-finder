#!/usr/bin/env python3
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

REMOTEOK_API = "https://remoteok.com/api"


def fetch_jobs():
    """Fetch jobs from RemoteOK API and normalize them."""
    try:
        resp = requests.get(
            REMOTEOK_API,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        # RemoteOK puts metadata in the first element, jobs after
        if isinstance(data, list) and len(data) > 1:
            raw_jobs = data[1:]
        else:
            raw_jobs = data

        jobs = []
        for item in raw_jobs:
            if not isinstance(item, dict):
                continue
            jobs.append(
                {
                    "id": item.get("id"),
                    "company": item.get("company") or "Unknown company",
                    "title": item.get("position") or item.get("title") or "Untitled role",
                    "location": item.get("location") or "Worldwide",
                    "tags": item.get("tags") or [],
                    "url": item.get("url") or "",
                    "date": item.get("date") or "",
                    "salary": item.get("salary") or "",
                }
            )
        return jobs
    except Exception as e:
        # You saw this printout earlier in your terminal
        print(f"Error fetching jobs from RemoteOK: {e}")
        return None


def salary_key(job):
    """Extract a numeric value from the salary string for sorting."""
    s = job.get("salary") or ""
    digits = "".join(ch for ch in s if (ch.isdigit() or ch == "."))
    try:
        return float(digits)
    except Exception:
        return 0.0


@app.route("/")
def index():
    query = request.args.get("search", "").strip()
    category = request.args.get("category", "").strip()
    sort = request.args.get("sort", "newest")

    jobs_raw = fetch_jobs()
    error_message = None

    if jobs_raw is None:
        # API unreachable → show a nice message instead of just an empty page
        jobs = []
        error_message = (
            "Could not reach RemoteOK right now. "
            "Please check your connection or try again in a moment."
        )
    else:
        # Filter
        q_lower = query.lower()
        cat_lower = category.lower()
        filtered = []

        for job in jobs_raw:
            text = f"{job['title']} {job['company']} {' '.join(job['tags'])}".lower()

            if q_lower and q_lower not in text:
                continue

            # We treat category as a simple keyword (e.g. 'dev', 'design', 'marketing')
            if cat_lower and cat_lower != "all":
                if cat_lower not in text:
                    continue

            filtered.append(job)

        # Sort
        if sort == "newest":
            # RemoteOK already returns newest first, but we keep this in case
            filtered.sort(key=lambda j: j.get("date", ""), reverse=True)
        elif sort == "oldest":
            filtered.sort(key=lambda j: j.get("date", "") or "")
        elif sort == "salary":
            filtered.sort(key=salary_key, reverse=True)

        # If no search and no specific category → show only the first 10 jobs on the homepage
        if not query and (not category or category == "all"):
            filtered = filtered[:10]

        jobs = filtered

    return render_template(
        "index.html",
        jobs=jobs,
        search=query,
        category=category,
        sort=sort,
        error_message=error_message,
    )


if __name__ == "__main__":
    app.run(debug=True)
