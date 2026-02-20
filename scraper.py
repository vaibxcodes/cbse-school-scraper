import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://saras.cbse.gov.in"
LIST_URL = BASE_URL + "/saras/AffiliatedList/ListOfSchdirReport"

# -----------------------------
# CHECK ARGUMENT
# -----------------------------
if len(sys.argv) != 2:
    print("Usage: python scraper.py <STATE_CODE>")
    print("Example: python scraper.py 05  # Bihar")
    sys.exit(1)

STATE_CODE = sys.argv[1]

# Create output directory if not exists
os.makedirs("output", exist_ok=True)

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": LIST_URL
}

# -----------------------------
# GET TOKEN
# -----------------------------
print("🔄 Fetching verification token...")
response = session.get(LIST_URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

token_tag = soup.find("input", {"name": "__RequestVerificationToken"})
if not token_tag:
    print("❌ Could not fetch token.")
    sys.exit(1)

token = token_tag["value"]

# -----------------------------
# FETCH SCHOOL LIST
# -----------------------------
print(f"🔄 Fetching school list for State Code: {STATE_CODE}...")

form_data = {
    "MainRadioValue": "State_wise",
    "State": STATE_CODE,
    "District": "",
    "Region": "",
    "InstName_orAddress": "",
    "RegAffNo": "0",
    "__Invariant": "RegAffNo",
    "SchoolStatusWise": "0",
    "__RequestVerificationToken": token
}

list_response = session.post(LIST_URL, data=form_data, headers=headers)
list_soup = BeautifulSoup(list_response.text, "html.parser")

rows = list_soup.select("table tbody tr")

print(f"✅ Found {len(rows)} schools")

if not rows:
    print("❌ No schools found. Check state code.")
    sys.exit(1)

detail_urls = []

for row in rows:
    cols = row.find_all("td")
    if cols:
        view_tag = cols[-1].find("a")
        if view_tag:
            detail_urls.append(BASE_URL + view_tag["href"])

# -----------------------------
# SCRAPE DETAIL PAGES
# -----------------------------
all_school_details = []

def scrape_detail(url):
    try:
        r = session.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        rows = soup.select("table tr")
        data = {}

        for row in rows:
            cells = row.find_all("td")
            if len(cells) == 2:
                key = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                data[key] = value

        return data
    except:
        return None

print("⚡ Scraping detail pages (multi-threaded)...")

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(scrape_detail, url) for url in detail_urls]
    for future in as_completed(futures):
        result = future.result()
        if result:
            all_school_details.append(result)

# -----------------------------
# SAVE OUTPUT
# -----------------------------
if all_school_details:
    output_file = f"output/state_{STATE_CODE}_school_details.csv"
    df = pd.DataFrame(all_school_details)
    df.to_csv(output_file, index=False)
    print(f"\n✅ Data saved successfully: {output_file}")
else:
    print("❌ No data collected.")
