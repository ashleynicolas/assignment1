import os
import sys
import time
import numpy as mp
from sentence_transformers import SentenceTransformer
import joblib

# score_headlines.py

if len(sys.argv) < 3:
    print("ERROR: Missing parameter. Please include text file name and source name such as 'python score_headlines.py <TEXT_FILE> <SOURCE_NAME>")
    sys.exit(1)

TEXT_FILE = sys.argv[1]
SOURCE_NAME = sys.argv[2]

with open(TEXT_FILE, 'r') as file:
    headlines = file.readlines()
    
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(headlines)

clf = joblib.load('svm.joblib')

scores = clf.predict(embeddings)

OUTPUT_FILE = f"headlines"
with(open)



