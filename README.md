# PartyAux

A real-time music collaboration platform built with Flask, SocketIO, and MongoDB.

## Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd PartyAux
```

### 2. Create and activate virtual environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\Activate.ps1
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Copy the example environment file and configure your settings:
```bash
cp .env.example .env
```

Edit `.env` with your actual values:
- `MONGODB_URI`: Your MongoDB connection string
- `JWT_SECRET`: A strong secret key for JWT tokens
- `SENDER_EMAIL`: Your Gmail address
- `SENDER_PASSWORD`: Your Gmail app password

### 5. Run the application
```bash
python api.py
```

The server will start on `http://localhost:5000`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB connection string | - |
| `DATABASE_NAME` | MongoDB database name | PartyAux |
| `JWT_SECRET` | Secret key for JWT tokens | - |
| `JWT_ALGORITHM` | JWT algorithm | HS256 |
| `SENDER_EMAIL` | Gmail address for OTP | - |
| `SENDER_PASSWORD` | Gmail app password | - |
| `SMTP_SERVER` | SMTP server | smtp.gmail.com |
| `SMTP_PORT` | SMTP port | 587 |
| `FLASK_DEBUG` | Flask debug mode | True |
| `FLASK_HOST` | Flask host | 0.0.0.0 |
| `FLASK_PORT` | Flask port | 5000 |
| `CORS_ALLOWED_ORIGINS` | CORS allowed origins | * |

## Security Notes

- Never commit your `.env` file to version control
- Use strong, unique JWT secrets in production
- Use Gmail app passwords, not your main password
- Consider using environment-specific `.env` files (`.env.production`, `.env.development`)

## Features

- OTP-based user authentication
- Real-time room creation and joining
- YouTube Music integration
- Song queue management
- Downvoting system
- WebSocket-based real-time updates 