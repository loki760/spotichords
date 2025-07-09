import requests
from bs4 import BeautifulSoup
import urllib.parse
import json

def scrape_chords(song_name):
    query = urllib.parse.quote_plus(song_name)
    url = f"https://www.ultimate-guitar.com/search.php?search_type=title&value={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    
    store_div = soup.find("div", class_="js-store")
    if not store_div:
        return []

    data = json.loads(store_div["data-content"])
    tabs = data["store"]["page"]["data"].get("results", [])

    results = []
    for tab in tabs:
        results.append({
            "song": tab["song_name"],
            "artist": tab["artist_name"],
            "url": tab["tab_url"]
        })
    return results
