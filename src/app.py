#NOTE TO DO IS TO ADD BLUEPRINTS SO THIS FILE ISNT A JUNK, BUT RIGHT NOW SPOTIY OAUTH IS KINDA HARD TO ROUTE AND ACT ON
from flask import Flask, request, url_for, session, redirect, jsonify, render_template
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from format import *
import spotipy
import os
import requests
import time
import json
import sys
sys.path.append('/Users/fluffy/repos/Spotifyapp/Mosaics/ColorHarmonicMosaics')

import MosaicGenerator


app = Flask(__name__)
CORS(app, supports_credentials= True)
app.secret_key = "ONcs92894hfnl"
app.config['SESSION_COOKIE_NAME'] = 'Rickys cookie'
TOKEN_INFO = "token_info"

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_spotify():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return None
    return spotipy.Spotify(auth=token_info['access_token'])


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
         scope="user-library-read user-top-read user-read-currently-playing user-modify-playback-state playlist-modify-private" )

def parse_query(query):
    params = {}
    # Check if the query contains "by", indicating it's in the format "track by artist"
    if " by " in query:
        # Split the query by "by" to separate track and artist
        track, artist = query.split(" by ", 1)
        params['track'] = track.strip()
        params['artist'] = artist.strip()
    else:
        # Split the query into words
        words = query.split()
        modified_query = []
        for word in words:
            # Check if the word contains letters and digits (assuming digits are in artist names)
            if any(char.isalpha() for char in word) and any(char.isdigit() for char in word):
                # If it contains both letters and digits, assume it's in the format "track:Unwritten artist:Natasha Bedingfield"
                modified_query.append(word)
            else:
                # Otherwise, keep the word as it is
                modified_query.append(word)
        # Join the modified query to form the final query string
        query = ' '.join(modified_query)
        # Split the modified query by spaces
        parts = query.split()
        # Iterate through each part to extract parameters
        for part in parts:
            # Split each part by ':'
            key_value = part.split(':')
            # Ensure there's a key-value pair
            if len(key_value) == 2:
                key, value = key_value
                # Store the key-value pair in the params dictionary
                params[key.lower()] = value
        # If no 'track' key was found, assume the input is just the artist name
        if 'track' not in params:
            params['artist'] = ' '.join(parts)

    return params

# # Example usage:
# query = 'Unwritten by Natasha Bedingfield'
# search_params = parse_query(query)
# print(search_params)

# query = 'Natasha Bedingfield'
# search_params = parse_query(query)
# print(search_params)

# {'track': 'Unwritten', 'artist': 'Natasha Bedingfield'}
# {'artist': 'Natasha Bedingfield'}


#return song id given a query
def search_song(query):
    sp = get_spotify()
    if sp is None:
        return redirect(url_for("login", _external=True))
    result = sp.search(q = query, type = 'track', limit = 1)
    if result['tracks']['items']:
        track = result['tracks']['items'][0]
        track_id = track['id']
        track_name = track['name']
        return track_id, track_name
        return f"Track ID: {track_id}, Track Name: {track_name}"
    else:
        return "No results found"
    
#return artist id given a query
def search_artist(query):
    sp = get_spotify()
    if sp is None:
        return redirect(url_for("login", _external=True))
    result = sp.search(q = query, type = 'artist', limit = 1)
    if result['artists']['items']:
        artist = result['artists']['items'][0]
        artist_id = artist['id']
        artist_name = artist['name']
        return artist_id, artist_name;
        return f"Artist ID: {artist_id}, Artist Name: {artist_name}"
    else:
        return "No results found"

def get_album_id(query):
    sp = get_spotify()
    if sp is None:
        return redirect(url_for("login", _external=True))
    results = sp.search(q=query, limit=1, type='album')
    
    return results['albums']['items'][0]['id']

def get_album_tracks(album_id):
    sp = get_spotify()
    if sp is None:
        return redirect(url_for("login", _external=True))
    tracks = sp.album_tracks(album_id)
    return tracks

def download_image(url, directory):
    # Create the directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)

    # Get the file name from the URL
    file_name = url.split('/')[-1]
    # Ensure the file name ends with .jpg
    if not file_name.lower().endswith('.jpg'):
        file_name += '.jpg'

    file_path = os.path.join(directory, file_name)

    # Download the image
    with open(file_path, 'wb') as f:
        response = requests.get(url)
        f.write(response.content)

    return file_path


def download_album_cover(query):
    sp = get_spotify()
    album_id = get_album_id(query)
    # print('downloaded')
    # print(sp.album(album_id))
    return sp.album(album_id)


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login')
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
    return redirect(url_for('getCurrentTrack', _external = True))

@app.route('/AlbumCoverMosaic', methods=['GET', 'POST'])
def AlbumCoverMosaic():
    # sp = get_spotify()
    # if sp is None:
    #     return redirect(url_for("login", _external=True))
    if request.method == 'POST':
        data = request.get_json()
        album_info = data.get('albumName')
        inputs = MosaicGenerator.get_user_inputs()
        MosaicGenerator.createMosaic(*inputs)
        #NOTE still need to fix the directory relatives for the images, right now the terminal is conlicting with my js calls to it
        return {'album_name': album_info}
    
    if request.method == 'GET':
        return {"mosaic_url": 'https://i.scdn.co/image/ab67616d0000b273715973050587fe3c93033aad',
                "album_name": "Rodeo"
                }
    
        # url = download_album_cover('album%3ARodeo%20artist%3ATravis%20Scott')['images'][0]['url']
        # directory = 'album_cover'
        # downloaded_file = download_image(url, directory)
        # print(f'Downloaded file: {downloaded_file}')
        # return download_album_cover('album%3ARodeo%20artist%3ATravis%20Scott')['images'][0]['url']


