async function fetchData(url) {
    try {
        const response = await fetch('/' + url);
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
}

function addButtonClickListener(buttonId, resultId, action) {
    document.getElementById(buttonId).addEventListener('click', async () => {
        const resultDiv = document.getElementById(resultId);
        const data = await fetchData(action);
        if (data && Array.isArray(data['data'])) {
            // Clear previous content
            resultDiv.innerHTML = '';
            // Iterate over each item in the 'data' array
            data['data'].forEach(item => {
                // Create a paragraph element to display each item
                const paragraph = document.createElement('p');
                if('name' in item && 'artist' in item && 'uri' in item){
                    //Top Tracks
                    paragraph.innerText = `Name: ${item['name']}, Artist: ${item['artist']}, URI: ${item['uri']}`;
                }
                else{
                    //Top artists
                    paragraph.innerText = `Name: ${item['name']}, Genres: ${item['genres']}, Image: ${item['image_url']}`;
                }
                // Append the paragraph to the resultDiv
                resultDiv.appendChild(paragraph);
            });
        }
        else if (data){
            resultDiv.innerText = data['data']  
        }
        else{
            resultDiv.innerText = 'Failed to fetch data'
        }
    });
}

addButtonClickListener('pauseButton', 'pauseResult', 'Pause');
addButtonClickListener('resumeButton', 'resumeResult', 'Resume');
addButtonClickListener('previousButton', 'previousResult', 'Previous');
addButtonClickListener('nextButton', 'nextResult', 'Next');
addButtonClickListener('currentTrackButton', 'currentTrackResult', 'getCurrentTrack');
addButtonClickListener('addSongToQueueButton', 'addSongToQueueResult', 'addSongToQueue');
addButtonClickListener('get50TopArtistsButton', 'get50TopArtistsResult', 'get50TopArtists');
addButtonClickListener('get50TopTracksButton', 'get50TopTracksResult', 'get50TopTracks');
