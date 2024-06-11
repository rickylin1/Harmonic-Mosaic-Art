# from flask import Blueprint, session, url_for
# from spotipy.oauth2 import SpotifyOAuth
# import time
# import os
# from dotenv import load_dotenv
# import spotipy

# spotifysetup_bp = Blueprint('spotifysetup', __name__)

# load_dotenv()
# client_id = os.getenv("CLIENT_ID")
# client_secret = os.getenv("CLIENT_SECRET")
# TOKEN_INFO = "token_info"

# def get_spotify():
#     try:
#         token_info = get_token()
#     except:
#         print("User not logged in spotifysetup")
#         return None
#     return spotipy.Spotify(auth=token_info['access_token'])


# def get_token():
#     token_info = session.get(TOKEN_INFO, None)
#     if not token_info:
#         raise "exception"

#     now = int(time.time())
#     expired = token_info['expires_at'] - now < 60
#     if expired:
#         sp_oauth = create_spotify_oath()
#         token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
#     return token_info


# def create_spotify_oath():
#     return SpotifyOAuth(
#         client_id=client_id, 
#         client_secret=client_secret, 
#         redirect_uri=url_for('spotifysetup.redirectPage', _external=True),
#         scope="user-library-read user-top-read user-read-currently-playing user-modify-playback-state playlist-modify-private" 
#     )
