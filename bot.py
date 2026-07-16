import csv
import os
import requests
from playwright.sync_api import sync_playwright

# Error-proof stealth import
try:
    from playwright_stealth import stealth_sync
except ImportError:
    stealth_sync = None

def send_telegram_msg(msg):
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, data={'chat_id': chat_id, 'text': msg})

def run_scraper():
    with sync_playwright() as p:
        # Browser launch with stealth-friendly arguments
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
        page = context.new_page()
        
        if stealth_sync:
            stealth_sync(page)
        
        page.goto("https://www.tiktok.com/trending")
        page.wait_for_timeout(8000) # Thora zyada wait
        
        # Titiles scrap karein
        titles = page.query_selector_all('h2')
        data = [[t.inner_text()] for t in titles[:10]]
        
        with open('trends.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Viral_Trend_Title"])
            writer.writerows(data)
            
        browser.close()
        send_telegram_msg("✅ DataVelocity_bot: Trends scraped!")

if __name__ == "__main__":
    run_scraper()
