FROM apache/airflow:2.7.1

USER root
# Install git 
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

USER airflow
# Installing PyTorch CPU version specifically
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

#  Installing the rest from the standard PyPI index
RUN pip install --no-cache-dir \
    transformers \
    pandas \
    mlflow \
    sentencepiece