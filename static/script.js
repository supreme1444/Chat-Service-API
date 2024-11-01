DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/static/styles.css">
    <title>Chat Application</title>
</head>
<body>
    <div class="container">
        <h1>Регистрация</h1>
        <div id="registration-message" class="message-box"></div>
        <input type="text" id="reg-username" placeholder="Введите имя пользователя" required>
        <input type="password" id="reg-password" placeholder="Введите пароль" required>
        <button id="registerButton">Зарегистрироваться</button>

        <h1>Авторизация</h1>
        <div id="login-message" class="message-box"></div>
        <input type="text" id="login-username" placeholder="Введите имя пользователя" required>
        <input type="password" id="login-password" placeholder="Введите пароль" required>
        <button id="loginButton">Войти</button>

        <div id="chat-section" class="hidden">
            <h2>Чат</h2>
            <input type="text" id="recipient" placeholder="Имя получателя" required>
            <textarea id="message" placeholder="Введите ваше сообщение..." required></textarea>
            <button id="sendMessage">Отправить сообщение</button>
            <div id="messages" class="messages"></div>
        </div>
    </div>
    <script src="/static/script.js"></script>
</body>
</html>
