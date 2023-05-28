#!/usr/bin/python3
"""A module containing a function to load .env files"""
import os


def load_env_file():
    """Loads all environment variables from .env file"""
    try:
        with open('.env', 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value
    except Exception:
        pass
