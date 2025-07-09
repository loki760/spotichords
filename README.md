
# Spotify Chord Scraper Web App

This is a web application that allows users to log in with their Spotify account, fetch playlists, and scrape guitar chords for songs using web scraping from e-chords.com.

## Features

- Login with Spotify (OAuth 2.0)
- Fetch Spotify playlists
- Search for chords of any song manually
- Scrape chords from ultimate guitar and display them on the web page
- Save scraped chords easily for personal use

## Tech Stack

- Python
- FastAPI
- Spotipy (Spotify API wrapper)
- BeautifulSoup (Web Scraping)
- Jinja2 (Templating)
- Uvicorn (ASGI server)
- Dotenv (Environment variable management)

## Project Structure

```
spotify-chord-scraper/
│
├── app/
│   ├── main.py              # FastAPI app & route handlers
│   ├── spotify_fetcher.py   # Spotify API playlist fetcher
│   └── chord_scraper.py     # Chord scraping logic
│
├── templates/               # Jinja2 templates for rendering HTML
│   ├── index.html           
│   └── chords.html          
│
├── static/                  # Static files (CSS, JS, Images)
│
├── .env                     # Spotify API credentials (not committed)
├── .gitignore               # Files & folders to ignore in git
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
```

## Setup Instructions

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/spotify-chord-scraper.git
cd spotify-chord-scraper
```

2. **Create a Virtual Environment and Install Dependencies**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Set Up Spotify API Credentials**

- Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
- Create an application and obtain the Client ID and Client Secret
- Set your Redirect URI to: `http://localhost:8000/callback`
- Create a `.env` file in the root directory and add:

```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8000/callback
```

4. **Run the Application**

```bash
uvicorn app.main:app --reload
```

5. **Visit the App**

Open your browser and navigate to:

```
http://localhost:8000
```

## Notes

- This app is for educational purposes.
- Use responsibly and respect the terms of service of any websites you scrape.
- You can extend this app to automatically fetch and scrape entire Spotify playlists.

## License

This project is licensed under the MIT License.
