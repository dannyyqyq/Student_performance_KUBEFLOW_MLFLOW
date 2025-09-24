import pandas as pd
import json
from loguru import logger

def main():
    logger.add(sys.stdout, colorize=True, format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}")

    raw_data_path = "/data/student.csv"  
    output_data_path = "/tmp/data.csv"
    metadata_path = "/tmp/ingest_metadata.json"

    logger.info(f"Starting ingestion process...")
    logger.info(f"Reading raw data from {raw_data_path}")

    try:
        df = pd.read_csv(raw_data_path)
    except FileNotFoundError:
        logger.error(f"File not found: {raw_data_path}")
        return

    logger.info(f"Raw data loaded: {len(df)} rows, {len(df.columns)} columns")

    # Simplified cleaning
    df = df.dropna()
    logger.info(f"After dropping NA: {len(df)} rows")

    # Save cleaned data
    df.to_csv(output_data_path, index=False)
    logger.info(f"Cleaned data saved to {output_data_path}")

    # Save metadata
    metadata = {
        "rows": len(df),
        "columns": df.columns.tolist(),
        "raw_data_path": raw_data_path,
        "output_data_path": output_data_path
    }

    with open(metadata_path, "w") as f:
        json.dump(metadata, f)

    logger.info(f"Metadata saved to {metadata_path}")
    logger.info("Ingestion completed!!!")

if __name__ == "__main__":
    import sys
    main()
