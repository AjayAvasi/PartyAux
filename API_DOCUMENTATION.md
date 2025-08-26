# PartyAux API Documentation

This document provides a comprehensive overview of all API endpoints, their request/response structures, and examples.

## Authentication
Most endpoints require JWT authentication. Include the JWT token in the request body as `jwt`.

---

## Endpoints

### 1. Home
**GET** `/`

Returns a welcome message.

**Response:**
```
Welcome to the PartyAux API!
```

---

### 2. Search Music
**GET** `/search/<query>`

Search for music tracks.

**Parameters:**
- `query` (string): Search term for music

**Response:**
```json
[
  {
    "title": "Song Title",
    "artist": "Artist Name",
    "duration": "3:45",
    "thumbnail": "https://example.com/thumbnail.jpg",
    "video_id": "abc123"
  }
]
```

---

### 3. Search Suggestions
**GET** `/search/suggestions/<query>`

Get search suggestions for a query.

**Parameters:**
- `query` (string): Partial search term

**Response:**
```json
{
  "input": "partial query",
  "suggestions": [
    "suggestion 1",
    "suggestion 2",
    "suggestion 3"
  ]
}
```

---

### 4. Search Playlists
**GET** `/search-playlists/<playlist_name>`

Search for public playlists by name.

**Parameters:**
- `playlist_name` (string): Name or partial name of the playlist to search for

**Response:**
```json
{
  "status": "Playlists retrieved",
  "playlists": [
    {
      "_id": "550e8400-e29b-41d4-a716-446655440000",
      "playlist_id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "My Public Playlist",
      "owner": "user@example.com",
      "public": true,
      "playlist_id": "jlksadkljsadjlkdaslkjasdkljads"
    }
  ]
}
```

---

### 5. Send OTP
**POST** `/send-otp`

Send OTP to user's email for authentication.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "OTP sent successfully"
}
```

---

### 6. Login
**POST** `/login`

Verify OTP and get JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "otp": "123456"
}
```

**Success Response:**
```json
{
  "message": "OTP verified successfully",
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Response:**
```json
{
  "message": "Invalid OTP"
}
```

---

### 7. Check User Exists
**POST** `/exists`

Check if user exists in the system.

**Request Body:**
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "exists": true
}
```

---

### 8. Create Account
**POST** `/create-signup`

Create a new user account.

**Request Body:**
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "username": "johndoe"
}
```

**Success Response:**
```json
{
  "status": "Account created successfully"
}
```

**Error Responses:**
```json
{
  "status": "User already exists"
}
```
```json
{
  "status": "Username already exists"
}
```

---

## Room Management

### 9. Create Room
**POST** `/create-room`

Create a new music room.

**Request Body:**
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "max_downvotes": 3
}
```

**Response:**
```json
{
  "status": "Room created successfully",
  "code": "ABC123"
}
```

---

### 10. Get Room Info
**POST** `/get-room-info`

Get detailed information about a room.

**Request Body:**
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "room": "ABC123"
}
```

**Response:**
```json
{
  "status": "Room info retrieved",
  "room_info": {
    "code": "ABC123",
    "host": {
      "email": "host@example.com",
      "username": "hostuser"
    },
    "users": [
      {
        "email": "user1@example.com",
        "username": "user1"
      },
      {
        "email": "user2@example.com",
        "username": "user2"
      }
    ],
    "current_song": {
      "title": "Current Song",
      "artist": "Artist",
      "uuid": "550e8400-e29b-41d4-a716-446655440000",
      "added_by": "username",
      "downvotes": ["user@example.com"]
    },
    "queue": [
      {
        "title": "Next Song",
        "artist": "Artist",
        "uuid": "550e8400-e29b-41d4-a716-446655440001",
        "added_by": "username",
        "downvotes": []
      }
    ],
    "max_downvotes": 3
  }
}
```

---

### 11. Change Max Downvotes
**POST** `/change-max-downvotes`

Change the maximum downvotes threshold for a room (host only).

**Request Body:**
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "room": "ABC123",
  "max_downvotes": 5
}
```

