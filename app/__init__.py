# app/__init__.py
import sys
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ELEVEN_LABS_API_KEY = os.environ.get("ELEVEN_LABS_API_KEY")

print("ASDFG", OPENAI_API_KEY, ELEVEN_LABS_API_KEY)
