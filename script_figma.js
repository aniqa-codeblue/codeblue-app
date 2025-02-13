const textInput = document.getElementById('text-input');
const textError = document.getElementById('text-error');
const doneButton = document.getElementById('done-button');

doneButton.addEventListener('click', () => {
    if (textInput.validity.valid) {
        //Here you would handle updating the preview and price
        textError.textContent = "";
    } else {
        textError.textContent = "Please enter at least 3 characters.";
    }
});

textInput.addEventListener('input', () => {
    if (textInput.validity.valid) {
        textError.textContent = "";
    }
});