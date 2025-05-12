"""This script takes in text files and uses an SVM model to assign sentiment scores to headlines."""
import sys
import datetime
import joblib
from sentence_transformers import SentenceTransformer
import requests
import logging
from typing import Dict, List

app = FastAPI()
logging.basicConfig(
    level=logging.INFO,
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

try:
    logger.info("Loading Sentence Transformer model...")
    model = SentenceTransformer("/opt/huggingface_models/all-MiniLM-L6-v2")
    logger.info("Sentence Transformer model loaded.")
    logger.info("Loading SVM model...")
    clf = joblib.load('svm.joblib')
    logger.info("SVM Model loaded.")

except Exception as e:
    logger.critical("Unable to load model.")

@app.get('/status')
def status() -> Dict[str, str]:
    d = {'status':'OK'}
    return d

@app.post('/score_headlines')
def score_headlines(headlines: List[str]):
    try:
        embeddings = model.encode(headlines)
        scores = clf.predict(embeddings)
        return scores
    except Exception as e:
        logging.error("Error scoring headlines")

