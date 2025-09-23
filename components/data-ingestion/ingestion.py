import pandas as pd
from sklearn.model_selection import train_test_split
import yaml
import os

def ingest_data(data_path, params_path, output_dir):
    # Load params
    with open(params_path, "r") as f:
        params = yaml.safe_load(f)
    # Load dataset
    df = pd.read_csv(data_path)
    # Clean: Drop missing values (customize based on your dataset)
    df = df.dropna()
    # Split data
    train_df, test_df = train_test_split(df, test_size=params["data"]["test_size"], random_state=42)
    # Save outputs
    os.makedirs(output_dir, exist_ok=True)
    train_df.to_csv(f"{output_dir}/train.csv", index=False)
    test_df.to_csv(f"{output_dir}/test.csv", index=False)

if __name__ == "__main__":
    ingest_data("/input/data.csv", "/input/params.yaml", "/output")