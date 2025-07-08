# Import the Spotipy library for interacting with the Spotify API
import spotipy

def fetch_playlist_tracks(sp: spotipy.Spotify, playlist_id: str):
    """
    Fetches all tracks from a given Spotify playlist.

    Args:
        sp (spotipy.Spotify): An authenticated Spotipy client instance.
        playlist_id (str): The ID of the Spotify playlist.

    Returns:
        list: A list of strings, where each string is in the format "Track Name - Artist Name".
    """
    # Get the tracks from the specified playlist using the provided Spotipy client
    results = sp.playlist_tracks(playlist_id)
    
    # Initialize an empty list to store the formatted track information
    tracks = []
    
    # Loop through each item in the playlist's track list
    for item in results['items']:
        # Get the track object from the item
        track = item['track']
        # Format the track information as "Track Name Artist Name" and add it to the list
        tracks.append(f"{track['name'] } {track['artists'][0]['name']}")
            
    # Return the list of formatted track strings
    return tracks