# Import necessary libraries
import requests  # For making HTTP requests to web pages
from bs4 import BeautifulSoup  # For parsing HTML and extracting data
import urllib.parse  # For URL-encoding the song name for the search query

def scrape_chords(song_name):
    """
    Scrapes guitar chords for a given song name from e-chords.com.

    Args:
        song_name (str): The name of the song to search for.

    Returns:
        str: The scraped chords as a string, or a message if chords are not found.
    """
    # URL-encode the song name to be used in the search URL
    query = urllib.parse.quote(song_name)
    # Construct the search URL for e-chords.com
    url = f"https://www.e-chords.com/search-all/{query}"

    # Send a GET request to the search URL
    response = requests.get(url)
    # Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the first search result link, which is typically the correct song
    result = soup.find("a", class_="music-link")
    # If no result is found, return a "not found" message
    if not result:
        return "Chords not found."

    # Construct the full URL for the song's chord page
    song_link = "https://www.e-chords.com" + result["href"]
    # Send a GET request to the song's chord page
    response = requests.get(song_link)
    # Parse the HTML response of the song page
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the <pre> tag with the class "core" which contains the chords
    chords_section = soup.find("pre", class_="core")
    # If the chords section is not found on the song page, return a message
    if not chords_section:
        return "Chords not found on song page."

    # Return the text content of the chords section, with leading/trailing whitespace removed
    return chords_section.text.strip()