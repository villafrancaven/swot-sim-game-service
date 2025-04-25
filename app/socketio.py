import eventlet
eventlet.monkey_patch()

from flask_socketio import SocketIO
import redis
import os

redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")

redis_client = redis.Redis.from_url(redis_url, decode_responses=True)

socketio = SocketIO(cors_allowed_origins="*", message_queue=redis_url, async_mode="eventlet")
