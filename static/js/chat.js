function displayingMessage() {// отображение сообщений и формы вывода
    var roomName = [roomName1, roomName2];
    var fromChatId = '{{ request.user.username }}';
    var toChatId = '{{ user.username }}';

    for (i = 0; i < roomName.length; i++) {
        var chatSocket = new ReconnectingWebSocket(
            'ws://' + window.location.host +
            '/ws/chat/' + roomName[i] + '/');
        chatSocket.onopen = function (e) {
            fetchMessages();
        }

        chatSocket.onmessage = function (e) {
            var data = JSON.parse(e.data);
            if (data['command'] === 'messages') {
                for (let i = 0; i < data['messages'].length; i++) {
                    createMessage(data['messages'][i]);
                }
            } else if (data['command'] === 'new_message') {
                createMessage(data['message']);
            }
        }

        document.querySelector('#chat-message-input').focus();

        document.querySelector('#chat-message-input').onkeyup = function (e) {
            if (e.keyCode === 13) {  // enter, return
                document.querySelector('#chat-message-submit').click();
            }
        };

        document.querySelector('#chat-message-submit').onclick = function (e) {
            var messageInputDom = document.querySelector('#chat-message-input');
            var message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'command': 'new_message',
                'message': message,
                'fromSender': fromChatId,
                'toRecipient': toChatId
            }));
            messageInputDom.value = '';
        };

        function fetchMessages() {
            chatSocket.send(JSON.stringify({ 'command': 'fetch_messages' }));
        }
    }

    function createMessage(data) {
        var sender = data['sender'];
        var msgListTag = document.createElement('li');
        var imgTag = document.createElement('img');
        var pTag = document.createElement('p');
        pTag.textContent = data.message;
        imgTag.className = 'circle';
        if (sender === fromChatId) {
            msgListTag.className = 'sent';
            imgTag.src = '{{ request.user.photo.url }}';
        } else {
            msgListTag.className = 'replies';
            imgTag.src = '{{ user.photo.url }}';
        }
        msgListTag.appendChild(imgTag);
        msgListTag.appendChild(pTag);
        document.querySelector('#messages').appendChild(msgListTag);
    }
}

hash = window.location.hash

function displayingForm() { // Функция добавления формы
    $('#current_user_data').empty()
    $('#' + id).clone().appendTo("#current_user_data")
    $('#box, .title').show()
    // Обновления названия чатов
    if (document.getElementById(id).parentNode.hash === window.location.hash) {
        space = hash.indexOf('_');
        roomName1 = hash.slice(2, -1)
        roomName2 = hash.slice(space + 1, -1) + hash.slice(space, space + 1) + hash.slice(2, space)
        recipient = hash.slice(space + 1, -1)
        console.log('displayingFrom', roomName1, roomName2)
    }
    displayingMessage() // Вывод сообщений
}

function selectingForm() { // Функция выбора получателя из списка
    $("#to_user .row a").click(function (event) {
        id = (event.target.id)
        if (document.getElementById(id).parentNode.hash != window.location.hash) {
            space = this.hash.indexOf('_');
            roomName1 = this.hash.slice(2, -1)
            roomName2 = this.hash.slice(space + 1, -1) + this.hash.slice(space, space + 1) + this.hash.slice(2, space)
            recipient = this.hash.slice(space + 1, -1)
            console.log('selectingForm', roomName1, roomName2)
            $('#messages li').remove()
            displayingForm()
        }
    });
}
if (hash === window.location.hash && hash != '') { // Если есть хэш
    console.log('Есть хэштег')
    start = hash.indexOf('_') + 1;
    hash_username = (hash.slice(start, -1))
    id = "to_" + hash_username + "_data"
    displayingForm() // Отображение формы
    selectingForm() // Выбор нового получателя
} else { //
    console.log('Хэштега нет')
    selectingForm() // Выбор получателя из списка
}