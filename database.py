from glob import glob
from math import ceil
import os
from pathlib import Path
from random import choices
import re

import cv2
import matplotlib.pyplot as plt
from PIL import Image

from pymongo import MongoClient
from pymongo.errors import CollectionInvalid, DuplicateKeyError
from pymongo.operations import SearchIndexModel

from sentence_transformers import SentenceTransformer 
from tqdm.notebook import tqdm                        

def read_properties_file(file_path):
    properties = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=')
                properties[key.strip()] = value.strip()
    return properties

### API ###

def fetch_query():

### ###

properties = read_properties_file('./app.properties')

# These can be modified if they're not appropriate for your cluster:
DATABASE_NAME = properties["db_name"]
IMAGE_COLLECTION_NAME = properties["collection_name"]

# Change this to 1000 to load a suitable number of images into MongoDB:
NUMBER_OF_IMAGES_TO_LOAD = properties["images_to_load_to_db"]

# Set this as an environment variable to avoid accidentally sharing your cluster credentials:
MONGODB_URI = os.environ.get('MONGO_DB_URI')

client = MongoClient(MONGODB_URI)
db = client.get_database(DATABASE_NAME)

# Ensure the collection exists, because otherwise you can't add a search index to it.
try:
    db.create_collection(IMAGE_COLLECTION_NAME)
except CollectionInvalid:
    # This is raised when the collection already exists.
    print("Images collection already exists")

collection = db.get_collection(IMAGE_COLLECTION_NAME)

model = SentenceTransformer("clip-ViT-L-14")

def load_images(image_count=1000):
    """
    Load `image_count` images into the database, creating an embedding for each using the sentence transformer above.

    This can take some time to run if image_count is large.

    The image's pixel data is not loaded into MongoDB, just the image's path and vector embedding.
    """
    image_paths = choices(glob("images/*.png", recursive=True), k=image_count)
    for path in tqdm(image_paths):
        emb = model.encode(Image.open(path))
        try:
            collection.insert_one(
                {
                    "_id": re.sub("images/", "", path),
                    "embedding": emb.tolist(),
                }
            )
        except DuplicateKeyError:
            pass


load_images(NUMBER_OF_IMAGES_TO_LOAD)

