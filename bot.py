import csv
import requests

def run_scraper():
    # TikTok Creative Center ka internal API URL
    url = "https://ads.tiktok.com/business/creativecenter/api/hashtag/list/pc?period=7&region=PK"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://ads.tiktok.com/business/creativecenter/hashtag/pc/en"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        hashtags = data.get('data', {}).get('hashtag_list', [])
        
        with open('trends.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Hashtag", "Popularity"])
            for item in hashtags[:10]:
                writer.writerow([item.get('name'), item.get('popularity')])
    else:
        print(f"Error: {response.status_code}")

if __name__ == "__main__":
    run_scraper()
