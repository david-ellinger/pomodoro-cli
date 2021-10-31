import redis

class Database():
    db = redis.Redis(host="redis",port=6379, db=0, decode_responses=True)

    def set(self, key, value, **kwargs):
        return self.db.set(key, value, **kwargs)

    def set_redis_values(self, data):
        [self.db.set(key, data[key]) for key in data.keys()]

