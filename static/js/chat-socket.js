function handleFileSelectMulti(evt) {
    var files = evt.target.files;
    document.getElementById('preview_image').innerHTML = "";
    for (var i = 0, f; f = files[i]; i++) {
        var reader = new FileReader();

        reader.onload = (function (theFile) {
            return function (e) {
                var span = document.createElement('span');
                span.innerHTML = ['<img id="', escape(theFile.name),
                    '" class="img-thumbnail" src="', e.target.result, '">'].join('');
                document.getElementById('preview_image').insertBefore(span, null);
            };
        })(f);
        reader.readAsDataURL(f);
    }
}

document.getElementById('chat_photo_input').addEventListener('change', handleFileSelectMulti, false);

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            var csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var roomName;

function sendMessage(chatSocket, imgId) {
    var messageInputDom = document.querySelector('#chat_message_input');
    var message = messageInputDom.value;
    if (document.querySelector('#chat_message_input').value != '' || document.querySelector('#chat_photo_input').value != '') {
        chatSocket.send(JSON.stringify({
            'command': 'new_message',
            'message': message,
            'fromSender': fromChatId,
            'toRecipient': id,
            'imgId': imgId,
        }));
    }
    messageInputDom.value = '';
    $('#chat_photo_input').val('');
    $('#messagebox_container #preview_image').empty();
}

function displayingMessage() {
    roomName = [roomName1, roomName2]
    for (i = 0; i < roomName.length; i++) {
        var chatSocket = new ReconnectingWebSocket(
            'ws://' + window.location.host +
            '/wss/chat/' + roomName[i] + '/');
        chatSocket.onopen = function (e) {
            fetchMessages();
        }

        document.querySelector('#smile_list').onclick = function (e) {
            var smile = e.target.id;
            chatSocket.send(JSON.stringify({
                'command': 'new_message',
                'fromSender': fromChatId,
                'toRecipient': id,
                'smileId': smile,
            }));
        };

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
        
        chatSocket.onclose = function (e) {
            $('#messages').empty()
        };

        document.querySelector('#chat_message_input').focus();

        document.querySelector('#chat_message_input').onkeyup = function (e) {
            if (e.keyCode === 13) {
                document.querySelector('#chat_submit').click();
            }
        };

        document.querySelector('#chat_submit').onclick = function (e) {
            e.stopPropagation();
            e.preventDefault()
            var files = $('#chat_photo_input')[0].files[0];
            if (files) {
                var fd = new FormData();
                fd.append('img', files);
                $.ajax({
                    url: uploadImageUrl,
                    type: "POST",
                    cache: false,
                    processData: false,
                    contentType: false,
                    data: fd,
                    success: function (data) {
                        sendMessage(chatSocket, data.id);
                    }
                });
            } else {
                sendMessage(chatSocket);
            }
        };

        function fetchMessages() {
            chatSocket.send(JSON.stringify({ 'command': 'fetch_messages' }));
            $('#messages').empty();
        }
    }

    function createMessage(data) {
        var sender = data['sender'];
        var msgListTag = document.createElement('li');
        var imgTag = document.createElement('img');
        var pTag = document.createElement('p');
        var spanTag = document.createElement('span');
        spanTag.textContent = data.message;
        if (data.img) {
            var file = document.createElement("img");
            file.setAttribute('src', data.img)
            file.setAttribute('class', 'message-img')
            if (data.message) {
            }
            pTag.appendChild(file)
        }
        if (data.smile) {
            var file = document.createElement("img");
            file.setAttribute('src', data.smile)
            file.setAttribute('class', 'smile')
            pTag.appendChild(file)
        }
        imgTag.className = 'circle';
        if (sender === fromChatId) {
            msgListTag.className = 'sent';
            imgTag.src = senderImage;
        } else {
            msgListTag.className = 'replies';
            imgTag.src = $('.title .circle').attr("src");
        }
        pTag.appendChild(spanTag)
        msgListTag.appendChild(imgTag);
        msgListTag.appendChild(pTag);
        document.querySelector('#messages').appendChild(msgListTag);
        $('#messages').scrollTop(9999)
    }
}

hash = window.location.hash

function displayingForm() {
    $('#current_user_data').empty()
    $('#' + id).clone().appendTo("#current_user_data")
    $('#box, .title').show()
    hash = $('#' + id).parent('a').attr('href')
    if (hash === window.location.hash) {
        space = hash.indexOf('_');
        recipient = hash.slice(space + 1, -1)
        roomName1 = fromChatId + '_' + recipient
        roomName2 = recipient + '_' + fromChatId
    }
    displayingMessage()
}

function selectingForm() {
    $("#recipient .row a").click(function (event) {
        id = (event.target.id)
        if ($('#' + id).parent('a').attr('href') != window.location.hash) {
            space = this.hash.indexOf('_');
            recipient = this.hash.slice(space + 1, -1)
            roomName1 = fromChatId + '_' + recipient
            roomName2 = recipient + '_' + fromChatId
            $('#messages').empty()
            displayingForm()
        }
    });
}

function visibleList() {
    if (window.outerWidth < 768) {
        $('#user_list').show()
        $('#messagebox_container').hide()
    }
}

function visibleMessageBox() {
    if (window.outerWidth < 768) {
        $('#user_list').hide()
        $('#messagebox_container').show()
    }
}

$(window).bind('hashchange', function () {
    if (location.hash != '') {
        $('#box, .title').show()
        visibleMessageBox()
    } else {
        $('.title, #box').hide()
        visibleList()
    } 
});

if (window.location.hash != '') {
    start = hash.indexOf('_') + 1;
    id = (hash.slice(start, -1))
    displayingForm()
    selectingForm()
    visibleMessageBox()
} else {
    selectingForm()
    visibleList()
}
