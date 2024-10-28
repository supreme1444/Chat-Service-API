const sendMessageButton = document.getElementById('sendMessage');
const messagesDiv = document.getElementById('messages');

sendMessageButton.addEventListener('click', async () => {
    const recipient = document.getElementById('recipient').value;
    const messageContent = document.getElementById('message').value;

    // Отправка сообщения
    const token = localStorage.getItem('token'); // Получите токен из localStorage

    const response = await fetch('/messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            recipient_username: recipient,
            content: messageContent
        })
    });

    if (response.ok) {
        document.getElementById('message').value = ''; // Очистить поле ввода сообщения
        await fetchMessageHistory(recipient);
    } else {
        alert('Error sending message');
    }
});

async function fetchMessageHistory(recipientUsername) {
    const token = localStorage.getItem('token'); // Получите токен из localStorage

    const response = await fetch(`/messages/history/${recipientUsername}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (response.ok) {
        const messages = await response.json();
        displayMessages(messages);
    } else {
        alert('Error fetching message history');
    }
}

function displayMessages(messages) {
    messagesDiv.innerHTML = ''; // Очистить текущее содержимое

    messages.forEach(message => {
        const messageDiv = document.createElement('div');
        messageDiv.textContent = `${message.timestamp}: ${message.message}`;
        messagesDiv.appendChild(messageDiv);
    });

    // Прокрутить вниз
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}
