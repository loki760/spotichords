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


# Route: Spotify Login (GET Request)
@app.get("/login")
def login():
    """
    Redirects the user to the Spotify login page for authentication.
    """
    # Initialize the Spotify OAuth flow with credentials from environment variables
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-read-private"  # This scope allows reading the user's private playlists
    )
    # Get the Spotify authorization URL
    auth_url = sp_oauth.get_authorize_url()
    # Redirect the user to the Spotify login page
    return RedirectResponse(auth_url)


# Route: Spotify OAuth Callback (GET Request)
@app.get("/callback")
def callback(code: str):
    """
    Handles the callback from Spotify after the user has logged in.
    """
    # Complete the Spotify OAuth flow using the authorization code from the callback
    sp_oauth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="playlist-read-private"
    )
    # Exchange the authorization code for an access token
    token_info = sp_oauth.get_access_token(code)
    # Initialize the Spotify API client with the obtained access token
    sp = spotipy.Spotify(auth=token_info['access_token'])
    # Fetch the current user's playlists
    playlists = sp.current_user_playlists()['items']
    # Return the list of playlists as a JSON response
    # In a real application, you would likely render a template with this data
    return {"playlists": playlists}


# Route: Manual Chord Scraper (POST Request)
@app.post("/scrape", response_class=HTMLResponse)
def scrape(request: Request, song: str = Form(...)):
    """
    Scrapes chords for a song provided via a form submission.
    """
    # Scrape the chords for the provided song name using the custom scraper function
    chords = scrape_chords(song)
    # Render the chords.html template, passing the song name and scraped chords
    return templates.TemplateResponse("chords.html", {"request": request, "song": song, "chords": chords})