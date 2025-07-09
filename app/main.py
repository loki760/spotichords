# Import required FastAPI modules
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Import Spotify API library
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Import your custom modules
from app.spotify_fetcher import fetch_playlist_tracks
from app.chord_scraper import scrape_chords

# Load environment variables from .env file
import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the root directory
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Setup Jinja2 Templates for rendering HTML pages
# It looks for HTML files in the "templates" directory
templates = Jinja2Templates(directory="templates")

# Mount the "static" folder to serve static files like CSS, JS, and images
app.mount("/static", StaticFiles(directory="static"), name="static")


# Route: Home page (GET Request)
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """
    Renders the main page of the application.
    """
    # Renders the index.html template
    return templates.TemplateResponse("index.html", {"request": request})

os.environ["SPOTIPY_REDIRECT_URI"] = "http://127.0.0.1:8000/callback"
# Route: Spotify Login (GET Request)
@app.get("/login")
def login():
    """
    Redirects the user to the Spotify login page for authentication.
    """

    print("=== DEBUGGING REDIRECT URI ===")
    print(f"Using redirect URI: {os.getenv('SPOTIPY_REDIRECT_URI')}")
    # Initialize the Spotify OAuth flow with credentials from environment variables
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-read-private",  # This scope allows reading the user's private playlists
        show_dialog=True
    )
    # Get the Spotify authorization URL
    auth_url = sp_oauth.get_authorize_url()
    # Redirect the user to the Spotify login page
    return RedirectResponse(auth_url)


# Route: Spotify OAuth Callback (GET Request)
@app.get("/callback")
def callback(request: Request, code: str = None, error: str = None):
    if error:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Spotify authentication failed: {error}"
        })
    
    if not code:
        return RedirectResponse("/")
        
    try:
        sp_oauth = SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI")
        )
        token_info = sp_oauth.get_access_token(code)
        # Store token_info in session or database
        # ... rest of your callback logic
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Authentication error: {str(e)}"
        })

# Route: Get Chords for a Playlist (POST Request)
@app.post("/get_chords", response_class=HTMLResponse)
def get_chords(request: Request, playlist_id: str = Form(...)):
    """
    Fetches tracks from a selected playlist and scrapes their chords.
    """
    # Initialize the Spotify API client (ideally, you'd reuse the authenticated client)
    # For simplicity, we re-authenticate here. In a real app, you'd store the token.
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-read-private"
    )
    # A bit of a hack: we need a valid token to make a client.
    # Since we don't have the user's token from the callback,
    # we'll use a client credentials flow for this public playlist data.
    # Note: This won't work for private playlists.
    from spotipy.client import SpotifyCredentials
    client_credentials_manager = SpotifyCredentials(client_id=os.getenv("SPOTIPY_CLIENT_ID"), client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"))
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Fetch the playlist details to get the name
    playlist = sp.playlist(playlist_id)
    playlist_name = playlist['name']

    # Fetch the tracks from the selected playlist
    tracks = fetch_playlist_tracks(sp, playlist_id)
    # Scrape the chords for each track
    chords_data = {track: scrape_chords(track) for track in tracks}
    # Render the chords.html template, passing the song and chords data
    return templates.TemplateResponse("chords.html", {"request": request, "title": playlist_name, "chords": chords_data})


# Route: Manual Chord Scraper (POST Request)
@app.post("/scrape", response_class=HTMLResponse)
def scrape(request: Request, song: str = Form(...)):
    """
    Scrapes chords for a song provided via a form submission.
    """
    # Scrape the chords for the provided song name using the custom scraper function
    chords = scrape_chords(song)
    chords_data = {song: chords}
    # Render the chords.html template, passing the song name and scraped chords
    return templates.TemplateResponse("chords.html", {"request": request, "title": song, "chords": chords_data})