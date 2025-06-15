function sendMessage() {
    let messageInput = document.getElementById('message-input');
    let message = messageInput.value.trim();
    if (!message) return;

    displayMessage('user', message);

    let functionSelect = document.getElementById('function-select');
    let selectedFunction = functionSelect.value;
    let xhr = new XMLHttpRequest();
    let url = '/' + selectedFunction;

    // Show loading indicator
    document.getElementById('loading-indicator').style.display = 'block';

    xhr.open('POST', url);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        document.getElementById('loading-indicator').style.display = 'none';
        if (xhr.status === 200) {
            let response = JSON.parse(xhr.responseText);
            displayMessage('assistant', response.message);
        } else {
            displayMessage('assistant', "❌ Sorry, something went wrong. Try again.");
        }
    };
    xhr.onerror = function() {
        document.getElementById('loading-indicator').style.display = 'none';
        displayMessage('assistant', "❌ Error connecting to the server.");
    };
    xhr.send(JSON.stringify({ message: message }));

    messageInput.value = '';
}

function displayMessage(sender, message) {
    let chatContainer = document.getElementById('chat-container');
    let messageDiv = document.createElement('div');

    messageDiv.classList.add(sender === 'assistant' ? 'assistant-message' : 'user-message');
    messageDiv.innerHTML = `<strong>${sender === 'assistant' ? 'NatureBot' : 'User'}:</strong> ${message}`;

    let timestamp = document.createElement('span');
    timestamp.classList.add('timestamp');
    timestamp.innerText = " [" + new Date().toLocaleTimeString() + "]";
    messageDiv.appendChild(timestamp);

    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Event listeners
let sendButton = document.getElementById('send-btn');
sendButton.addEventListener('click', sendMessage);

document.getElementById('message-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') sendMessage();
});

document.getElementById('clear-btn').addEventListener('click', function () {
    document.getElementById('chat-container').innerHTML = '';
});
