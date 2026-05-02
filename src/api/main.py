from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from src.db.connection import get_connection
from src.model.inference import load_model, get_reconstruction_error

# Global model variables
model = None
min_val = None
max_val = None
THRESHOLD = 0.213

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model, min_val, max_val
    print("Loading model...")
    model, min_val, max_val = load_model()
    print("Model loaded.")
    yield

app = FastAPI(title="Price Tracker API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnomalyRequest(BaseModel):
    product_id: int
    prices: list[float]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/products")
def get_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, site FROM products ORDER BY site, name")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/price-history/{product_id}")
def get_price_history(product_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM products WHERE id = ?", (product_id,))
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Product not found")
    cursor.execute(
        "SELECT price, scraped_at FROM price_history WHERE product_id = ? ORDER BY scraped_at ASC",
        (product_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/detect-anomaly")
def detect_anomaly(request: AnomalyRequest):
    if len(request.prices) < 7:
        raise HTTPException(status_code=422, detail="Need at least 7 price points")
    sequence = request.prices[-7:]
    error = get_reconstruction_error(model, sequence, min_val, max_val)
    return {
        "product_id": request.product_id,
        "reconstruction_error": error,
        "is_anomaly": error > THRESHOLD,
        "threshold": THRESHOLD
    }