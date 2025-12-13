from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
from src.app.model import AdGenerator  # Reusing your class from Phase 2

app = FastAPI(title="Ad Creative Generator API")

# --- Prometheus Metrics ---
REQUEST_COUNT = Counter("request_count", "Total number of inference requests", ["status"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Latency of inference requests")

# --- Initialize Model ---
# We load the model once when the app starts
try:
    ad_generator = AdGenerator()
except Exception as e:
    print(f"Error loading model: {e}")
    ad_generator = None

# --- Request Schema ---
class AdRequest(BaseModel):
    product_name: str
    description: str

# --- Endpoints ---
@app.get("/health")
def health_check():
    if ad_generator:
        return {"status": "healthy", "model": "loaded"}
    return {"status": "unhealthy", "error": "model_failed"}

@app.get("/metrics")
def metrics():
    """Expose Prometheus metrics"""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/generate")
def generate_ad(request: AdRequest):
    """
    Generate ad text from product description.
    """
    start_time = time.time()
    
    if not ad_generator:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Generate the ad
        ad_copy = ad_generator.generate_ad(request.product_name, request.description)
        
        # Log success metric
        REQUEST_COUNT.labels(status="success").inc()
        REQUEST_LATENCY.observe(time.time() - start_time)
        
        return {"ad_copy": ad_copy}
    
    except Exception as e:
        # Log failure metric
        REQUEST_COUNT.labels(status="error").inc()
        raise HTTPException(status_code=500, detail=str(e))