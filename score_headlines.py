import sys
from sentence_transformers import SentenceTransformer
import joblib
import datetime

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

TODAY = datetime.datetime.today().strftime('%Y_%m_%d')

OUTPUT_FILE = f"headline_scores_{SOURCE_NAME}_{TODAY}.txt"
with open(output_name, 'w', encoding='utf-8') as output:
    for score, headline in zip(scores, headlines):
        output.write(f"{score}, {headline}")

print(f"Output file saved as <OUTPUT_FILE>")