import csv
import os
import requests
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

def send_telegram_msg(msg):
    token = os.environ['TELEGRAM_TOKEN']
    chat_id = os.environ['CHAT_ID']
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={'chat_id': chat_id, 'text': msg})

def run_scraper():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        stealth_sync(page)
        
        # TikTok Trending URL
        page.goto("https://www.tiktok.com/trending")
        page.wait_for_timeout(5000)
        
        # Scrape titles (Example: h2 tags are usually titles)
        titles = page.query_selector_all('h2')
        data = [[t.inner_text()] for t in titles[:10]]
        
        # Save to CSV
        with open('trends.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Viral_Trend_Title"])
            writer.writerows(data)
            
        browser.close()
        send_telegram_msg("🔥 Trend Update: Scrape Successful. Check your CSV!")

if __name__ == "__main__":
    run_scraper()
