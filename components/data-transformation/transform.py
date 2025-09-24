# components/data-transformation/transform.py

import sys
import json
import pandas as pd
from loguru import logger
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split


def preprocess_data(df: pd.DataFrame):
    """
    Split data into train/test, encode categorical vars,
    and scale numeric vars (fit only on train).
    """
    # Train-test split
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    # Identify columns
    numeric_cols = train_df.select_dtypes(include=["int64", "float64"]).columns
    categorical_cols = train_df.select_dtypes(include=["object"]).columns

    logger.info(f"Numeric columns: {list(numeric_cols)}")
    logger.info(f"Categorical columns: {list(categorical_cols)}")

    # Encode categorical variables
    encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        train_df[col] = le.fit_transform(train_df[col].astype(str))
        test_df[col] = le.transform(test_df[col].astype(str))
        encoders[col] = le
        logger.info(f"Encoded column: {col}")

    # Scale numeric variables
    scalers = {}
    if len(numeric_cols) > 0:
        scaler = StandardScaler()
        train_df[numeric_cols] = scaler.fit_transform(train_df[numeric_cols])
        test_df[numeric_cols] = scaler.transform(test_df[numeric_cols])
        for col in numeric_cols:
            scalers[col] = scaler
        logger.info("Scaled numeric columns.")

    return train_df, test_df, list(numeric_cols), list(categorical_cols)


def main():
    # Setup logger
    logger.remove()
    logger.add(sys.stdout, colorize=True,
               format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}")

    input_path = "/tmp/data.csv"    # from ingestion
    train_path = "/tmp/train.csv"
    test_path = "/tmp/test.csv"
    metadata_path = "/tmp/transformation_metadata.json"

    logger.info("Starting train/test split and transformation...")

    try:
        df = pd.read_csv(input_path)
        logger.info(f"Loaded dataset with {df.shape[0]} rows, {df.shape[1]} columns.")
    except FileNotFoundError:
        logger.error(f"File not found: {input_path}")
        return

    train_df, test_df, numeric_cols, categorical_cols = preprocess_data(df)

    # Save processed datasets
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    logger.info(f"Train set saved: {train_path} ({train_df.shape})")
    logger.info(f"Test set saved: {test_path} ({test_df.shape})")

    # Save metadata
    metadata = {
        "train_rows": train_df.shape[0],
        "test_rows": test_df.shape[0],
        "numeric_columns": numeric_cols,
        "categorical_columns": categorical_cols,
        "input_path": input_path,
        "train_output": train_path,
        "test_output": test_path,
    }
    with open(metadata_path, "w") as f:
        json.dump(metadata, f)

    logger.info(f"Metadata saved to {metadata_path}")
    logger.info("Transformation complete!!!")


if __name__ == "__main__":
    main()
