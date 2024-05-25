from flask import Flask, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import time

#NOTE for some reason must do flask run, cannot just run 
#next to-do is to add automatic refresh so that I don't have to automatically refresh everytime

app = Flask(__name__)
app.secret_key = "ONcs92894hfnl"
app.config['SESSION_COOKIE_NAME'] = 'Rickys cookie'
TOKEN_INFO = "token_info"

if __name__ == '__main__':
    app.run(debug = True)

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


@app.route('/')
def login():
    sp_oauth = create_spotify_oath()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oath()
    session.clear()
    code = request.args.get('code')
    access_token = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = access_token
    # return redirect(url_for('getTracks', _external = True))
    return redirect(url_for('get20TopArtists', _external = True))
    # return 'redirect'

@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login", _external = True))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    current_track = sp.current_user_playing_track()
    formatted_info = format_currently_playing_track(current_track)
    return formatted_info

@app.route('/get20TopArtists')
def get20TopArtists():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login", _external = True))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_artists = sp.current_user_top_artists(limit=50, offset = 0)['items'][0:50]
    format_top_artists(top_artists)
    return "hi"

def format_top_artists(top_artists):
    for artist in top_artists:
        print("Name:", artist['name'])
        print("Popularity:", artist['popularity'])
        print("Genres:", ", ".join(artist['genres']))
        print("Followers:", artist['followers']['total'])
        print("Spotify URI:", artist['external_urls']['spotify'])
        print("Images:")
        for image in artist['images']:
            print(f"  - {image['url']}")
        print()




# Function to format and print the currently playing track information
def format_currently_playing_track(track_info):
    print('test')
    print('test')
    print('test')
    print('test')
    print('test')
    print('test')
    if not track_info or not track_info.get('item'):
        return "No track is currently playing."

    track = track_info['item']
    album = track['album']
    artists = ", ".join([artist['name'] for artist in track['artists']])
    album_artists = ", ".join([artist['name'] for artist in album['artists']])
    album_images = "\n".join([f"  - {image['url']}" for image in album['images']])
    available_markets = ", ".join(album['available_markets'])

    formatted_info = (
        f"Currently Playing Track:\n"
        f"  Name: {track['name']}\n"
        f"  Artists: {artists}\n"
        f"  Duration (ms): {track['duration_ms']}\n"
        f"  Popularity: {track['popularity']}\n"
        f"  Preview URL: {track['preview_url']}\n"
        f"  External URL: {track['external_urls']['spotify']}\n"
        f"  Track URI: {track['uri']}\n"
        f"Album Information:\n"
        f"  Name: {album['name']}\n"
        f"  Artists: {album_artists}\n"
        f"  Release Date: {album['release_date']}\n"
        f"  Total Tracks: {album['total_tracks']}\n"
        f"  Album Type: {album['album_type']}\n"
        f"  Album URI: {album['uri']}\n"
        f"  External URL: {album['external_urls']['spotify']}\n"
        f"  Images:\n{album_images}\n"
        f"Available Markets:\n  {available_markets}\n"
    )
    print(formatted_info)
    return formatted_info

# @app.route('/getPlaylists')
# def getPlaylists():
#     try:
#         token_info = get_token()
#     except:
#         print("user not logged in")
#         return redirect(url_for("login", _external = False))

#     sp = spotipy.Spotify(auth=token_info['access_token'])
#     return str(sp.playlisto(limit=20, offset = 0)['items'][0:5])



def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"

    now = int(time.time())
    expired = token_info['expires_at'] - now < 60
    if expired:
        sp_oauth = create_spotify_oath()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    
    return token_info


def create_spotify_oath():
    return SpotifyOAuth(
        client_id=client_id, 
        client_secret= client_secret, 
        redirect_uri= url_for('redirectPage', _external = True),
         scope="user-library-read user-top-read user-read-currently-playing")


