import json

# Path to your JSON file
json_file_path = './data/ExtendedStreamingHistory/Streaming_History_Audio_2022_12.json'

# Load JSON data
with open(json_file_path, 'r') as file:
    data = json.load(file)

# Initialize sets to store unique values
skipped = set()

# Iterate through each object in the JSON data
for record in data:
    skipped.add(record['skipped'])

# Print unique values
print("skipped", skipped)
