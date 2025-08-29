import os
import joblib
import pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL = os.path.join(ROOT, "services", "classifier", "clf.joblib")
DATA = os.path.join(ROOT, "data", "intents.csv")

def test_model_exists_after_training():
    assert os.path.exists(MODEL), "Run train_classifier.py before tests."

def test_predict_labels():
    model = joblib.load(MODEL)
    df = pd.read_csv(DATA)
    texts = df['text'].sample(10, random_state=1).tolist()
    preds = model.predict(texts)
    labels = set(df['label'].unique().tolist())
    for p in preds:
        assert p in labels

