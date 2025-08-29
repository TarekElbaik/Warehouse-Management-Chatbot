"""
FastAPI app exposing /predict for text intent classification
"""
import os
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

MODEL_PATH = os.path.join(os.path.dirname(__file__), "clf.joblib")
app = FastAPI(title="Classifier Service", version="1.0.0")

class PredictIn(BaseModel):
    text: str

class PredictOut(BaseModel):
    intent: str
    confidence: float

# Lazy load
model = None
def load_model():
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError(f"Model not found at {MODEL_PATH}. Run train_classifier.py first.")
        model = joblib.load(MODEL_PATH)

@app.post("/predict", response_model=PredictOut)
def predict(inp: PredictIn):
    load_model()
    probs = model.predict_proba([inp.text])[0]
    classes = model.classes_
    top_idx = probs.argmax()
    return {"intent": str(classes[top_idx]), "confidence": float(probs[top_idx])}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

