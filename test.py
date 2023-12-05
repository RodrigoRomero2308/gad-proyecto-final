import sqlite3
from PIL import Image
import numpy as np
from scipy.spatial.distance import cdist
import pickle

# Load an image
def load_image(file_path):
    image = Image.open(file_path)
    return np.array(image)

# Calculate image embeddings (you can replace this with any pre-trained model)
def calculate_embeddings(image):
    return np.mean(image, axis=(0, 1))

# Create a database connection
def create_connection():
    conn = sqlite3.connect(':memory:')
    return conn

# Create a table for storing images and their embeddings
def create_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE images
             (id INTEGER PRIMARY KEY, name TEXT, image BLOB, embeddings BLOB)''')

# Insert an image and its embeddings into the database
def insert_image(conn, image, embeddings, name):
    c = conn.cursor()
    blob = sqlite3.Binary(pickle.dumps(image))
    embeddings_blob = sqlite3.Binary(pickle.dumps(embeddings))
    c.execute("INSERT INTO images (name, image, embeddings) VALUES (?, ?, ?)", (name, blob, embeddings_blob))
    conn.commit()

# Query the 5 closest images to an input image from the database
def query_images(conn, input_embeddings, k=5):
    c = conn.cursor()
    c.execute("SELECT id, name, image, embeddings FROM images")
    rows = c.fetchall()

    closest_images = []
    for row in rows:
        id, name, image, embeddings = row
        image_embeddings = pickle.loads(embeddings)
        distance = np.linalg.norm(input_embeddings - image_embeddings)
        closest_images.append((distance, id, name, image))

    closest_images.sort()
    closest_images = closest_images