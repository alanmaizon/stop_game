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
        if (areAllFieldsFilled()) {
            clearInterval(countdown);
            alert("You stopped the game!");
            form.submit(); // Submit the form when Stop is clicked
            fetch(`/game/stop_round/${round_id}/`, { method: 'POST' }) // Stop the round
                .then(response => response.json())
                .then(data => {
                    if (data.message === 'Round stopped!') {
                        window.location.href = `/game/results/${round_id}/`; // Redirect to results page
                    }
                });
        } else {
            alert("Please fill all the fields before stopping the game.");
        }
    });

    function areAllFieldsFilled() {
        const inputs = form.querySelectorAll('input[type="text"]');
        for (let input of inputs) {
            if (input.value.trim() === '') {
                return false;
            }
        }
        return true;
    }
}