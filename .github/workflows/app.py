from flask import Flask, render_template, request, jsonify
from flask_session import Session
from redis import Redis
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('redis.env')

app = Flask(__name__)

# Session config using Redis
app.config['SESSION_TYPE'] = os.getenv('SESSION_TYPE', 'redis')
app.config['SESSION_REDIS'] = Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    password=os.getenv('REDIS_PASSWORD', None),
    db=int(os.getenv('REDIS_DB', 0))
)
Session(app)

# Homepage route
@app.route('/')
def index():
    return render_template('index.html')

# Example API route
@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "running", "redis": True})

# Optional: Redis test route
@app.route('/api/redis-test', methods=['GET'])
def redis_test():
    r = app.config['SESSION_REDIS']
    try:
        r.set('test-key', 'hello')
        value = r.get('test-key').decode('utf-8')
        return jsonify({"redis_value": value})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
