let keybindInput = document.getElementById('keybind-input');
let keybind = '';

keybindInput.addEventListener('keydown', (event) => {
    event.preventDefault();
    let keys = [];
    if (event.ctrlKey) keys.push('Ctrl');
    if (event.altKey) keys.push('Alt');
    if (event.shiftKey) keys.push('Shift');
    if (event.metaKey) keys.push('Meta');
    if (!['Control', 'Alt', 'Shift', 'Meta'].includes(event.key)) keys.push(event.key);

    keybind = keys.join('+');
    keybindInput.value = keybind;
});

document.getElementById('save-keybind').addEventListener('click', () => {
    if (keybind) {
        localStorage.setItem('customKeybind', keybind);
        alert(`Keybind ${keybind} saved!`);
    }
});

document.addEventListener('keydown', (event) => {
    if (document.activeElement === keybindInput) {
        event.preventDefault();
    }
});

document.addEventListener('keydown', (event) => {
    const customKeybind = localStorage.getItem('customKeybind');
    if (customKeybind) {
        const keys = customKeybind.split('+');
        if (keys.every(key => {
            if (key === 'Ctrl') return event.ctrlKey;
            if (key === 'Alt') return event.altKey;
            if (key === 'Shift') return event.shiftKey;
            if (key === 'Meta') return event.metaKey;
            return event.key.toLowerCase() === key.toLowerCase();
        })) {
            event.preventDefault();
            alert(`Custom action triggered by ${customKeybind}!`);
        }
    }
});