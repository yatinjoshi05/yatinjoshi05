#!/usr/bin/env python3
"""
fetch_contributions.py — Fetch public GitHub contribution calendar and write data/contributions.json
No GitHub token required.
"""

import json
import re
import sys
from datetime import datetime
import requests
from bs4 import BeautifulSoup

USERNAME = "yatinjoshi05"
URL = f"https://github.com/users/{USERNAME}/contributions"

def fetch():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    resp = requests.get(URL, headers=headers, timeout=15)
    if resp.status_code != 200:
        print(f"Error fetching contributions: HTTP {resp.status_code}", file=sys.stderr)
        sys.exit(1)

    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Map tooltips by id
    tooltips = {}
    for tt in soup.find_all("tool-tip"):
        for_id = tt.get("for")
        if for_id:
            tooltips[for_id] = tt.get_text(strip=True)

    days = []
    # Find all table cells with data-date
    for td in soup.find_all("td", attrs={"data-date": True}):
        date = td["data-date"]
        level = int(td.get("data-level", "0"))
        td_id = td.get("id")
        
        count = 0
        if td_id and td_id in tooltips:
            m = re.match(r"^(\d+)\s+contribution", tooltips[td_id])
            if m:
                count = int(m.group(1))
        elif level > 0:
            count = level

        days.append({"date": date, "level": level, "count": count})

    total = sum(d["count"] for d in days)
    data = {
        "username": USERNAME,
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "total_contributions": total,
        "days": days
    }

    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Successfully saved {len(days)} days ({total} contributions) to data/contributions.json")

if __name__ == "__main__":
    fetch()
