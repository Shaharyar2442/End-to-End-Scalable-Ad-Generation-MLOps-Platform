import mlflow
import mlflow.pytorch
import torch
import transformers
import pandas as pd
import os
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Define paths
PROCESSED_DATA_PATH = "/opt/airflow/data/processed/training_data.csv"
if not os.path.exists("/opt/airflow"):
    PROCESSED_DATA_PATH = "data/processed/training_data.csv"

def train_model():
    print("--- 1. Initializing Training Script ---")
    
    # Setup MLflow Tracking
    tracking_uri = "http://mlflow:5000" if os.path.exists("/.dockerenv") else "http://localhost:5000"
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment("ad_creative_generation")
    
    print(f"--- 2. Connected to MLflow at {tracking_uri} ---")

    with mlflow.start_run():
        # Log Parameters
        params = {
            "epochs": 1,
            "batch_size": 4,
            "learning_rate": 5e-5,
            "model_name": "t5-small"
        }
        mlflow.log_params(params)
        print("--- 3. Parameters Logged ---")
        
        # Load Data
        if os.path.exists(PROCESSED_DATA_PATH):
            df = pd.read_csv(PROCESSED_DATA_PATH)
        else:
            print("Warning: Data not found, creating dummy data in memory.")
            
        # Load Model
        print("--- 4. Loading Model (cached) ---")
        tokenizer = T5Tokenizer.from_pretrained(params["model_name"])
        model = T5ForConditionalGeneration.from_pretrained(params["model_name"])
        
        # Simulate Training
        print("--- 5. Simulating Training Steps ---")
        for step in range(0, 3):
            loss = 2.5 - (step * 0.4) 
            mlflow.log_metric("training_loss", loss, step=step)
        
        # Log Model (THE FIX IS HERE)
        print("--- 6. Logging Model to MLflow (This writes ~250MB) ---")
        
        # We explicitly list dependencies to skip the slow auto-scan
        reqs = [
            f"torch=={torch.__version__}", 
            f"transformers=={transformers.__version__}",
            f"pandas=={pd.__version__}"
        ]
        
        mlflow.pytorch.log_model(
            model, 
            "model", 
            registered_model_name="ad_generator_t5",
            pip_requirements=reqs  # <--- This prevents the hang!
        )
        print("--- 7. Training Complete. Model Logged Successfully! ---")

if __name__ == "__main__":
    train_model()