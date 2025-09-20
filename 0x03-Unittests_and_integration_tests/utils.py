#!/usr/bin/env python3
"""
Utility functions for testing purposes.
This module provides functions for accessing nested maps, making HTTP requests,
and memoization.
"""
import requests
from functools import wraps
from typing import Dict, Tuple, Any, Union


def access_nested_map(nested_map: Dict, path: Tuple[str, ...]) -> Any:
    """
    Access a value in a nested map using a tuple of keys.
    
    Args:
        nested_map: The nested dictionary to access
        path: Tuple of keys representing the path to the value
        
    Returns:
        The value at the specified path
        
    Raises:
        KeyError: If any key in the path doesn't exist
    """
    for key in path:
        if not isinstance(nested_map, dict) or key not in nested_map:
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Dict:
    """
    Get JSON data from a URL.
    
    Args:
        url: The URL to fetch JSON from
        
    Returns:
        The JSON data as a dictionary
    """
    response = requests.get(url)
    return response.json()


def memoize(func):
    """
    Memoize decorator that caches function results.
    
    Args:
        func: The function to memoize
        
    Returns:
        The memoized function
    """
    cache = {}
    
    @wraps(func)
    def wrapper(self):
        if func not in cache:
            cache[func] = func(self)
        return cache[func]
    
    # Add cache attribute for testing
    wrapper.cache = cache
    return property(wrapper)
