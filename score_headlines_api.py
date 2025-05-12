"""Script creates an API that clients can use to get headline sentiment scores"""
import joblib
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI, HTTPException
import logging
from typing import Dict, List

app = FastAPI()
logging.basicConfig(
    level=logging.INFO,
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

try:
    model = SentenceTransformer("/opt/huggingface_models/all-MiniLM-L6-v2")
    clf = joblib.load('svm.joblib')
except Exception as e:
    logger.critical("Unable to load model.")

@app.get('/status')
def status() -> Dict[str, str]:
    d = {'status':'OK'}
    return d

@app.post('/score_headlines')
def score_headlines(headlines: List[str]) -> Dict[str, List[str]]:
    if not headlines:
        raise HTTPException(400, "`headlines` must be a non-empty list")
    try:
        embeddings = model.encode(headlines)
        scores = clf.predict(embeddings)
        return {'labels':scores}
    except Exception as e:
        logger.error("Error scoring headlines")
