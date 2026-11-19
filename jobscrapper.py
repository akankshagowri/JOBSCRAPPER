"""Scrape job postings from https://realpython.github.io/fake-jobs/ into a CSV file."""

import csv
import sys
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://realpython.github.io/fake-jobs/"
OUTPUT_FILE = "jobs.csv"
FIELDS = ["job_title", "company", "location", "job_url"]


def fetch_html(url: str) -> str:
    """Download a page and return its HTML, raising on HTTP errors."""
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.text


def get_text(parent, selector: str) -> str:
    """Return the stripped text of the first element matching `selector`, or ''."""
    element = parent.select_one(selector)
    return element.get_text(strip=True) if element else ""


def get_detail_url(card) -> str:
    """Return the absolute URL of the job's detail page, or '' if missing.

    Each card has two footer links: "Learn" (a generic Real Python page)
    and "Apply" (the job's own detail page). We want the latter.
    """
    for link in card.select("footer a[href]"):
        if link.get_text(strip=True).lower() == "apply":
            return urljoin(BASE_URL, link["href"])
    return ""


def parse_jobs(html: str) -> list[dict]:
    """Extract all job postings from the page HTML."""
    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    for card in soup.select("div.card-content"):
        job = {
            "job_title": get_text(card, "h2.title"),
            "company": get_text(card, "h3.company"),
            "location": get_text(card, "p.location"),
            "job_url": get_detail_url(card),
        }
        # Skip cards that contain no usable data at all.
        if any(job.values()):
            jobs.append(job)

    return jobs


def save_to_csv(jobs: list[dict], path: str) -> None:
    """Write the job list to a CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(jobs)


def main() -> int:
    try:
        html = fetch_html(BASE_URL)
    except requests.RequestException as exc:
        print(f"Failed to fetch {BASE_URL}: {exc}", file=sys.stderr)
        return 1

    jobs = parse_jobs(html)
    if not jobs:
        print("No job postings found; the page structure may have changed.", file=sys.stderr)
        return 1

    save_to_csv(jobs, OUTPUT_FILE)

    missing = sum(1 for job in jobs if not all(job.values()))
    print(f"Saved {len(jobs)} jobs to {OUTPUT_FILE} ({missing} with missing fields).")
    return 0


if __name__ == "__main__":
    sys.exit(main())