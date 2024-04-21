from glob import glob
import os
from random import choices
import re

from PIL import Image

from pymongo import MongoClient
from pymongo.errors import CollectionInvalid, DuplicateKeyError

from sentence_transformers import SentenceTransformer 
from tqdm.notebook import tqdm                        
from os.path import join, dirname
from dotenv import load_dotenv

def read_properties_file(file_path):
    properties = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=')
                properties[key.strip()] = value.strip()
    return properties

### CLASSES ###

class Database():

    def __init__(self) -> None:
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        properties = read_properties_file('./app.properties')
        # These can be modified if they're not appropriate for your cluster:
        DATABASE_NAME = str(properties["db_name"])
        IMAGE_COLLECTION_NAME = str(properties["collection_name"])

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

        self.collection = db.get_collection(IMAGE_COLLECTION_NAME)

        self.model = SentenceTransformer("clip-ViT-L-14")
    
    def load_images_to_db(self, image_count=1000):
        """
        Load `image_count` images into the database, creating an embedding for each using the sentence transformer above.

        This can take some time to run if image_count is large.

        The image's pixel data is not loaded into MongoDB, just the image's path and vector embedding.
        """
        image_paths = choices(glob("images/*.png", recursive=True), k=image_count)
        for path in tqdm(image_paths):
            emb = self.model.encode(Image.open(path))
            try:
                self.collection.insert_one(
                    {
                        "_id": re.sub("images/", "", path),
                        "embedding": emb.tolist(),
                    }
                )
            except DuplicateKeyError:
                pass
    
    def query_top_k_images(self, query, top_k=5):
        emb = self.model.encode(query)
        cursor = self.collection.aggregate(
            [
                {
                    "$vectorSearch": {
                        "index": "default",
                        "path": "embedding",
                        "queryVector": emb.tolist(),
                        "numCandidates": 100,
                        "limit": top_k,
                    }
                },
                {"$project": {"_id": 1, "score": {"$meta": "vectorSearchScore"}}},
            ]
        )
        image_paths = []
        for img in list(cursor):
            image_paths.append("images/" + img["_id"])

        return image_paths

### ###

if __name__ == "__main__":
    db = Database()
    # db.load_images_to_db()
    query = "dogs"
    top_k = 5
    print(db.query_top_k_images(query, top_k))

