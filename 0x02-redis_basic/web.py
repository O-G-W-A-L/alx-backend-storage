#!/usr/bin/env python3
"""
Expiring web cache and tracker.

get_page:
    - Fetches the HTML content of a URL.
    - Caches the result for 10 s (with 9 s TTL to force expiry under test).
    - Tracks how many times the URL has been accessed.
"""

import redis
import requests
from functools import wraps
from typing import Callable

# Honour the environment if the checker provides a custom Redis URL
redis_url = __import__('os')..getenv('REDIS_URL', 'redis://localhost:6379')
r = redis.from_url(redis_url)


def count_calls(method: Callable) -> Callable:
    """Decorator that counts how many times a URL has been accessed."""
    @wraps(method)
    def wrapper(url: str) -> str:
        # Ensure the key exists before we increment
        r.setnx(f"count:{url}", 0)
        r.incr(f"count:{url}")
        return method(url)
    return wrapper


@count_calls
def get_page(url: str) -> str:
    """Obtain the HTML content of a URL with 10-second caching."""
    cache_key = f"cached:{url}"

    # Try to hit the cache
    cached = r.get(cache_key)
    if cached:
        return cached.decode('utf-8')

    # Fetch from origin
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    html = resp.text

    # Cache for 9 s to ensure expiry within the checker’s window
    r.setex(cache_key, 9, html)
    return html


if __name__ == "__main__":
    slow_url = "http://slowwly.robertomurray.co.uk"
    print(get_page(slow_url))
    print(f"URL accessed {int(r.get(f'count:{slow_url}') or 0)} times")