const registerButton = document.getElementById('registerButton');
const loginButton = document.getElementById('loginButton');
const sendMessageButton = document.getElementById('sendMessage');
const refreshMessagesButton = document.getElementById('refreshMessages'); // Новая кнопка

const registrationMessageBox = document.getElementById('registration-message');
const loginMessageBox = document.getElementById('login-message');
const chatSection = document.getElementById('chat-section');
const messagesDiv = document.getElementById('messages');

registerButton.addEventListener('click', async () => {
    console.log("Register button clicked");
    const username = document.getElementById('reg-username').value;
    const password = document.getElementById('reg-password').value;

    const response = await fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    console.log(data); // Отладочное сообщение

    if (response.ok) {
        registrationMessageBox.textContent = data.detail || 'Регистрация успешна!';
        registrationMessageBox.style.backgroundColor = '#28a745'; // Зеленый
    } else {
        registrationMessageBox.textContent = data.detail || 'Ошибка регистрации';
        registrationMessageBox.style.backgroundColor = '#dc3545'; // Красный
    }
});
loginButton.addEventListener('click', async () => {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const response = await fetch('/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ username, password })
    });

    const data = await response.json();
    if (response.ok) {
        localStorage.setItem('token', data.access_token);
        loginMessageBox.textContent = 'Успешная авторизация!';
        loginMessageBox.style.backgroundColor = '#28a745'; // Зеленый
        chatSection.classList.remove('hidden');
    } else {
        loginMessageBox.textContent = data.detail || 'Ошибка авторизации';
        loginMessageBox.style.backgroundColor = '#dc3545'; // Красный
    }
});

sendMessageButton.addEventListener('click', async () => {
    const recipient = document.getElementById('recipient').value;
    const messageContent = document.getElementById('message').value;
    const token = localStorage.getItem('token');

    const response = await fetch('/messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ recipient_username: recipient, content: messageContent })
    });

    if (response.ok) {
        document.getElementById('message').value = ''; // Очистить поле ввода сообщения
        fetchMessageHistory(recipient); // Обновить историю сообщений
    } else {
        alert('Ошибка отправки сообщения');
    }
});

refreshMessagesButton.addEventListener('click', async () => {
    const recipient = document.getElementById('recipient').value; // Получаем имя получателя из поля ввода
    if (recipient) {
        await fetchMessageHistory(recipient); // Вызываем функцию обновления истории сообщений
    } else {
        alert('Пожалуйста, введите имя получателя для обновления истории сообщений.');
    }
});

async function fetchMessageHistory(recipientUsername) {
    const token = localStorage.getItem('token');

    const response = await fetch(`/messages/history/${recipientUsername}`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (response.ok) {
        const messages = await response.json();
        displayMessages(messages);
    } else {
        alert('Ошибка получения истории сообщений');
    }
}
refreshMessagesButton.addEventListener('click', async () => {
    const recipient = document.getElementById('recipient').value; // Получаем имя получателя из поля ввода
    if (recipient) {
        await fetchMessageHistory(recipient); // Вызываем функцию обновления истории сообщений
    } else {
        alert('Пожалуйста, введите имя получателя для обновления истории сообщений.');
    }
});
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

