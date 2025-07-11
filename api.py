from flask import Flask, request, jsonify
from youtube import get_music_info
from misc import generate_otp, create_jwt
import misc
from db import *
import jwt
from flask_socketio import SocketIO, emit, join_room, leave_room
import db
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins=os.getenv('CORS_ALLOWED_ORIGINS', '*'))


@app.route('/')
def home():
    return 'Welcome to the PartyAux API!'

@app.get('/search/<query>')
def search(query):
    return jsonify(get_music_info(query))

@app.post('/send-otp')
def send_otp():
    email = request.json.get('email')
    otp = generate_otp()
    misc.send_otp(email, otp)
    store_otp(email, otp)
    return jsonify({"message": "OTP sent successfully"}), 200

@app.post('/login')
def login():
    email = request.json.get('email')
    otp = request.json.get('otp')
    if verify_otp(email, otp):
        return jsonify({"message": "OTP verified successfully", "jwt": create_jwt(email)}), 200
    else:
        return jsonify({"message": "Invalid OTP"}), 400

@app.post('/exists')
def exists():
    user_jwt = request.json.get('jwt')
    if user_jwt:
        try:
            email = jwt.decode(user_jwt, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
        except jwt.InvalidTokenError:
            return jsonify({"authenticated": False}), 200
    else:
        return jsonify({"authenticated": False}), 200
    if find_email(email):
        return jsonify({"exists": True}), 200
    else:
        return jsonify({"exists": False}), 200

@app.post('/create-signup')
def signup():
    user_jwt = request.json.get('jwt')
    username = request.json.get('username')
    if user_jwt:
        try:
            email = jwt.decode(user_jwt, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
        except jwt.InvalidTokenError:
            return jsonify({"authenticated": False}), 200
    else:
        return jsonify({"authenticated": False}), 200
    
    if find_email(email):
        return jsonify({"status": "User already exists"}), 200
    
    if find_username(username):
        return jsonify({"status": "Username already exists"}), 200
    
    if create_account(email, username):
        return jsonify({"status": "Account created successfully"}), 200
    else:
        return jsonify({"status": "Account creation failed"}), 200

@app.post('/create-room')
def create_room_route():
    user_jwt = request.json.get('jwt')
    if user_jwt:
        try:
            email = jwt.decode(user_jwt, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
        except jwt.InvalidTokenError:
            return jsonify({"authenticated": False}), 200
    else:
        return jsonify({"authenticated": False}), 200
    
    code = create_room(email)
    if code:
        return jsonify({"status": "Room created successfully", "code": code}), 200
    else:
        return jsonify({"status": "Room creation failed"}), 200

@app.post('/add-song-to-queue')
def add_song_to_queue():
    room = request.json.get('room')
    song = request.json.get('song')
    jwt_token = request.json.get('jwt')
    email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    if db.add_song_to_queue(room, song, email):
        socketio.emit('add_song', {'song': song}, room=room)
        return jsonify({"status": "Song added to queue"}), 200
    else:
        return jsonify({"status": "Song addition failed"}), 200

@app.post('/remove-song-from-queue')
def remove_song_from_queue():
    room = request.json.get('room')
    song = request.json.get('song')
    jwt_token = request.json.get('jwt')
    email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    if db.remove_song_from_queue(room, song, email):
        socketio.emit('remove_song', {'song': song}, room=room)
        return jsonify({"status": "Song removed from queue"}), 200
    else:
        return jsonify({"status": "Song removal failed"}), 200

@app.post('/next-song')
def next_song():
    room = request.json.get('room')
    if db.next_song(room):
        socketio.emit('delete_head_song', {}, room=room)
        socketio.emit('current_song', {"song": db.get_current_song(room)}, room=room)
        return jsonify({"status": "Song skipped"}), 200
    else:
        return jsonify({"status": "Song skipping failed"}), 200

@app.post('/get-queue')
def get_queue():
    room = request.json.get('room')
    jwt_token = request.json.get('jwt')
    email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    if db.get_queue(room, email):
        return jsonify({"status": "Queue retrieved"}), 200
    else:
        return jsonify({"status": "Queue retrieval failed"}), 200

@app.post('/get-current-song')
def get_current_song():
    room = request.json.get('room')
    jwt_token = request.json.get('jwt')
    email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    if db.get_current_song(room, email):
        return jsonify({"status": "Current song retrieved"}), 200
    else:
        return jsonify({"status": "Current song retrieval failed"}), 200

@app.post('/add-downvote')
def add_downvote():
    room = request.json.get('room')
    song = request.json.get('song')
    jwt_token = request.json.get('jwt')
    email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    downvotes = db.add_downvote(room, song, email)
    if downvotes != -1:
        socketio.emit('downvote', {'song': song, 'downvotes': downvotes}, room=room)
        return jsonify({"status": "Downvote added"}), 200
    else:
        return jsonify({"status": "Downvote addition failed"}), 200



@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    


@socketio.on('join_room')
def handle_join_room(data):
    room = data['room']
    jwt_token = data['jwt']
    email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    if db.join_room(room, email):
        join_room(room)
        emit('server_message', {'message': f'Joined room {room}'}, to=request.sid)
    else:
        emit('server_message', {'message': f'You are not in room {room}'}, to=request.sid)

@socketio.on('leave_room')
def handle_leave_room(data):
    jwt_token = data['jwt']
    email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    room = get_room_by_email(email)["code"]
    if db.leave_room(email):
        leave_room(room)
        emit('server_message', {'message': f'Left room {room}'}, to=request.sid)
    else:
        emit('server_message', {'message': f'You are not in room {room}'}, to=request.sid)





if __name__ == '__main__':
    socketio.run(
        app, 
        debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true',
        port=int(os.getenv('FLASK_PORT', '5000')),
        host=os.getenv('FLASK_HOST', '0.0.0.0')
    )
