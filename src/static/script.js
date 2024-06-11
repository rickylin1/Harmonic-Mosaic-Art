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
        resultDiv.innerText = data ? data['data'] : 'Failed to fetch data';
    });
}

addButtonClickListener('pauseButton', 'pauseResult', 'Pause');
addButtonClickListener('resumeButton', 'resumeResult', 'Resume');
addButtonClickListener('previousButton', 'previousResult', 'Previous');
addButtonClickListener('nextButton', 'nextResult', 'Next');
