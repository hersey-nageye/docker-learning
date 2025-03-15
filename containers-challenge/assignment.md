# Docker Assignment - CoderCo Containers Challenge

## Objective
Create a multi-container application consisting of a simple Python Flask web application and a Redis database. The Flask application should use Redis to store and retrieve data.

## Requirements
1. **Flask Web Application**:
   - A Flask app with two routes:
     - `/`: Displays a welcome message.
     - `/count`: Increments and displays a visit count stored in Redis.
2. **Redis Database**:
   - Use Redis as a key-value store to keep track of the visit count.
3. **Dockerize Both Services**:
   - Create Dockerfiles for both the Flask app and Redis.
   - Use Docker Compose to manage the multi-container application.

## Test the Application
### Access the Welcome Page
Open your browser and go to `http://localhost:5000` to view the welcome message.

### Test the Visit Count
Navigate to `http://localhost:5000/count` to see the visit count increment each time you refresh the page.

---

### Step 1: Flask Application
Start by creating the Flask app (`flask-app.py`) based on requirements 1 and 2:

```python
from flask import Flask
import redis

# Initialize Flask app
app = Flask(__name__)

# Connect to Redis database (localhost:6379)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@app.route('/')
def home():
    """Route for the home page, displaying a welcome message."""
    return "Welcome to the Flask Web App!"

@app.route('/count')
def count():
    """Route for counting visits. Increments and displays the visit count from Redis."""
    visits = redis_client.incr('visit_count')  # Increment visit count in Redis
    return f'Visit count: {visits}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
```

Test the Flask app locally by running `python3 flask-app.py` and accessing `http://localhost:5001` in your browser. Check if the `/count` page works as expected. Once the app is tested locally and confirmed to be working, make sure to update the host for the Redis connection in the Flask app from `'localhost'` to `'db'`, as this is the service name defined in your `docker-compose.yml` file.


---

### Step 2: Dockerfile for Flask App
Create a Dockerfile for the Flask app, naming it `Dockerfile.flask`:

```dockerfile
FROM python:3-alpine

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements.txt file to the container
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose port 5001
EXPOSE 5001

# Command to run the Flask app
CMD [ "python", "flask-app.py" ]
```

Build the Docker image for the Flask app:
```bash
docker build -t flask-app -f Dockerfile.flask .
```

Verify the image has been created:
```bash
docker images
```

---

### Step 3: Dockerfile for Redis
Create a Dockerfile for Redis, naming it `Dockerfile.redis`:

```dockerfile
# Use the official Redis image from Docker Hub
FROM redis

# Set the working directory for Redis config
WORKDIR /usr/local/etc/redis

# Copy the custom redis.conf file to the container
COPY redis.conf /usr/local/etc/redis/redis.conf

# Expose port 6379 for Redis
EXPOSE 6379

# Command to run the Redis server with the custom config
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]
```

Build the Docker image for Redis:
```bash
docker build -t redis-database -f Dockerfile.redis .
```

Verify the image creation:
```bash
docker images
```

---

### Step 4: Docker Compose Configuration
Create a `docker-compose.yml` file to build and run both containers simultaneously:

```yaml
version: '3'

services:
  web:
    image: flask-app
    ports:
      - "5001:5001"
    depends_on:
      - db

  db:
    image: redis-database
    ports:
      - "6379:6379"
```

---

### Step 5: Running the Application
To run the containers, execute the following command:
```bash
docker-compose up -d
```

Check if the containers are running:
```bash
docker ps
```

---

### Step 6: Access the Application
Open your browser and navigate to:
- **Welcome Page**: http://127.0.0.1:5001/
- **Visit Count**: http://127.0.0.1:5001/count

**Conclusion**
The multi-container application consisting of a Flask web app and Redis database is up and running. The visit count increments each time the `/count` page is refreshed.

To stop and remove the containers, execute the following command:
```bash
docker-compose down
```

This will gracefully shut down the containers and clean up any resources created by Docker Compose.