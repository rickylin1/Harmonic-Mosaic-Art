from flask import Flask, request, url_for, session, redirect
import os
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler



app = Flask(__name__)
# app.secret_key = "ONcs92894hfno"
app.config['SECRET_KEY'] = 'verysecretkey'

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = 'http://127.0.0.1:5000/callback'
scope = 'playlist-read-private, user-top-read,app-remote-control'

cache_handler = FlaskSessionCacheHandler(session)

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=client_id, 
        client_secret= client_secret, 
        redirect_uri= redirect_uri,
        scope= scope,
        cache_handler = cache_handler,
        show_dialog = True)

def validatetoken():
     if not sp_o_auth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_o_auth.get_authorize_url()
        return redirect(auth_url)

sp_o_auth = create_spotify_oauth()

sp = Spotify(auth_manager = sp_o_auth)

@app.route('/')
def login():
    # validatetoken()
    if not sp_o_auth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_o_auth.get_authorize_url()
        return redirect(auth_url)
    # return redirect('https://www.youtube.com/feed/subscriptions')
    return redirect(url_for('get_playlists'))

@app.route('/callback')
def callback():
    sp_o_auth.get_access_token(request.args['code'])
    return redirect(url_for('get_playlists'))


@app.route('/get_playlists')
def get_playlists():
    if not sp_o_auth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_o_auth.get_authorize_url()
        return redirect(auth_url)
    playlists = sp.current_user_playlists()
    # return str(sp.current_user_top_artists(limit=20, offset = 0)['items'][0:20])
    return str(sp.current_user_playlists(limit=20, offset = 0)['items'][0:20])


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))








if __name__ == '__main__':
    app.run(debug = True)

