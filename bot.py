import csv
import os
import requests
from playwright.sync_api import sync_playwright

def send_telegram_msg(msg):
    token = os.environ.get('TELEGRAM_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    if token and chat_id:
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={'chat_id': chat_id, 'text': msg})

def run_scraper():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile view emulate karna zaruri hai kyunke TikTok desktop pe limited data dikhata hai
        context = browser.new_context(viewport={'width': 375, 'height': 812}, user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)")
        page = context.new_page()
        
        # Hashtags ka trend page
        page.goto("https://ads.tiktok.com/business/creativecenter/hashtag/pc/en")
        page.wait_for_timeout(10000)
        
        # Viral Tags aur unki Popularity scrape karna
        # (Note: TikTok ke selectors change hote hain, hum yahan tags ko target kar rahe hain)
        tags = page.query_selector_all('.hashtag-text')
        growth = page.query_selector_all('.growth-rate')
        
        data = []
        for i in range(len(tags[:10])):
            data.append([tags[i].inner_text(), growth[i].inner_text() if i < len(growth) else "N/A"])
        
        with open('trends.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Hashtag", "Growth_Rate"])
            writer.writerows(data)
            
        browser.close()
        send_telegram_msg("🚀 DataVelocity: Professional Hashtag Intelligence updated!")

if __name__ == "__main__":
    run_scraper()
