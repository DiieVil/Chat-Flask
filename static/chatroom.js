document.addEventListener('DOMContentLoaded', () => {  
    const request = new XMLHttpRequest();

    request.open("POST", "/ver_mensajes");

    request.onload = () => {
        
        const data = JSON.parse(request.responseText);
        
        localStorage.setItem("chat_id", data["chat_id"])
        let i;
        for (i = 0; i<data["message"].length; i++) {
            const li = document.createElement(`li`);
            const response = data["message"][i];
            li.innerHTML = `<b>${response["user_name"]}</b>:
                ${response["selection"]}
                <small>${response["time"]}</small>`;
            document.querySelector(`#messages`).append(li);
        }
    };
    request.send();

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);  

    socket.on('connect', () => {
        document.querySelector('button').onclick = function() {
            const selection = document.querySelector('input').value;
            this.form.reset();
            socket.emit('envio msj', {'selection':selection});
        };
    });

    socket.on('tratar msj', data => {
        if (data["chat_id"] === localStorage.chat_id) {
            const li = document.createElement('li');

            li.innerHTML = `<b>${data["user_name"]}</b> :
                ${data["selection"]} ${data["time"]}`;
            document.querySelector(`#messages`).append(li);
        }
    });



    // Al seleccionar un canal, se obtienen los mensajes
    // previos a través de una nueva petición POST con HTTP:
    // Abrir una nueva petición para obtener mensajes previos
    

    // Callback para cuando una petición es completada

    // Conectar al web socket
  
    // Al conectar, configurar el botón
 

    // Cuando se envía el mensaje, añadirlo a la lista 'ul' de chatroom.html


});
