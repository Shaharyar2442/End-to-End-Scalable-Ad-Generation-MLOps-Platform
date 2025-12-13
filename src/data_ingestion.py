import pandas as pd
import os

RAW_PATH = "/opt/airflow/data/raw/sample_products.csv"
PROCESSED_PATH = "/opt/airflow/data/processed/training_data.csv"

def ingest_data():
    print("Starting data ingestion...")
    
    # 1. Read Data
    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError(f"Raw data not found at {RAW_PATH}")
    
    df = pd.read_csv(RAW_PATH)
    print(f"Raw data loaded. Rows: {len(df)}")
    
    # 2. Simple Cleaning (Data Layer requirement [cite: 36])
    # Drop rows where description is missing
    df = df.dropna(subset=['description'])
    
    # 3. Feature Engineering (Construct the input text for T5)
    # T5 expects "task: input_text". We prep this column now.
    df['input_text'] = "write an advertisement for: " + df['product_name'] + ". Key features: " + df['description']
    
    # 4. Save to Processed
    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"Data processed and saved to {PROCESSED_PATH}")

if __name__ == "__main__":
    ingest_data()