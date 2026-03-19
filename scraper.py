import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

BASE_URL = "https://saras.cbse.gov.in"
LIST_URL = BASE_URL + "/saras/AffiliatedList/ListOfSchdirReport"

STATE_CODE = "17"  # MAHARASHTRA

session = requests.Session()

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": LIST_URL
}

print("🔄 Fetching token...")

response = session.get(LIST_URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

token_tag = soup.find("input", {"name": "__RequestVerificationToken"})
if not token_tag:
    print("❌ Token not found")
    exit()

token = token_tag["value"]

print("🔄 Fetching Maharashtra school list...")

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

print(f"✅ Found {len(rows)} schools in Maharashtra")

detail_urls = []

for row in rows:
    cols = row.find_all("td")
    if cols:
        view_tag = cols[-1].find("a")
        if view_tag:
            detail_urls.append(BASE_URL + view_tag["href"])

all_school_details = []

# -----------------------------
# RETRY LOGIC
# -----------------------------
def scrape_detail(url, retries=3):
    for attempt in range(retries):
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

        except Exception as e:
            time.sleep(1)  # retry delay

    return None


print("⚡ Scraping detail pages...")

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(scrape_detail, url) for url in detail_urls]

    # ✅ Smooth Progress Bar
    with tqdm(total=len(futures), desc="Progress", unit="req") as pbar:
        for future in as_completed(futures):
            result = future.result()
            if result:
                all_school_details.append(result)
            pbar.update(1)

# -----------------------------
# SAVE OUTPUT
# -----------------------------
if all_school_details:
    df = pd.DataFrame(all_school_details)
    df.to_csv("Maharashtra_full_school_details.csv", index=False)
    print("\n✅ Maharashtra FULL data saved successfully!")
else:
    print("❌ No data collected.")
