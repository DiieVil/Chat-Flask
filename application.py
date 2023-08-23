import os

from datetime import datetime
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_session import Session
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.config["SESSION_PERMANENT"]= False
app.config["SESSION_TYPE"] = "filesystem"
socketio = SocketIO(app)
Session(app)


# Variables globales

chatlist=[]
usernames = []
messagedict={}
chatActual=0


# Ruta inicial 
@app.route("/")
def index():
    # Código aquí
    #print('PASO INDEX')
    return render_template("index.html")



# Para salir de la aplicación
@app.route("/logout", methods=["GET"])
def logout():

    global usernames
    #print('PASO LOGOUT')
    del usernames[-1]
    #print(usernames)

    return redirect(url_for('index'))



# Muestra la lista de canales creados y añade a un usuario (si no existe) que se acaba de registrar
# con el formulario index.html 
@app.route("/chatrooms", methods=["GET", "POST"])
def chatroomlist():

    global usernames
    global chatlist

    if request.method == "GET":
        #print('1')

        if session["user_name"] not in usernames:
            return render_template("error.html", error_message="Tiene que registrarse primero")

        else:
            return render_template("chatlist.html", usuario = session["user_name"], chats=chatlist)
    
    else:
        session["user_name"] = request.form.get("user_name")

        if session["user_name"] == "":
            #print('PASO 2')
            return render_template("error.html", error_message="No se ha introducido ningún nombre de usuario ")
        
        if len(usernames) == 0:
            usernames.append(session["user_name"])
            #print('PASO 3')
            return render_template("chatlist.html", usuario = session["user_name"], chats=chatlist)

        else:
            
            if session["user_name"] in usernames:
                    # YA ESTAS REGISTRADO
                #print('PASO 4')
                return render_template("error.html", error_message="El usuario ya existe")

            else:
                # Registro de usuario
                usernames.append(session["user_name"])
                #print('PASO 5')
                return render_template("chatlist.html", usuario =session["user_name"], chats=chatlist)



@app.route("/chatrooms/<int:chat_id>", methods=["GET","POST"])
def chatroom(chat_id):
    
    global usernames
    global chatlist
    global chatActual

    
    #chat_name = request.form.get("chatroom_name")

    if request.method == "POST":
        #print('PASO 6')
        if chatActual == '':
            print('Error1')
            return render_template("error.html", error_message="No se ha introducido ningun canal")

        if chatActual in chatlist:
            print('Error2')
            return render_template("error.html", error_message="El canal ya existe")
        
        else:
            session["chat_id"]=chat_id
            chatlist.append(chatActual)
            messagedict[chatActual]=[]
            return render_template("chatroom.html", usuario =session["user_name"],chats=chatlist)
    
    if request.method == "GET":
        #print('PASO 7')
        session["chat_id"]=chat_id
        print('CHAT ID GET',session["chat_id"])
        return render_template("chatroom.html", usuario = session["user_name"],chats=chatlist)



@socketio.on("envio canal")
def creaCanal(data):
    global chatlist
    global messagedict
    global chatActual

    #print('8')
    chatActual= data['selection']

    emit('tratar canal', {"selection": data['selection'], "chat_id":
        len(chatlist) + 1}, broadcast=True)

    
@socketio.on("envio msj")
def enviaMsg(data):
    global usernames
    global messagedict
    global chatlist

    usuario = usernames[-1]

    time = datetime.now().strftime("%Y-%m-%d %H:%M")
    response_dict= {"selection":data["selection"],
        "time" : time,
        "user_name" : usuario,
    }

    emit("tratar msj", {**response_dict, **{"chat_id":
        str(session["chat_id"])}}, broadcast = True)


    messagedict[chatlist[session["chat_id"]-1]].append(response_dict)
    


@app.route("/ver_mensajes", methods=["GET","POST"])
def ver_mensajes():
    global messagedict
    global chatlist

    return jsonify({**{"message":
        messagedict[chatlist[session["chat_id"]-1]]}, **{"chat_id":
        session["chat_id"]}})
    

if __name__ == "__main__":
    app.run(debug=True)