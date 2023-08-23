document.addEventListener('DOMContentLoaded', () => {

    // Connectar al  websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // En cuanto se está conectado, se configura el botón
    socket.on("connect", () => {
        document.querySelector('button').onclick = function(){


            const selection = document.querySelector("input").value;
            this.form.reset();
            socket.emit("envio canal", {'selection':selection});

        };
    });

    socket.on("tratar canal", data => {

        const li = document.createElement('li');
        const link = "/chatrooms/" + data['chat_id'];
        li.innerHTML = `<a href=${link}>${data.selection}</a>`;
        document.querySelector('#canales').append(li);
    });
});