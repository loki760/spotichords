import requests
from bs4 import BeautifulSoup
import urllib.parse
import json

def _get_chords_from_tab_page(tab_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(tab_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    store_div = soup.find("div", class_="js-store")
    if not store_div:
        return "Could not find chords."

    data = json.loads(store_div["data-content"])
    chords = data.get("store", {}).get("page", {}).get("data", {}).get("tab_view", {}).get("wiki_tab", {}).get("content", "")
    return chords

def scrape_chords(song_name):
    query = urllib.parse.quote_plus(song_name)
    url = f"https://www.ultimate-guitar.com/search.php?search_type=title&value={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    
    store_div = soup.find("div", class_="js-store")
    if not store_div:
        return "Could not find song."

    data = json.loads(store_div["data-content"])
    tabs = data["store"]["page"]["data"].get("results", [])

    if not tabs:
        return "No tabs found for this song."

    # Get the first result that is a chord tab
    for tab in tabs:
        if tab.get("type") == "Chords":
            tab_url = tab["tab_url"]
            return _get_chords_from_tab_page(tab_url)

    return "No chord tabs found for this song."