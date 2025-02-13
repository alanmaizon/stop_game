function updateImagesBasedOnTheme() {
    const assistantImg = document.getElementById('assistant-image');
    const playerImg = document.getElementById('player-image');
    const sorryImg = document.getElementById('sorry-image');
    const resultImg = document.getElementById('result-image');
    const darkModeEnabled = document.body.classList.contains('dark-mode');

    const assistantGif = document.body.dataset.assistantGif;
    const assistant1Gif = document.body.dataset.assistant1Gif;
    const playerGif = document.body.dataset.playerGif;
    const player1Gif = document.body.dataset.player1Gif;
    const sorryGif = document.body.dataset.sorryGif;
    const sorry1Gif = document.body.dataset.sorry1Gif;

    if (assistantImg) {
        assistantImg.src = darkModeEnabled ? assistantGif : assistant1Gif;
    }
    if (playerImg) {
        playerImg.src = darkModeEnabled ? playerGif : player1Gif;
    }
    if (sorryImg) {
        sorryImg.src = darkModeEnabled ? sorryGif : sorry1Gif;
    }
    if (resultImg) {
        const score = parseInt(resultImg.dataset.score);
        const allcorrect = resultImg.dataset.allcorrect === 'true';
        if (allcorrect || score > 0) {
            resultImg.src = darkModeEnabled ? playerGif : player1Gif;
        } else {
            resultImg.src = darkModeEnabled ? sorryGif : sorry1Gif;
        }
    }
}

// Function to toggle dark mode based on checkbox state
function toggleDarkMode() {
    const isChecked = document.getElementById('darkModeSwitch').checked;
    document.body.classList.toggle('dark-mode', isChecked); // Add/remove class based on state
    localStorage.setItem('darkMode', isChecked ? 'enabled' : 'disabled'); // Save preference
    updateImagesBasedOnTheme(); // Update images based on theme
}

// Apply dark mode on page load if it was enabled
document.addEventListener('DOMContentLoaded', function () {
    const darkModeSwitch = document.getElementById('darkModeSwitch');
    const darkModeEnabled = localStorage.getItem('darkMode') === 'enabled';

    // Set the checkbox state based on preference
    darkModeSwitch.checked = darkModeEnabled;

    // Apply dark mode class if enabled
    if (darkModeEnabled) {
        document.body.classList.add('dark-mode');
    }

    // Add event listener to toggle dark mode on checkbox change
    darkModeSwitch.addEventListener('change', toggleDarkMode);

    // Initial check for images
    updateImagesBasedOnTheme();
});

// Listen for changes in the system color scheme
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    const darkModeSwitch = document.getElementById('darkModeSwitch');
    const darkModeEnabled = e.matches;

    // Update the checkbox state
    darkModeSwitch.checked = darkModeEnabled;

    // Toggle dark mode class
    document.body.classList.toggle('dark-mode', darkModeEnabled);

    // Update images based on theme
    updateImagesBasedOnTheme();
});