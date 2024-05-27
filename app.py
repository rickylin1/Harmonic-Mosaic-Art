from flask import Flask, request, url_for, session, redirect, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import time

#NOTE for some reason must do flask run, cannot just run 
#next to-do is to add automatic refresh so that I don't have to automatically refresh everytime
#also reduce inefficiencies by removing duplication?

app = Flask(__name__)
app.secret_key = "ONcs92894hfnl"
app.config['SESSION_COOKIE_NAME'] = 'Rickys cookie'
TOKEN_INFO = "token_info"

# if __name__ == '__main__':
#     app.run(debug = True)

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
    return redirect(url_for('addSongToQueue', _external = True))
    # return redirect(url_for('audio_features', _external = True))
    # return redirect(url_for('Pause', _external = True))
    # return redirect(url_for('Resume', _external = True))
    # return redirect(url_for('Previous', _external = True))
    # return redirect(url_for('Next', _external = True))
    # return redirect(url_for('CreatePlaylist', _external = True))
    # return redirect(url_for('SimilarSongs', _external = True))
    # return redirect(url_for('get20TopArtists', _external = True))
    return redirect(url_for('get20TopTracks', _external = True))
    ##for top tracks and artists can specify a time range as well

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


@app.route('/Pause')
def Pause():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login", _external = True))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    sp.pause_playback()
    return 'paused'


def AddSongToPlaylist(playlistid):
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login", _external = True))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    trackid, trackname = search_song('track:Unwritten artist:Natasha Bedingfield')
    userprofile = sp.current_user()
    userid = userprofile['id']
    sp.user_playlist_add_tracks(user = userid, playlist_id=playlistid, tracks = [trackid])
    return 'added songs'
    


@app.route('/CreatePlaylist')
def CreatePlaylist():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login", _external = True))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    name = "a test playlist"
    userprofile = sp.current_user()
    userid = userprofile['id']
    playlist = sp.user_playlist_create(user = userid, name = "a test", public = False)
    id = playlist['id']
    AddSongToPlaylist(id)

    return 'created playlist'

@app.route('/Resume')
def Resume():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login", _external = True))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    sp.start_playback()
    return 'start'

@app.route('/Previous')
def Previous():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login", _external = True))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    sp.previous_track()
    return 'prev'


@app.route('/Next')
def Next():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login", _external = True))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    sp.next_track()
    return 'next'

#return song id given a query
def search_song(query):
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login", _external = True))

    sp = spotipy.Spotify(auth=token_info['access_token'])
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
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login", _external = True))

    sp = spotipy.Spotify(auth=token_info['access_token'])
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
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login", _external = True))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.search(q=query, limit=1, type='album')
    print('test')
    print('test')
    print('test')
    print(str(type(results)))
    print(results['albums']['items'][0]['id'])

    # album_list = []
    # for album in results['albums']['items']:
    #     album_info = {
    #         'name': album['name'],
    #         'artist': album['artists'][0]['name'],
    #         'release_date': album['release_date']
    #         # Add more fields as needed
    #     }
    #     album_list.append(album_info)
    
    return results['albums']['items'][0]['id']

def get_album_tracks(album_id):
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login", _external = True))
    sp = spotipy.Spotify(auth=token_info['access_token'])
    tracks = sp.album_tracks(album_id)
    return tracks

#POTENTIAL, TAKE AN ARTIST OR ALBUM AND RANDOMLY SHUFFLE SONGS INTO QUEUE??
# @app.route('/NewReleases')
# def NewReleases():


@app.route('/addSongToQueue')
def addSongToQueue():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login", _external = True))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    # songid, songname = search_song('track:Unwritten artist:Natasha Bedingfield')
    songid, songname = search_song('Unwritten Natasha Bedingfield')
    sp.add_to_queue(uri = songid)
    return f"Song: {songname} has been added to the queue."

@app.route('/SimilarSongs')
def SimilarSongs():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login", _external = True))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    artist_id, artist_name= search_artist(query = 'artist:aespa')
    related_artists = sp.artist_related_artists(artist_id)
    return f"related artists to {artist_name} are {related_artists}"

@app.route('/audio_analysis')
def audio_analysis():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect(url_for("login", _external=True))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    song_id, song_name = search_song('track:Trap Queen artist:Fetty Wap')

    sp.add_to_queue(uri = song_id)
    

    analysis = sp.audio_analysis(song_id)
    

    return analysis


@app.route('/audio_features')
def audio_features():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect(url_for("login", _external=True))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    album_id = get_album_id('album%3ARodeo%20artist%3ATravis%20Scott')
    album = get_album_tracks(album_id)
    print('yoyo')
    print(type(album))

    track_ids = [track['id'] for track in album['items']]
    analysis = sp.audio_features(track_ids)
    for track_id in track_ids:
        sp.add_to_queue(track_id)

    return analysis

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

@app.route('/get20TopTracks')
def get20TopTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect(url_for("login", _external = True))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    top_tracks = sp.current_user_top_tracks(limit=20, offset=0)['items']
    formatted_tracks = []
    for track in top_tracks:
        formatted_track = {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'uri': track['uri']
        }
        formatted_tracks.append(formatted_track)

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
         scope="user-library-read user-top-read user-read-currently-playing user-modify-playback-state playlist-modify-private" )


if __name__ == '__main__':
    app.run(debug = True)