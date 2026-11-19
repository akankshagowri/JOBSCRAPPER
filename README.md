# Fake Jobs Scraper

A small Python web scraper that collects job postings from the [Real Python Fake Jobs](https://realpython.github.io/fake-jobs/) practice site and saves them to a CSV file.

**Project URL:** https://github.com/akankshagowri/JOBSCRAPPER

## Features

- Extracts four fields for every job posting:
  - Job title
  - Company name
  - Location
  - Job detail page URL
- Writes the results to a clean, UTF-8 encoded CSV file
- Handles simple edge cases:
  - Missing fields are saved as empty strings instead of crashing the run
  - Completely empty cards are skipped
  - Relative links are converted to absolute URLs
  - Network and HTTP errors are reported with a clear message
  - A warning is shown if no jobs are found (for example, if the page layout changes)

## Requirements

- Python 3.9 or newer
- [requests](https://pypi.org/project/requests/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

## Installation

```bash
git clone https://github.com/akankshagowri/JOBSCRAPPER.git
cd JOBSCRAPPER
pip install requests beautifulsoup4
```

## Usage

```bash
python jobscrapper.py
```

On success you will see a message like:

```
Saved 100 jobs to jobs.csv
```

The CSV file is created in the folder you run the command from. To save it somewhere else, change `OUTPUT_FILE` at the top of the script to a full path, for example:

```python
OUTPUT_FILE = r"C:\Users\<you>\Downloads\jobs.csv"
```

## Output format

`jobs.csv` has one row per job and the following columns:

| Column      | Description                          |
|-------------|--------------------------------------|
| `job_title` | Title of the position                |
| `company`   | Name of the hiring company           |
| `location`  | City and state code                  |
| `job_url`   | Link to the job's detail page        |

Example rows:

```csv
job_title,company,location,job_url
Senior Python Developer,"Payne, Roberts and Davis","Stewartbury, AA",https://realpython.github.io/fake-jobs/jobs/senior-python-developer-0.html
Energy engineer,Vasquez-Davidson,"Christopherville, AA",https://realpython.github.io/fake-jobs/jobs/energy-engineer-1.html
```

## How it works

1. Downloads the page HTML with `requests`.
2. Parses it with `BeautifulSoup` and loops over each job card.
3. Reads the title, company and location from each card. The job URL is taken from the card's "Apply" link, since the "Learn" link is the same generic page on every card.
4. Saves all rows to CSV with Python's built-in `csv` module.

## Project structure

```
.
├── jobscrapper.py   # the scraper
├── jobs.csv         # generated output
└── README.md
```

## Notes

The target site is a static page built for scraping practice, so there is no login, pagination or JavaScript rendering to deal with. Please be considerate when adapting this script to real websites: check their terms of service and `robots.txt`, and avoid sending requests too quickly.

## License

This project is released under the MIT License. Feel free to use and modify it.
