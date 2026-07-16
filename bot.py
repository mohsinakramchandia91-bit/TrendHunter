import csv
import os
import requests
from playwright.sync_api import sync_playwright

def run_scraper():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Proper Desktop User-Agent taake full data render ho
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        page = context.new_page()
        
        # Creative Center Hashtag Page
        page.goto("https://ads.tiktok.com/business/creativecenter/hashtag/pc/en")
        
        # Dynamic content load hone ka wait karein
        page.wait_for_selector('.list-item', timeout=20000)
        
        # Hum poore 'list-item' block ko uthate hain
        items = page.query_selector_all('.list-item')
        
        data = []
        for item in items[:10]:
            # Har item ke andar se text nikalna
            name = item.query_selector('.hashtag-text')
            growth = item.query_selector('.index-item-text')
            
            if name and growth:
                data.append([name.inner_text(), growth.inner_text()])
        
        # Save results
        with open('trends.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Hashtag", "Growth_Rate"])
            writer.writerows(data)
            
        browser.close()

if __name__ == "__main__":
    run_scraper()
