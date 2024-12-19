// timer.js

export function initializeTimer(duration, onStopCallback) {
    let timer = duration; // Timer duration in seconds
    const timerElement = document.getElementById('timer');
    const stopButton = document.getElementById('stopButton');
    const form = document.getElementById('wordForm');

    // Countdown logic
    const countdown = setInterval(() => {
        timer -= 1;
        timerElement.innerText = timer;

        if (timer <= 0) {
            clearInterval(countdown);
            alert("Time's up!");
            onStopCallback(); // Auto-submit when the timer ends
        }
    }, 1000);

    // Stop button logic
    stopButton.addEventListener('click', () => {
        clearInterval(countdown);
        alert("You stopped the game!");
        onStopCallback(); // Submit the form when Stop is clicked
    });
}
