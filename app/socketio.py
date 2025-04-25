from flask_socketio import SocketIO
import redis

socketio = SocketIO(cors_allowed_origins="*")

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
