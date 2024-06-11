
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
    return formatted_info

