#!/usr/bin/env python3
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = "https://remoteok.com/api"


def fetch_jobs():
    """
    Fetch job data from the RemoteOK API.
    Returns a list of job dicts, sorted by newest first (epoch field).
    """
    try:
        response = requests.get(API_URL, headers={"User-Agent": "remote-finder"})
        response.raise_for_status()
        data = response.json()

        # RemoteOK returns a list where the first element is metadata
        if not isinstance(data, list) or len(data) <= 1:
            return []

        jobs = data[1:]  # skip metadata

        # Normalize some fields and prepare tags string
        for job in jobs:
            job.setdefault("company", "Unknown company")
            job.setdefault("position", "Unknown role")
            job.setdefault("location", "Worldwide")
            job.setdefault("url", "#")
            job.setdefault("tags", [])

            # Make a readable tags string
            if isinstance(job["tags"], list):
                job["tags_str"] = ", ".join(job["tags"])
            else:
                job["tags_str"] = str(job["tags"])

        # Sort by epoch (timestamp), newest first
        jobs_sorted = sorted(
            jobs,
            key=lambda j: j.get("epoch", 0),
            reverse=True,
        )
        return jobs_sorted

    except Exception as e:
        # For now just print; later you can log this properly
        print("Error fetching jobs from RemoteOK:", e)
        return []


@app.route("/", methods=["GET"])
def index():
    """
    Home page: shows a list of remote jobs.
    Supports simple keyword search filtering.
    """
    search = request.args.get("search", "").strip().lower()

    jobs = fetch_jobs()

    if search:
        filtered = []
        for job in jobs:
            # Build a text blob to search through
            text_parts = [
                job.get("position", ""),
                job.get("company", ""),
                job.get("location", ""),
                " ".join(job.get("tags", [])),
            ]
            searchable = " ".join(text_parts).lower()

            if search in searchable:
                filtered.append(job)

        jobs = filtered

    return render_template("index.html", jobs=jobs, search=search)


if __name__ == "__main__":
    # Local development only; in production we'll use Gunicorn
    app.run(debug=True)
