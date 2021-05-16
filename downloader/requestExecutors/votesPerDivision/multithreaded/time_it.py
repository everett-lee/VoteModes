import time
import logging
from functools import wraps

#SOURCE: https://rednafi.github.io/digressions/python/2020/04/21/python-concurrent-futures.html
def timeit(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        end_time = time.time()
        logging.info(f"{method.__name__} => {(end_time-start_time)*1000} ms")

        return result

    return wrapper
