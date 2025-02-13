import { initializeTimer } from "{% static 'game/js/timer.js' %}";

document.getElementById('startButton').addEventListener('click', () => {
    document.getElementById('startButtonContainer').style.display = 'none';
    document.getElementById('letter').style.display = 'block';
    document.getElementById('timerContainer').style.display = 'block';
    document.getElementById('wordForm').style.display = 'block';
    document.getElementById('stopButtonContainer').style.display = 'block';
    document.getElementById('3dModelContainer').style.display = 'none'; // Hide the 3D model

    // Start the timer
    initializeTimer({{ round_time }}, () => {
        document.getElementById('wordForm').submit(); // Form submission logic
    });
});

// Three.js setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, 300 / 300, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('3dModelCanvas') });
renderer.setSize(300, 300);

// Add lights
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 10, 7.5);
scene.add(directionalLight);

// Set background color based on dark mode setting in local storage
const setBackgroundColor = () => {
    const darkModeEnabled = localStorage.getItem('darkMode') === 'enabled';
    scene.background = new THREE.Color(darkModeEnabled ? 0x2B2C2E : 0xffffff);
    document.body.style.backgroundColor = darkModeEnabled ? '#2B2C2E' : '#ffffff';
};

// Initial background color
setBackgroundColor();

// Listen for changes in the color scheme
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', setBackgroundColor);

// Listen for changes in the dark mode switch
document.getElementById('darkModeSwitch').addEventListener('change', (event) => {
    if (event.target.checked) {
        localStorage.setItem('darkMode', 'enabled');
    } else {
        localStorage.setItem('darkMode', 'disabled');
    }
    setBackgroundColor();
});

// Set the switch state based on localStorage
if (localStorage.getItem('darkMode') === 'enabled') {
    document.getElementById('darkModeSwitch').checked = true;
}

const loader = new THREE.GLTFLoader();
loader.load('{% static "game/models/stopwatch.glb" %}', function (gltf) {
    const model = gltf.scene;
    scene.add(model);
    model.position.set(0, 0, 3);
    model.scale.set(1, 1, 1);

    // Use the colors inherited from the model
    model.traverse((child) => {
        if (child.isMesh) {
            child.material.color.set(child.material.color); // Keep the original color
        }
    });

    // Animation
    function animate() {
        requestAnimationFrame(animate);
        model.rotation.y += 0.01; // Rotate the model
        renderer.render(scene, camera);
    }
    animate();
}, undefined, function (error) {
    console.error(error);
});

camera.position.z = 5;

// Help button functionality
document.getElementById('helpButton').addEventListener('click', () => {
    document.getElementById('helpModal').style.display = 'block';
});

// Close modal when clicking on the close button or outside the modal
document.querySelector('.close').addEventListener('click', () => {
    document.getElementById('helpModal').style.display = 'none';
});

window.addEventListener('click', (event) => {
    if (event.target == document.getElementById('helpModal')) {
        document.getElementById('helpModal').style.display = 'none';
    }
});