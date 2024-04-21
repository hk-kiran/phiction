# app/__init__.py
import sys
import os

# Ensure the root project directory is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from settings import OPENAI_API_KEY