function updateImagesBasedOnTheme() {
    const assistantImg = document.getElementById('assistant-image');
    const playerImg = document.getElementById('player-image');
    const sorryImg = document.getElementById('sorry-image');
    const resultImg = document.getElementById('result-image');
    const darkModeEnabled = document.body.classList.contains('dark-mode');
    
    if (assistantImg) {
        assistantImg.src = darkModeEnabled ? "{% static 'assistant.gif' %}" : "{% static 'assistant1.gif' %}";
    }
    if (playerImg) {
        playerImg.src = darkModeEnabled ? "{% static 'player.gif' %}" : "{% static 'player1.gif' %}";
    }
    if (sorryImg) {
        sorryImg.src = darkModeEnabled ? "{% static 'sorry.gif' %}" : "{% static 'sorry1.gif' %}";
    }
    if (resultImg) {
        const score = parseInt(resultImg.dataset.score);
        const allcorrect = resultImg.dataset.allcorrect === 'true';
        if (allcorrect || score > 0) {
            resultImg.src = darkModeEnabled ? "{% static 'player.gif' %}" : "{% static 'player1.gif' %}";
        } else {
            resultImg.src = darkModeEnabled ? "{% static 'sorry.gif' %}" : "{% static 'sorry1.gif' %}";
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