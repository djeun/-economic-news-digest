"""Daily briefing orchestrator.

Runs all 3 jobs in parallel (fetch + AI summarize), then sends all 3 emails
simultaneously once every job is ready.
"""
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(__file__))

import jobs.us_economic_news.main as us_econ
import jobs.tech_news.main as tech_news
import jobs.github_trending.main as github_trending


def _run(job_name: str, fetch_fn, process_fn) -> tuple:
    """Fetch data and generate AI summary for one job."""
    print(f"[{job_name}] Fetching data...")
    data = fetch_fn()
    if not data:
        raise RuntimeError("No data collected")
    print(f"[{job_name}] {len(data)} items collected. Generating AI summary...")
    summary_html = process_fn(data)
    print(f"[{job_name}] Ready.")
    return summary_html, data


def main():
    jobs = [
        ("US Economic News", us_econ.fetch_data,          us_econ.process,          us_econ.notify),
        ("Tech News",        tech_news.fetch_data,         tech_news.process,        tech_news.notify),
        ("GitHub Trending",  github_trending.fetch_data,   github_trending.process,  github_trending.notify),
    ]

    # Step 1: Fetch + process all 3 jobs in parallel
    ready = {}  # job_name -> (notify_fn, summary_html, data)
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(_run, name, fetch_fn, process_fn): (name, notify_fn)
            for name, fetch_fn, process_fn, notify_fn in jobs
        }
        for future in as_completed(futures):
            name, notify_fn = futures[future]
            try:
                summary_html, data = future.result()
                ready[name] = (notify_fn, summary_html, data)
            except Exception as e:
                print(f"[{name}] ERROR during fetch/process: {e}")

    if not ready:
        print("All jobs failed. No emails sent.")
        return

    # Step 2: All jobs ready — send emails simultaneously
    print(f"\nAll {len(ready)}/3 jobs ready. Sending emails...")
    with ThreadPoolExecutor(max_workers=3) as executor:
        send_futures = {
            executor.submit(notify_fn, summary_html, data): name
            for name, (notify_fn, summary_html, data) in ready.items()
        }
        for future in as_completed(send_futures):
            name = send_futures[future]
            try:
                future.result()
                print(f"[{name}] Email sent.")
            except Exception as e:
                print(f"[{name}] Email failed: {e}")


if __name__ == "__main__":
    main()
