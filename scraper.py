from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import csv

def scrape_trends():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) # Headless: Screen ki zaroorat nahi
        page = browser.new_page()
        stealth_sync(page) # Yeh Cloudflare ko "Human" banata hai
        
        page.goto("https://www.tiktok.com/trending")
        page.wait_for_timeout(5000) # Page load hone ka wait
        
        # Yahan aap apna scraping logic likhenge (element select karna)
        # Filhal hum sirf page ka title check kar rahe hain
        print(f"Scraped Title: {page.title()}")
        
        # Data ko CSV mein save karein
        with open('trends.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Trend"])
            writer.writerow([page.title()])
            
        browser.close()

scrape_trends()
