import torch
from transformers import pipeline

print(f"PyTorch Version: {torch.__version__}")
print(f"CUDA Available: {torch.cuda.is_available()} (Should be False for CPU)")

# Test downloading a tiny model to ensure internet and library work
print("Downloading a test model...")
generator = pipeline('text-generation', model='distilgpt2')
print("Model loaded successfully!")