**Response:**
```json
{
  "status": "Max downvotes changed"
}
```

---

## Queue Management

### 12. Add Song to Queue
**POST** `/add-song-to-queue`

Add a song to the room's queue.

**Request Body:**
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "room": "ABC123",
  "song": {
    "title": "Song Title",
    "artist": "Artist Name",
    "duration": "3:45",
    "thumbnail": "https://example.com/thumbnail.jpg",
    "video_id": "abc123"
  }
}
```

**Response:**
```json
{
  "status": "Song added to queue"
}
```

---

### 13. Remove Song from Queue
**POST** `/remove-song-from-queue`

Remove a song from the queue (host only).

**Request Body:**
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "room": "ABC123",
  "song_uuid": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```json
{
  "status": "Song removed from queue"
}
```

---

### 14. Next Song
**POST** `/next-song`

Skip to the next song in the queue.

**Request Body:**
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "room": "ABC123"
}
```

**Response:**
```json
{
  "status": "Song skipped"
}
```

---

### 15. Get Queue
**POST** `/get-queue`

Get the current queue for a room.

**Request Body:**
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "room": "ABC123"
}
```

**Response:**
```json
{
  "status": "Queue retrieved",
  "queue": [
    {
      "title": "Song Title",
      "artist": "Artist Name",
      "duration": "3:45",
      "thumbnail": "https://example.com/thumbnail.jpg",
      "video_id": "abc123",
      "uuid": "550e8400-e29b-41d4-a716-446655440000",
      "added_by": "username",
      "downvotes": ["user@example.com"]
    }
  ]
}
```

---

### 16. Get Current Song
**POST** `/get-current-song`

Get the currently playing song.

**Request Body:**
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "room": "ABC123"
}
```

**Response:**
```json
{
  "status": "Current song retrieved",
  "song": {
    "title": "Current Song",
    "artist": "Artist",
    "duration": "3:45",
    "thumbnail": "https://example.com/thumbnail.jpg",
    "video_id": "abc123",
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "added_by": "username",
    "downvotes": ["user@example.com"]
  }
}
```

---

### 17. Add Downvote
**POST** `/add-downvote`

Downvote a song (current or in queue).

**Request Body:**
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "room": "ABC123",
  "song_uuid": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```json
{
  "status": "Downvote added",
  "downvotes": 2
}
```

---

## Playlist Management

### 18. Create Playlist
**POST** `/create-playlist`

Create a new playlist.

**Request Body:**
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "name": "My Awesome Playlist"
}
```

**Response:**
```json
{
  "status": "Playlist created successfully",
  "playlist_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

### 19. Get Playlist Info
**POST** `/get-playlist-info`

Get information about a specific playlist.

**Request Body:**
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "playlist_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```json
{
  "status": "Playlist info retrieved",
  "playlist": {
    "_id": "550e8400-e29b-41d4-a716-446655440000",
    "playlist_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "My Awesome Playlist",
    "owner": "user@example.com",
    "public": false,
    "songs": [
      {
        "title": "Song Title",
        "artist": "Artist Name",
        "duration": "3:45",
        "thumbnail": "https://example.com/thumbnail.jpg",
        "video_id": "abc123"
      }
    ]
  }
}
```

---

### 20. Get User Playlists
**POST** `/get-user-playlists`

Get all playlists owned by the authenticated user.

**Request Body:**
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "status": "User playlists retrieved",
  "playlists": [
    {
      "_id": "550e8400-e29b-41d4-a716-446655440000",
      "playlist_id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "My Awesome Playlist",
      "owner": "user@example.com",
      "public": false,
      "songs": []
    },
    {
      "_id": "550e8400-e29b-41d4-a716-446655440001",
      "playlist_id": "550e8400-e29b-41d4-a716-446655440001",
      "name": "Another Playlist",
      "owner": "user@example.com",
      "public": true,
      "songs": []
    }
  ]
}
```

---

### 21. Update Playlist
**POST** `/update-playlist`

Update the songs in a playlist.

**Request Body:**
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "playlist_id": "550e8400-e29b-41d4-a716-446655440000",
  "songs": [
    {
      "title": "Song Title",
      "artist": "Artist Name",
      "duration": "3:45",
      "thumbnail": "https://example.com/thumbnail.jpg",
      "video_id": "abc123"
    },
    {
      "title": "Another Song",
      "artist": "Another Artist",
      "duration": "4:12",
      "thumbnail": "https://example.com/thumbnail2.jpg",
      "video_id": "def456"
    }
  ]
}
```

**Response:**
```json
{
  "status": "Playlist updated successfully"
}
```

---

### 22. Change Playlist Visibility
**POST** `/change-playlist-visibility`

Change whether a playlist is public or private.

**Request Body:**
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "playlist_id": "550e8400-e29b-41d4-a716-446655440000",
  "public": true
}
```

