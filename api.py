from flask import Flask, request, jsonify
from youtube import get_music_info, get_search_suggestion
from misc import generate_otp, create_jwt
import misc
import db
import jwt
from flask_socketio import SocketIO, emit, join_room, leave_room
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

@app.get('/search/suggestions/<query>')
def search_suggestions(query):
    return jsonify({"input": query, "suggestions": get_search_suggestion(query)})

@app.post('/send-otp')
def send_otp():
    if not request.json:
        return jsonify({"message": "No JSON data provided"}), 400
    email = request.json.get('email')
    otp = generate_otp()
    misc.send_otp(email, otp)
    db.store_otp(email, otp)
    return jsonify({"message": "OTP sent successfully"}), 200

@app.post('/login')
def login():
    if not request.json:
        return jsonify({"message": "No JSON data provided"}), 400
    email = request.json.get('email')
    otp = request.json.get('otp')
    if db.verify_otp(email, otp):
        return jsonify({"message": "OTP verified successfully", "jwt": create_jwt(email)}), 200
    else:
        return jsonify({"message": "Invalid OTP"}), 400

@app.post('/exists')
def exists():
    if not request.json:
        return jsonify({"authenticated": False}), 200
    user_jwt = request.json.get('jwt')
    if user_jwt:
        try:
            email = jwt.decode(user_jwt, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
        except jwt.InvalidTokenError:
            return jsonify({"authenticated": False}), 200
    else:
        return jsonify({"authenticated": False}), 200
    if db.find_email(email):
        return jsonify({"exists": True}), 200
    else:
        return jsonify({"exists": False}), 200

@app.post('/create-signup')
def signup():
    if not request.json:
        return jsonify({"message": "No JSON data provided"}), 400
    user_jwt = request.json.get('jwt')
    username = request.json.get('username')
    if user_jwt:
        try:
            email = jwt.decode(user_jwt, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
        except jwt.InvalidTokenError:
            return jsonify({"authenticated": False}), 200
    else:
        return jsonify({"authenticated": False}), 200
    
    if db.find_email(email):
        return jsonify({"status": "User already exists"}), 200
    
    if db.find_username(username):
        return jsonify({"status": "Username already exists"}), 200
    
    if db.create_account(email, username):
        return jsonify({"status": "Account created successfully"}), 200
    else:
        return jsonify({"status": "Account creation failed"}), 200

@app.post('/create-room')
def create_room_route():
    if not request.json:
        return jsonify({"message": "No JSON data provided"}), 400
    user_jwt = request.json.get('jwt')
    if user_jwt:
        try:
            email = jwt.decode(user_jwt, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
        except jwt.InvalidTokenError:
            return jsonify({"authenticated": False}), 200
    else:
        return jsonify({"authenticated": False}), 200
    max_downvotes = request.json.get('max_downvotes')
    code = db.create_room(email, max_downvotes)
    if code:
        return jsonify({"status": "Room created successfully", "code": code}), 200
    else:
        return jsonify({"status": "Room creation failed"}), 200

@app.post('/add-song-to-queue')
def add_song_to_queue():
    if not request.json:
        return jsonify({"message": "No JSON data provided"}), 400
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
    if not request.json:
        return jsonify({"message": "No JSON data provided"}), 400
    room = request.json.get('room')
    song_uuid = request.json.get('song_uuid')
    jwt_token = request.json.get('jwt')
    
    if not jwt_token:
        return jsonify({"message": "JWT token required"}), 401
    
    try:
        email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid JWT token"}), 401
    
    if not room:
        return jsonify({"message": "Room code required"}), 400
    
    if not song_uuid:
        return jsonify({"message": "Song UUID required"}), 400
    
    if db.remove_song_from_queue(room, song_uuid, email):
        socketio.emit('remove_song', {'song': song_uuid}, room=room)
        return jsonify({"status": "Song removed from queue"}), 200
    else:
        return jsonify({"status": "Song removal failed"}), 200

@app.post('/next-song')
def next_song():
    if not request.json:
        return jsonify({"message": "No JSON data provided"}), 400
    room = request.json.get('room')
    jwt_token = request.json.get('jwt')
    email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    if not email:
        return jsonify({"status": "User not authenticated"}), 401
    if db.next_song(room, email):
        socketio.emit('delete_head_song', {}, room=room)
        room_data = db.get_room_by_code(room)
        if room_data:
            current_song = room_data.get("current_song", {})
            socketio.emit('current_song', {"song": current_song}, room=room)
        return jsonify({"status": "Song skipped"}), 200
    else:
        return jsonify({"status": "Song skipping failed"}), 200

@app.post('/get-queue')
def get_queue():
    if not request.json:
        return jsonify({"message": "No JSON data provided"}), 400
    room = request.json.get('room')
    jwt_token = request.json.get('jwt')
    email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    queue = db.get_queue(room, email)
    if queue is not False:
        return jsonify({"status": "Queue retrieved", "queue": queue}), 200
    else:
        return jsonify({"status": "Queue retrieval failed"}), 200

@app.post('/get-current-song')
def get_current_song():
    if not request.json:
        return jsonify({"message": "No JSON data provided"}), 400
    room = request.json.get('room')
    jwt_token = request.json.get('jwt')
    email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    current_song = db.get_current_song(room, email)
    if current_song is not False and current_song is not None:
        return jsonify({"status": "Current song retrieved", "song": current_song}), 200
    else:
        return jsonify({"status": "Current song retrieval failed"}), 200

@app.post('/add-downvote')
def add_downvote():
    if not request.json:
        return jsonify({"message": "No JSON data provided"}), 400
    room = request.json.get('room')
    song_uuid = request.json.get('song_uuid')
    jwt_token = request.json.get('jwt')
    
    if not jwt_token:
        return jsonify({"message": "JWT token required"}), 401
    
    try:
        email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid JWT token"}), 401
    
    if not room:
        return jsonify({"message": "Room code required"}), 400
    
    if not song_uuid:
        return jsonify({"message": "Song UUID required"}), 400
    
    downvotes = db.add_downvote(room, song_uuid, email, socketio)
    if downvotes != -1:
        socketio.emit('downvote', {'song': song_uuid, 'downvotes': downvotes}, room=room)
        return jsonify({"status": "Downvote added", "downvotes": downvotes}), 200
    else:
        return jsonify({"status": "Downvote addition failed"}), 200

@app.post('/get-room-info')
def get_room_info():
    if not request.json:
        return jsonify({"message": "No JSON data provided"}), 400
    room = request.json.get('room')
    jwt_token = request.json.get('jwt')
    email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    room_info = db.get_room_info(room, email)
    if room_info is not None:
        return jsonify({"status": "Room info retrieved", "room_info": room_info}), 200
    else:
        return jsonify({"status": "Room info retrieval failed"}), 200
    

@app.post('/change-max-downvotes')
def change_max_downvotes():
    if not request.json:
        return jsonify({"message": "No JSON data provided"}), 400
    room = request.json.get('room')
    max_downvotes = request.json.get('max_downvotes')
    jwt_token = request.json.get('jwt')
    email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    if db.change_max_downvotes(room, max_downvotes, email):
        return jsonify({"status": "Max downvotes changed"}), 200
    else:
        return jsonify({"status": "Max downvotes change failed"}), 200

@app.post('/create-playlist')
def create_playlist():
    if not request.json:
        return jsonify({"message": "No JSON data provided"}), 400
    jwt_token = request.json.get('jwt')
    name = request.json.get('name')
    
    if not jwt_token:
        return jsonify({"message": "JWT token required"}), 401
    
    try:
        email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid JWT token"}), 401
    
    if not name:
        return jsonify({"message": "Playlist name required"}), 400
    
    playlist_id = db.create_playlist(name, email)
    if playlist_id:
        return jsonify({"status": "Playlist created successfully", "playlist_id": str(playlist_id)}), 200
    else:
        return jsonify({"status": "Playlist creation failed"}), 500

@app.post('/get-playlist-info')
def get_playlist_info():
    if not request.json:
        return jsonify({"message": "No JSON data provided"}), 400
    jwt_token = request.json.get('jwt')
    playlist_id = request.json.get('playlist_id')
    
    if not jwt_token:
        return jsonify({"message": "JWT token required"}), 401
    
    try:
        email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid JWT token"}), 401
    
    if not playlist_id:
        return jsonify({"message": "Playlist ID required"}), 400
    
    playlist_info = db.get_playlist_info(playlist_id)
    if playlist_info:
        # Convert UUID to string for JSON serialization
        playlist_info = dict(playlist_info)
        playlist_info['playlist_id'] = str(playlist_info['playlist_id'])
        playlist_info['_id'] = str(playlist_info['_id'])
        
        # Check if user has access to this playlist
        if playlist_info['owner'] == email or playlist_info['public']:
            return jsonify({"status": "Playlist info retrieved", "playlist": playlist_info}), 200
        else:
            return jsonify({"message": "Access denied"}), 403
    else:
        return jsonify({"message": "Playlist not found"}), 404

@app.post('/get-user-playlists')
def get_user_playlists():
    if not request.json:
        return jsonify({"message": "No JSON data provided"}), 400
    jwt_token = request.json.get('jwt')
    
    if not jwt_token:
        return jsonify({"message": "JWT token required"}), 401
    
    try:
        email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid JWT token"}), 401
    
    playlist_ids = db.get_user_playlists(email)
    return jsonify({"status": "User playlists retrieved", "playlist_ids": playlist_ids}), 200

@app.post('/update-playlist')
def update_playlist():
    if not request.json:
        return jsonify({"message": "No JSON data provided"}), 400
    jwt_token = request.json.get('jwt')
    playlist_id = request.json.get('playlist_id')
    songs = request.json.get('songs')
    
    if not jwt_token:
        return jsonify({"message": "JWT token required"}), 401
    
    try:
        email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid JWT token"}), 401
    
    if not playlist_id:
        return jsonify({"message": "Playlist ID required"}), 400
    
    if songs is None:
        return jsonify({"message": "Songs array required"}), 400
    
    if db.update_playlist(email, playlist_id, songs):
        return jsonify({"status": "Playlist updated successfully"}), 200
    else:
        return jsonify({"status": "Playlist update failed"}), 500

@app.post('/change-playlist-visibility')
def change_playlist_visibility():
    if not request.json:
        return jsonify({"message": "No JSON data provided"}), 400
    jwt_token = request.json.get('jwt')
    playlist_id = request.json.get('playlist_id')
    public = request.json.get('public')
    
    if not jwt_token:
        return jsonify({"message": "JWT token required"}), 401
    
    try:
        email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid JWT token"}), 401
    
    if not playlist_id:
        return jsonify({"message": "Playlist ID required"}), 400
    
    if public is None:
        return jsonify({"message": "Public visibility flag required"}), 400
    
    if db.change_playlist_visibility(email, playlist_id, public):
        return jsonify({"status": "Playlist visibility changed successfully"}), 200
    else:
        return jsonify({"status": "Playlist visibility change failed or access denied"}), 403

@app.get('/search-playlist/<playlist_name>')
def search_playlist(playlist_name):
    playlists = db.search_playlist(playlist_name)
    return jsonify({"status": "Playlists retrieved", "playlists": playlists}), 200

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
        emit('someone_joined', {'room': room, 'email': email}, room=room)
    else:
        emit('server_message', {'message': f'You are not in room {room}'}, to=request.sid)

@socketio.on('leave_room')
def handle_leave_room(data):
    jwt_token = data['jwt']
    email = jwt.decode(jwt_token, os.getenv('JWT_SECRET', 'secret'), algorithms=[os.getenv('JWT_ALGORITHM', 'HS256')])["email"]
    room_data = db.get_room_by_email(email)
    if room_data:
        room = room_data["code"]
        if db.leave_room(email):
            leave_room(room)
            emit('server_message', {'message': f'Left room {room}'},to=request.sid)
            emit('someone_left', {'room': room, 'email': email}, room=room)
        else:
            emit('server_message', {'message': f'You are not in room {room}'},to=request.sid)
    else:
        emit('server_message', {'message': 'You are not in any room'},to=request.sid)

