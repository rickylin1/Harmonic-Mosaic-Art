import os
import json
from collections import defaultdict

# Directory containing your JSON files
directory = './data/ExtendedStreamingHistory'

# Initialize a defaultdict to store song play counts and total play time
song_play_counts = defaultdict(lambda: {'play_count': 0, 'total_ms_played': 0, 'skip_count' : 0, 'artist_name' : ' ', 'album_name': ' '})

# Iterate over each JSON file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as file:
            data = json.load(file)
            for record in data:
                    track_name = record['master_metadata_track_name']
                    ms_played = int(record['ms_played'])
                    skipped = True if ms_played < 30000 else False
                    #i will consider it skipped if its been played for less than 30 seconds
                    artist_name = record.get('master_metadata_album_artist_name', 'Placeholder Artist')
                    album_name = record.get('master_metadata_album_album_name', 'Placeholder Album')

                    # If this is the first time we encounter this track, set the artist and album
                    if song_play_counts[track_name]['play_count'] == 0:
                        song_play_counts[track_name]['artist_name'] = artist_name
                        song_play_counts[track_name]['album_name'] = album_name
                    
                    if skipped:
                         song_play_counts[track_name]['skip_count'] += 1

                    song_play_counts[track_name]['play_count'] += 1
                    song_play_counts[track_name]['total_ms_played'] += ms_played

# Convert defaultdict to regular dictionary for JSON serialization
song_play_counts_dict = {track_name: {
    'play_count': int(info['play_count']),
    'total_ms_played': int(info['total_ms_played']),
    'skip_count': int(info['skip_count']),
    'artist_name': info['artist_name'],
    'album_name': info['album_name']
} for track_name, info in song_play_counts.items()}


output_file = './DatasetAnalysis/streamcounts.json'

# Write the dictionary to a JSON file
with open(output_file, 'w') as outfile:
    json.dump(song_play_counts_dict, outfile, indent=4)

print(f"Data saved to {output_file}")
