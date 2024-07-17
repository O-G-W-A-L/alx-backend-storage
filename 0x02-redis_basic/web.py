#!/usr/bin/env python3
"""requesting to the web"""

import redis
import requests
from functools import wraps
from typing import Callable

# Initialize the Redis connection
r = redis.Redis()

def cache_page(method: Callable) -> Callable:
    '''Decorator to cache the output of the fetched data.'''
    @wraps(method)
    def wrapper(url: str) -> str:
        # Increment the URL access count
        r.incr(f"count:{url}")
        # Check if the result is already cached
        cached_result = r.get(f"cached:{url}")
        if cached_result:
            return cached_result.decode('utf-8')
        # If not cached, fetch the result and cache it
        result = method(url)
        r.setex(f"cached:{url}", 10, result)
        return result
    return wrapper

@cache_page
def get_page(url: str) -> str:
    '''Get the content of a page and cache it.'''
    response = requests.get(url)
    return response.text
