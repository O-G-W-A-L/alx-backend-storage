#!/usr/bin/env python3
"""Requesting to the web and caching the response."""

import redis
import requests

# Connect to Redis
r = redis.Redis()


def get_page(url: str) -> str:
    """Get the content of a page and cache it for 10 seconds."""
    try:
        # Check if the page is already cached
        cached_page = r.get(f"cached:{url}")
        if cached_page:
            print("Cache hit")  # Debugging output
            return cached_page.decode('utf-8')

        # Fetch the page content
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        html_content = response.text

        # Cache the result with an expiration time of 10 seconds
        r.setex(f"cached:{url}", 10, html_content)
        print("Cache set")  # Debugging output

        # Increment the URL access count
        r.incr(f"count:{url}")
        print("Count incremented")  # Debugging output

        return html_content
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"


if __name__ == "__main__":
    url = 'http://slowwly.robertomurray.co.uk'
    print(get_page(url))
    print(f"URL accessed {r.get(f'count:{url}').decode('utf-8')} times")
