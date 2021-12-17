import redis


class Database:

    def set(self, key, value, **kwargs):
        return self.db.set(key, value, **kwargs)

    def set_redis_values(self, data):
        [self.db.set(key, data[key]) for key in data.keys()]
