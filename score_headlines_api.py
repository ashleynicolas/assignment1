"""Script creates an API that clients can use to get headline sentiment scores"""
import joblib
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI
import logging
from typing import Dict, List
import uvicorn

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
def score_headlines(headlines: List[str]):
    try:
        embeddings = model.encode(headlines)
        scores = clf.predict(embeddings)
        return {'labels':scores}
    except Exception as e:
        logging.error("Error scoring headlines")

if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8082, reload=True)