#playback features
@app.route('/Pause')
def Pause():
    sp = get_spotify()
    if sp is None:
        return redirect(url_for("login", _external=True))
    sp.pause_playback()
    return jsonify({"data": "successful pause"})

@app.route('/Resume')
def Resume():
    sp = get_spotify()
    if sp is None:
        return redirect(url_for("login", _external=True))
    sp.start_playback()
    return jsonify({"data": "successful resume"})

@app.route('/Previous')
def Previous():
    sp = get_spotify()
    if sp is None:
        return redirect(url_for("login", _external=True))
    sp.previous_track()
    return jsonify({"data": "successful prev"})

@app.route('/Next')
def Next():
    sp = get_spotify()
    if sp is None:
        return redirect(url_for("login", _external=True))
    sp.next_track()
    return jsonify({"data": "successful next"})

@app.route('/getCurrentTrack')
def getCurrentTrack():
    sp = get_spotify()
    if sp is None:
        return redirect(url_for("login", _external=True))
    current_track = sp.current_user_playing_track()
    formatted_info = format_currently_playing_track(current_track)
    return jsonify({"data": formatted_info})

@app.route('/addSongToQueue')
def addSongToQueue():
    sp = get_spotify()
    if sp is None:
        return redirect(url_for("login", _external=True))
    songid, songname = search_song('track:Unwritten artist:Natasha Bedingfield')
    sp.add_to_queue(uri = songid)
    return f"Song: {songname} has been added to the queue."

#Song Features

@app.route('/SimilarSongs')
def SimilarSongs():
    sp = get_spotify()
    if sp is None:
        return redirect(url_for("login", _external=True))
    artist_id, artist_name= search_artist(query = 'artist:aespa')
    related_artists = sp.artist_related_artists(artist_id)
    return f"related artists to {artist_name} are {related_artists}"

def AddSongToPlaylist(playlistid):
    sp = get_spotify()
    if sp is None:
        return redirect(url_for("login", _external=True))
    trackid, trackname = search_song('track:Unwritten artist:Natasha Bedingfield')
    userprofile = sp.current_user()
    userid = userprofile['id']
    sp.user_playlist_add_tracks(user = userid, playlist_id=playlistid, tracks = [trackid])
    return 'added songs'
    
@app.route('/CreatePlaylist')
def CreatePlaylist():
    sp = get_spotify()
    if sp is None:
        return redirect(url_for("login", _external=True))
    name = "a test playlist"
    userprofile = sp.current_user()
    userid = userprofile['id']
    playlist = sp.user_playlist_create(user = userid, name = "a test", public = False)
    id = playlist['id']
    AddSongToPlaylist(id)

    return 'created playlist'


@app.route('/audio_analysis')
def audio_analysis():
    sp = get_spotify()
    if sp is None:
        return redirect(url_for("login", _external=True))
    song_id, song_name = search_song('track:Trap Queen artist:Fetty Wap')
    sp.add_to_queue(uri = song_id)
    analysis = sp.audio_analysis(song_id)


    return analysis


@app.route('/audio_features')
def audio_features():
    sp = get_spotify()
    if sp is None:
        return redirect(url_for("login", _external=True))
    album_id = get_album_id('album%3ARodeo%20artist%3ATravis%20Scott')
    album = get_album_tracks(album_id)
    print('yoyo')
    print(type(album))

    track_ids = [track['id'] for track in album['items']]
    analysis = sp.audio_features(track_ids)
    for track_id in track_ids:
        sp.add_to_queue(track_id)

    save_file = open("./data/audio_features.json", "w")  
    json.dump(analysis, save_file, indent = 1)  
    save_file.close()  

    

    return analysis

#time frames(short_term 4 weeks, medium_term 6 months default, long_term roughly 1 year
@app.route('/get50TopArtists')
def get50TopArtists():
    sp = get_spotify()
    if sp is None:
        return redirect(url_for("login", _external=True))
    #a list of dictionaries is returned

    top_artists = sp.current_user_top_artists(limit=50, offset = 0)['items'][0:50]
    
    formatted_artists = []
    for artist in top_artists:
        image_data = artist.get('images', [])  # Get the list of images or an empty list if not available
        image_url = image_data[0]['url'] if image_data else None
        formatted_artist = {
            'name': artist['name'],
            'genres': artist['genres'],
            'image_url': image_url  # Include the image URL in the formatted data
        }
        formatted_artists.append(formatted_artist)

    save_file = open("./data/top_artists.json", "w")  
    json.dump(top_artists, save_file, indent = 1)  
    save_file.close()  

    return jsonify({'data': formatted_artists})

@app.route('/get50TopTracks')
def get50TopTracks():
    sp = get_spotify()
    if sp is None:
        return redirect(url_for("login", _external=True))
    top_tracks = sp.current_user_top_tracks(limit=50, offset=0)['items']
    formatted_tracks = []
    for track in top_tracks:
        formatted_track = {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'uri': track['uri']
        }
        formatted_tracks.append(formatted_track)

    save_file = open("./data/top_tracks.json", "w")  
    json.dump(top_tracks, save_file, indent = 1)  
    save_file.close()  

    return jsonify({'data': formatted_tracks})




if __name__ == '__main__':
    app.run(debug = True)