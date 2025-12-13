from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default settings for the DAG
default_args = {
    'owner': 'sherry',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'ad_creative_pipeline',
    default_args=default_args,
    description='MLOps pipeline for Ad Generation',
    schedule_interval=timedelta(days=1), # Runs once a day
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['mlops', 'ad-generator'],
) as dag:

    # Task 1: Data Ingestion
    # We use BashOperator to run the script inside the Airflow container
    ingest_task = BashOperator(
        task_id='ingest_data',
        bash_command='python /opt/airflow/src/data_ingestion.py'
    )

    # Task 2: Model Training (Placeholder for Phase 4)
    train_task = BashOperator(
        task_id='train_model',
        bash_command='python /opt/airflow/src/train_model.py'
    )

    # Set dependency: Ingest MUST finish before Train starts
    ingest_task >> train_task