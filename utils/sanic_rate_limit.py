import datetime
import functools

from sanic import response

from app import redis
from results.results import Results


def rate_limited(max_per_min):
    def wrapper(func):
        async def limited_view():
            return response.json(
                Results.RATE_LIMIT, status=429)

        @functools.wraps(func)
        async def rate_limited_func(*args, **kargs):
            with await redis.conn as r:
                minute = datetime.datetime.now().minute
                key = "func:%s" % minute  # redis key for each minute
                tr = r.multi_exec()
                tr.incr(key)  # counting the number of request at this minute
                tr.expire(key, 59)  # expire the key after a minute to free up space
                await tr.execute()
                val = await r.get(key)
                if int(val) <= max_per_min:
                    return await func(*args, **kargs)
                else:
                    return await limited_view()

        return rate_limited_func

    return wrapper
