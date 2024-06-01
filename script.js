document.addEventListener('DOMContentLoaded', function () {

    const topArtistsListItem = document.getElementById('topArtists');

    // Add click event listener to the top artists list item
    topArtistsListItem.addEventListener('click', function() {
    // Fetch top artists data from the server
    fetch('/get50TopArtists')
        .then(response => response.json())
        .then(data => {
            console.log(data);
            const newDiv = document.createElement('div');
            newDiv.textContent = 'new div';
            data.forEach(entry => {
                // Create an image element for each entry
                const img = document.createElement('img');
                img.src = entry.image_url; // Assuming 'image_url' is the key for the image URL in your dictionary

                // Append the image to the newDiv
                newDiv.appendChild(img);
            });
            document.body.appendChild(newDiv);
        })
        .catch(error => {
            console.error('Error fetching top artists:', error);
        });
    })
});