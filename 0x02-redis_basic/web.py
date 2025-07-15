#!/usr/bin/env python3
"""Requesting web pages with Redis-based caching and tracking."""

import redis
import requests
from functools import wraps
from typing import Callable

# Initialize Redis connection
r = redis.Redis()


def cache_and_track(func: Callable) -> Callable:
    """Decorator to cache URL response and track access count."""

    @wraps(func)
    def wrapper(url: str) -> str:
        cache_key = f"cached:{url}"
        count_key = f"count:{url}"

        # Increment count regardless of cache hit or not
        r.incr(count_key)

        cached = r.get(cache_key)
        if cached:
            print("Cache hit")
            return cached.decode('utf-8')

        # Call the wrapped function to get fresh data
        result = func(url)

        # Cache for 10 seconds
        r.setex(cache_key, 10, result)
        print("Cache set")

        return result

    return wrapper


@cache_and_track
def get_page(url: str) -> str:
    """Fetch HTML content of a URL using requests."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    # Test URL
    test_url = "http://slowwly.robertomurray.co.uk"

    # Fetch page
    print(get_page(test_url))

    # Show how many times this URL has been accessed
    count = r.get(f"count:{test_url}")
    if count:
        print(count.decode('utf-8'))
