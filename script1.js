const neonTextInput = document.getElementById('neon-text');
const neonTextDisplay = document.querySelector('.neon-text');
const fontButtons = document.querySelectorAll('.font-button');
const toggleSwitch = document.querySelector('.toggle-switch');

neonTextInput.addEventListener('input', function() {
    neonTextDisplay.textContent = this.value;
});

fontButtons.forEach(button => {
    button.addEventListener('click', function() {
        fontButtons.forEach(btn => btn.classList.remove('active'));
        this.classList.add('active');
    });
});

toggleSwitch.addEventListener('click', function() {
    this.classList.toggle('active');
});