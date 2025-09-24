# components/model-training/train.py

import sys
import json
import pandas as pd
from loguru import logger
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
import joblib

def main():
    # Logger setup
    logger.remove()
    logger.add(sys.stdout, colorize=True,
               format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}")

    train_path = "/tmp/train.csv"
    test_path = "/tmp/test.csv"
    model_path = "/tmp/model.pkl"
    metrics_path = "/tmp/metrics.json"

    logger.info("Starting model training...")

    try:
        train_df = pd.read_csv(train_path)
        test_df = pd.read_csv(test_path)
        logger.info(f"Loaded train ({train_df.shape}) and test ({test_df.shape}) datasets")
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return

    # Assuming the last column is the target
    X_train = train_df.iloc[:, :-1]
    y_train = train_df.iloc[:, -1]
    X_test = test_df.iloc[:, :-1]
    y_test = test_df.iloc[:, -1]

    logger.info(f"Training model on {X_train.shape[0]} samples with {X_train.shape[1]} features")

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    logger.info("Model training complete")

    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    metrics = {"accuracy": acc, "f1_score": f1}

    logger.info(f"Evaluation metrics: Accuracy={acc:.4f}, F1={f1:.4f}")

    # Save model
    joblib.dump(model, model_path)
    logger.info(f"Trained model saved to {model_path}")

    # Save metrics
    with open(metrics_path, "w") as f:
        json.dump(metrics, f)
