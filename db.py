from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timedelta
import misc
from dotenv import load_dotenv
import os
from bson import json_util
import json
from uuid import uuid4


# Load environment variables
load_dotenv()

uri = os.getenv('MONGODB_URI', "mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'), uuidRepresentation='standard')
db = client[os.getenv('DATABASE_NAME', "PartyAux")]
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def create_document(data, collection_name):
    collection = db[collection_name]
    collection.insert_one(data)

def get_document(collection_name, query):
    collection = db[collection_name]
    return collection.find_one(query)

def get_documents(collection_name, query):
    collection = db[collection_name]
    return collection.find(query)

def update_document(collection_name, query, data):
    collection = db[collection_name]
    collection.update_one(query, {"$set": data})

def add_to_array(collection_name, query, data):
    collection = db[collection_name]
    collection.update_one(query, {"$push": data})

def pull_from_array(collection_name, query, data):
    collection = db[collection_name]
    collection.update_one(query, {"$pull": data})

def delete_document(collection_name, query):
    collection = db[collection_name]
    collection.delete_one(query)

def delete_documents(collection_name, query):
    collection = db[collection_name]
    collection.delete_many(query)

def get_all_documents(collection_name):
    collection = db[collection_name]
    return collection.find()


def store_otp(email, otp):
    if get_document("OTP", {"email": email}):
        delete_document("OTP", {"email": email})
    expiration_time = datetime.now() + timedelta(minutes=10)
    create_document({"email": email, "otp": otp, "expiration_time": expiration_time}, "OTP")

def find_email(email):
    return get_document("AccountInfo", {"email": email})

def find_username(username):
    return get_document("AccountInfo", {"username": username})

def get_account_by_id(uid):
    return get_document("AccountInfo", {"_id": uid})

def get_account_by_email(email):
    return get_document("AccountInfo", {"email": email})

def get_username_by_email(email):
    return get_account_by_email(email)["username"]


def verify_otp(email, otp) -> bool:
    otp_document = get_document("OTP", {"email": email})
    if not otp_document:
        return False
    if otp_document["otp"] != otp:
        return False
    if otp_document["expiration_time"] < datetime.now():
        return False
    delete_document("OTP", {"email": email})
    return True

def create_account(email, username):
    create_document({"email": email, "username": username}, "AccountInfo")
    return True

def delete_account(email, otp):
    if not verify_otp(email, otp):
        return False
    leave_room(email)
    delete_document("AccountInfo", {"email": email})
    delete_document("OTP", {"email": email})
    delete_documents("Rooms", {"host": email})
    delete_documents("Playlists", {"owner": email})
    return True

def room_exists(code):
    return get_room_by_code(code)

def create_room(email, max_downvotes):
    code = misc.create_room_code()
    create_document({"code": code, "host": email, "created_at": datetime.now(), "current_song": {}, "queue": [], "users": [], "max_downvotes": max_downvotes, "host_playing_only": True}, "Rooms")
    return code

def get_room_size(code):
    room = get_room_by_code(code)
    return len(room["users"])

def join_room(code, email):
    room = get_room_by_code(code)
    if email in room["users"]:
        return True
    leave_room(email)
    if not room:
        return False
    
    add_to_array("Rooms", {"code": code}, {"users": email})
    return True

def leave_room(email):
    room = get_document("Rooms", {"users": email})
    if not room:
        return False
    pull_from_array("Rooms", {"code": room["code"]}, {"users": email})
    if get_room_size(room["code"]) == 0:
        delete_document("Rooms", {"code": room["code"]})
    elif room["host"] == email:
        update_document("Rooms", {"code": room["code"]}, {"host": room["users"][1]})
    return True

def add_song_to_queue(code, song, email):
    room = get_room_by_code(code)
    if email not in room["users"]:
        return False
    song["added_by"] = get_username_by_email(email)
    song["downvotes"] = []
    song["uuid"] = str(uuid4())
    if room["current_song"] == {}:
        update_document("Rooms", {"code": code}, {"current_song": song})
        return True
    
    if not room:
        return False
    add_to_array("Rooms", {"code": code}, {"queue": song})
    return True

def remove_song_from_queue(code, song_id, email):
    room = get_room_by_code(code)
    if not room:
        return False
    if room["host"] == email:
        pull_from_array("Rooms", {"code": code}, {"queue": {"uuid": song_id}})
        return True
    return False

def next_song(code, email):
    room = get_room_by_code(code)
    if not room:
        return False
    if email not in room["users"]:
        return False
    
    if len(room["queue"]) != 0:
        update_document("Rooms", {"code": code}, {"current_song": room["queue"][0]})
        pull_from_array("Rooms", {"code": code}, {"queue": room["queue"][0]})
    else:
        update_document("Rooms", {"code": code}, {"current_song": {}})
    return True

def get_queue(code, email):
    room = get_room_by_code(code)
    if not room:
        return False
    if email not in room["users"]:
        return False
    return room["queue"]

def get_current_song(code, email):
    room = get_room_by_code(code)
    if not room:
        return False
    if email not in room["users"]:
        return False
    return room["current_song"] 

def get_room_by_code(code):
    return get_document("Rooms", {"code": code})

def get_room_by_email(email):
    return get_document("Rooms", {"users": email})

def add_downvote(code, song_id, email, socketio):
    room = get_room_by_code(code)
    if not room:
        return -1
    if email not in room["users"]:
        return -1
    if room["current_song"].get("uuid") == song_id and email not in room["current_song"].get("downvotes", []):
        add_to_array("Rooms", {"code": code}, {"current_song.downvotes": email})
        # Get updated room to check current downvote count
        room = get_room_by_code(code)
        if len(room["current_song"]["downvotes"]) >= room["max_downvotes"]:
            next_song(code, email)
            room = get_room_by_code(code)
            socketio.emit('current_song', {"song": room["current_song"]}, room=code)
        return len(room["current_song"]["downvotes"])
    for song in room["queue"]:
        if song["uuid"] == song_id and email not in song["downvotes"]:
            add_to_array("Rooms", {"code": code, "queue.uuid": song_id}, {"queue.$.downvotes": email})
            # Get updated room to check current downvote count
            room = get_room_by_code(code)
            # Find the updated song in the queue
            updated_song = next((s for s in room["queue"] if s["uuid"] == song_id), None)
            if updated_song and len(updated_song["downvotes"]) >= room["max_downvotes"]:
                pull_from_array("Rooms", {"code": code}, {"queue": {"uuid": song_id}})
                socketio.emit('delete_song_from_queue', {"uuid": song_id}, room=code)
            return len(updated_song["downvotes"]) if updated_song else 0
    return -1

def get_room_info(code, email):

    room = get_room_by_code(code)
    if not room:
        return None
    if email not in room["users"]:
        return None
    room = json.loads(json_util.dumps(room))
    room["host"] = { "email": room["host"], "username": get_username_by_email(room["host"]) }
    room["users"] = [{"email": user, "username": get_username_by_email(user)} for user in room["users"]]
    return room


def change_max_downvotes(code, max_downvotes, email):
    room = get_room_by_code(code)
    if not room:
        return False
    if email != room["host"]:
        return False
    update_document("Rooms", {"code": code}, {"max_downvotes": max_downvotes})
    return True


def create_playlist(name, email):
    playlist_id = str(uuid4())
    while get_document("Playlists", {"playlist_id": playlist_id}):
        playlist_id = str(uuid4())
    owner_username = get_username_by_email(email)
    create_document({"playlist_id": playlist_id, "name": name, "owner": email, "owner_username": owner_username, "songs": [], "public": False}, "Playlists")
    return playlist_id

def delete_playlist(email, playlist_id):
    playlist = get_playlist_info(playlist_id)
    if not playlist:
        return False
    if email != playlist["owner"]:
        return False
    delete_document("Playlists", {"playlist_id": playlist_id, "owner": email})
    return True

def get_playlist_info(playlist_id):
    return get_document("Playlists", {"playlist_id": playlist_id})

def get_user_playlists(email):
    playlist_ids = get_documents("Playlists", {"owner": email})
    return [playlist["playlist_id"] for playlist in playlist_ids]

def update_playlist(email, playlist_id, songs):
    update_document("Playlists", {"playlist_id": playlist_id, "owner": email}, {"songs": songs})
    return True

def change_playlist_visibility(email, playlist_id, public):
    playlist = get_playlist_info(playlist_id)
    if not playlist:
        return False
    if email != playlist["owner"]:
        return False
    update_document("Playlists", {"playlist_id": playlist_id, "owner": email}, {"public": public})
    return True

def change_host_playing_only(code, host_playing_only, email):
    room = get_room_by_code(code)
    if not room:
        return False
    if email != room["host"]:
        return False
    update_document("Rooms", {"code": code, "host": email}, {"host_playing_only": host_playing_only})
    return True

def search_playlists(query):
   playlist_collection = db["Playlists"]
   pipeline = [
    {
        "$search": {
            "index": "default",   # dynamic index is usually called "default"
            "compound": {
                "must": [
                    {
                        "text": {
                            "query": query,
                            "path": ["name", "owner", "owner_username"]
                        }
                    }
                ],
                "filter": [
                    {
                        "equals": {
                            "path": "public",
                            "value": True
                        }
                    }
                ]
            }
        }
    },
    {
        "$project": {
            "name": 1,
            "owner": 1,
            "owner_username": 1,
            "public": 1,
            "playlist_id": 1
        }
    },
    { "$sort": { "score": -1 } },
    { "$limit": 10 }
]
   playlists = list(playlist_collection.aggregate(pipeline))

   return playlists

# Ensure no module-level code execution
if __name__ == "__main__":
    pass

