import os
import redis

# Load REDIS_URL from environment
redis_url = os.getenv("REDIS_URL")

if not redis_url:
    print("REDIS_URL not set in environment.")
else:
    try:
        r = redis.from_url(redis_url)
        r.set("test_key", "redis-py")
        value = r.get("test_key")
        print("Redis test value:", value.decode())
    except Exception as e:
        print("Redis connection failed:", e)