**Response:**
```json
{
  "status": "Playlist visibility changed successfully"
}
```

---

## WebSocket Events

### Client to Server Events

#### Join Room
```json
{
  "room": "ABC123",
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Leave Room
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Server to Client Events

#### Server Message
```json
{
  "message": "Joined room ABC123"
}
```

#### Someone Joined
```json
{
  "room": "ABC123",
  "email": "user@example.com"
}
```

#### Someone Left
```json
{
  "room": "ABC123",
  "email": "user@example.com"
}
```

#### Add Song (when song is added to queue)
```json
{
  "song": {
    "title": "Song Title",
    "artist": "Artist Name",
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "added_by": "username",
    "downvotes": []
  }
}
```

#### Remove Song (when song is removed from queue)
```json
{
  "song": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### Current Song (when current song changes)
```json
{
  "song": {
    "title": "Current Song",
    "artist": "Artist",
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "added_by": "username",
    "downvotes": []
  }
}
```

#### Downvote (when a song receives a downvote)
```json
{
  "song": "550e8400-e29b-41d4-a716-446655440000",
  "downvotes": 2
}
```

#### Delete Song from Queue (when song is auto-removed due to downvotes)
```json
{
  "uuid": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### Delete Head Song (when next song is called)
```json
{}
```

---

## Error Responses

### Common Error Codes

**400 - Bad Request**
```json
{
  "message": "No JSON data provided"
}
```

**401 - Unauthorized**
```json
{
  "message": "JWT token required"
}
```
```json
{
  "message": "Invalid JWT token"
}
```

**403 - Forbidden**
```json
{
  "message": "Access denied"
}
```

**404 - Not Found**
```json
{
  "message": "Playlist not found"
}
```

**500 - Internal Server Error**
```json
{
  "status": "Playlist creation failed"
}
```

---

## Data Types

### Song Object
```json
{
  "title": "string",
  "artist": "string",
  "duration": "string (MM:SS format)",
  "thumbnail": "string (URL)",
  "video_id": "string",
  "uuid": "string (UUID format, auto-generated)",
  "added_by": "string (username, auto-generated)",
  "downvotes": ["string (array of emails)"]
}
```

### User Object
```json
{
  "email": "string",
  "username": "string"
}
```

### Room Object
```json
{
  "code": "string",
  "host": "User Object",
  "users": ["User Object array"],
  "current_song": "Song Object or {}",
  "queue": ["Song Object array"],
  "max_downvotes": "number",
  "created_at": "datetime"
}
```

### Playlist Object
```json
{
  "_id": "string (UUID)",
  "playlist_id": "string (UUID)",
  "name": "string",
  "owner": "string (email)",
  "public": "boolean",
  "songs": ["Song Object array"]
}
```

---

## Notes

1. All UUID parameters are validated for proper UUID format
2. JWT tokens are required for most endpoints and are validated
3. Room codes are auto-generated and unique
4. Song UUIDs are auto-generated when adding to queue
5. Users can only modify their own playlists
6. Only room hosts can remove songs from queue and change room settings
7. Songs are automatically removed from queue when they reach the max downvote threshold
8. WebSocket events are emitted to all users in the same room
