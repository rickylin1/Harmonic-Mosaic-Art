from flask import Flask, request, url_for, session, redirect, jsonify, render_template
from flask_cors import CORS, cross_origin
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import time
import json
import csv

app = Flask(__name__)
CORS(app)
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

def json_to_csv(json_data, csv_file_name):
    csv_file = csv_file_name
    with open(csv_file_name, mode='w', newline='') as file:
        # Create a CSV writer
        writer = csv.writer(file)
        
        # Write the header
        header = json_data[0].keys()
        writer.writerow(header)
        
        # Write the data rows
        for item in json_data:
            writer.writerow(item.values())

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

#POTENTIAL, TAKE AN ARTIST OR ALBUM AND RANDOMLY SHUFFLE SONGS INTO QUEUE??
# @app.route('/NewReleases')
# def NewReleases():


#recommendation

#remove old songs

#get playlists

#find duplicates


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
    return formatted_info

@app.route('/addSongToQueue')
def addSongToQueue():
    sp = get_spotify()
    if sp is None:
        return redirect(url_for("login", _external=True))
    songid, songname = search_song('track:Unwritten artist:Natasha Bedingfield')
    sp.add_to_queue(uri = songid)
    return f"Song: {songname} has been added to the queue."

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

    json_to_csv(analysis, "./data/audiofeatures.csv")

    

    return analysis

#time frames(short_term 4 weeks, medium_term 6 months default, long_term roughly 1 year
@app.route('/get50TopArtists')
def get50TopArtists():
    sp = get_spotify()
    if sp is None:
        return redirect(url_for("login", _external=True))
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
    
    json_to_csv(top_artists, "./data/topTracks.csv")
    return jsonify(formatted_artists)

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

    json_to_csv(top_tracks, "./data/topTracks.csv")
    return jsonify(formatted_tracks)

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



if __name__ == '__main__':
    app.run(debug = True)