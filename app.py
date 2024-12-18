from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

users = {}

@app.route('/')
def home():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    username = users.get(request.sid, "Anonymous")
    print(f"Message from {username}: {msg}")
    send(f"{username}: {msg}", broadcast=True)

@socketio.on('connect')
def handle_connect():
    print("A user connected!")

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in users:
        del users[request.sid]
    print("A user disconnected!")

@socketio.on('set_username')
def handle_set_username(username):
    users[request.sid] = username
    send(f"{username} has joined the chat", broadcast=True)

@socketio.on('add user')
def handle_add_user(username):
    users[request.sid] = username
    print(f"User added: {username}")

if __name__ == '__main__':
    socketio.run(app, debug=True)
