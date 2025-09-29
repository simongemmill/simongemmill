from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading
import time
import redis
import os

# Initialize Flask app with custom folders
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

# Load Redis URI from environment or fallback
redis_uri = os.getenv("REDIS_URL")
redis_client = redis.Redis.from_url(redis_uri) if redis_uri else None

# Initial state
state = {
    "timeline": 0.0,
    "yen_counter": -3.0,
    "yo_counter": 0.0,
    "statoshi_balance": 1_000_000_000,
    "p_balance": 0.0,
    "ten_balance": 0.0
}

unit = 1.0
updatesPaused = False

@app.route('/')
def index():
    return "Dashboard backend is running"

@app.route('/start', methods=['GET'])
def start_route():
    global updatesPaused
    updatesPaused = False
    return "Updates resumed"

@app.route('/pause', methods=['GET'])
def pause_route():
    global updatesPaused
    updatesPaused = True
    return "Updates paused"

@app.route('/')
def index():
    return render_template("index.html")

def reset_route():
    state["timeline"] = 0.0
    return "Timeline reset"

def background_task():
    global updatesPaused
    while True:
        try:
            if not updatesPaused:
                state["timeline"] += 8.497
                state["yen_counter"] += state["timeline"]
                state["yo_counter"] += 1_000_000 * unit
                state["p_balance"] += 9.0
                state["ten_balance"] += 9.0
                state["ten_balance"] *= 1.15

                socketio.emit("state_update", state)

                if redis_client:
                    redis_client.set("latest_timeline", state["timeline"])

            time.sleep(9)

        except Exception as e:
            print("Background task error:", e)
            time.sleep(1)

# Start background thread
threading.Thread(target=background_task, daemon=True).start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=32)  # Localhost or Render
