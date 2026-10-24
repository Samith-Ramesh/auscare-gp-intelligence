import requests
from bs4 import BeautifulSoup
import time
import re

class AusGPWebScraper:
    def _init_(self):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8",
            "Accept-Language": "en-AU,en-US;q=0.9",
        }

    def scrape_url(self, url: str) -> list[str]:
        records = []
        try:
            print(f"[*] Crawling live target: {url}")
            resp = self.session.get(url, headers=self.headers, timeout=12)
            if resp.status_code != 200:
                return records

            soup = BeautifulSoup(resp.text, "html.parser")
            candidate_blocks = soup.find_all(["div", "article", "section", "li"])
            for block in candidate_blocks:
                text = block.get_text(separator=" ", strip=True)
                if re.search(r"Dr\s+[A-Z][a-z]+", text) and any(w in text for w in ["FRACGP", "MBBS", "General Practitioner", "Special Interests", "Health"]):
                    if 40 < len(text) < 400 and text not in records:
                        records.append(text)
            time.sleep(1.0)
        except Exception as e:
            print(f"    [!] Error scraping {url}: {e}")
        return records

    def run_live_harvest(self) -> list[str]:
        live_targets = [
            "https://lotusmedicalcentre.com.au/about-us/our-doctors/",
            "https://gbmc.com.au/our-doctors/"
        ]
        harvested = []
        for url in live_targets:
            listings = self.scrape_url(url)
            harvested.extend(listings)
        return list(dict.fromkeys(harvested))
