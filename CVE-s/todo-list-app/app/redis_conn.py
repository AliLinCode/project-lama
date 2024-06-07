import redis
import os
import logging
from dotenv import load_dotenv


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("redis")

# Load environment variables from .env file
load_dotenv()

def get_redis_connection():
    """Establish and return a connection to the Redis server."""
    try:
        # Create a Redis connection object
        r = redis.Redis(
            host=os.getenv('REDIS_HOST', '127.0.0.1'),
            port=os.getenv('REDIS_PORT', 6379),
            decode_responses=True  # Automatically decode responses to utf-8
        )
        logger.info("Connected to Redis")
        return r
    except Exception as e:
        logger.exception("Failed to connect to Redis")
        raise
