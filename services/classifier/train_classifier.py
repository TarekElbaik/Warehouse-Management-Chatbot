"""
Train a simple TF-IDF + LogisticRegression classifier from data/intents.csv
"""
import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DATA_PATH = os.path.join(ROOT, "data", "intents.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "clf.joblib")

def main():
    df = pd.read_csv(DATA_PATH)
    X = df["text"].astype(str)
    y = df["label"].astype(str)

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2), min_df=1)),
        ("lr", LogisticRegression(max_iter=1000))
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    pipe.fit(X_train, y_train)

    print("Evaluation on holdout:")
    y_pred = pipe.predict(X_test)
    print(classification_report(y_test, y_pred))

    joblib.dump(pipe, MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")

if __name__ == "__main__":
    main()

