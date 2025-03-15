from flask import Flask
import redis

# Initialise Flask app
app = Flask(__name__)

# Connect to Redis database
# Redis is running on localhost at port 6379, using database index 0
# decode_responses=True ensures the data is returned as strings instead of bytes
redis_client = redis.Redis(host='db', port=6379, db=0, decode_responses=True)

@app.route('/')
def home():
    # Route for the home page, displaying a welcome message."""
    return "Welcome to the Flask Web App!"

@app.route('/count')
def count():
    # Route for counting visits. Increments and displays the visit count from Redis."""
    visits = redis_client.incr('visit_count')  # Increment visit count in Redis
    return f'Visit count: {visits}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)   
