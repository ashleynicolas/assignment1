"""This script takes in text files and uses an SVM model to assign sentiment scores to headlines."""
import sys
import datetime
import joblib
from sentence_transformers import SentenceTransformer

if len(sys.argv) < 3:
    print("ERROR: Missing parameter. Please include text file name and source name.")
    print("FORMAT: python score_headlines.py <TEXT_FILE> <SOURCE_NAME>")
    print("EXAMPLE: python score_headlines.py nyt_headlines_today.txt nyt")
    sys.exit(1)

TEXT_FILE = sys.argv[1]
SOURCE_NAME = sys.argv[2]

# Read in text file to create headline vectors for model classification
with open(TEXT_FILE, 'r', encoding="utf-8") as file:
    headlines = file.readlines()
model = SentenceTransformer("/opt/huggingface_models/all-MiniLM-L6-v2")
embeddings = model.encode(headlines)

# Load in trained SVM model to classify headline based on vector embeddings
clf = joblib.load('svm.joblib')
scores = clf.predict(embeddings)

TODAY = datetime.datetime.today().strftime('%Y_%m_%d')

# Write output file with scores followed by corresponding headline
OUTPUT_FILE = f"headline_scores_{SOURCE_NAME}_{TODAY}.txt"
with open(OUTPUT_FILE, 'w', encoding='utf-8') as output:
    for score, headline in zip(scores, headlines):
        output.write(f"{score}, {headline}")

print(f"Output file saved as {OUTPUT_FILE}")
