from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Product, BrassPrice, ScrapInventory

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ayastra API")

# Dependency — opens and closes DB connection per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- INVENTORY ENDPOINTS ---

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.put("/products/{product_id}/stock")
def update_stock(product_id: int, quantity: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.stock = quantity
    db.commit()
    return {"message": "Stock updated", "product": product.name, "new_stock": quantity}

# --- BRASS PRICE ENDPOINTS ---

@app.get("/brass-prices")
def get_brass_prices(db: Session = Depends(get_db)):
    return db.query(BrassPrice).order_by(BrassPrice.recorded_at).all()

@app.post("/brass-prices")
def add_brass_price(price: float, db: Session = Depends(get_db)):
    new_price = BrassPrice(price_per_kg=price)
    db.add(new_price)
    db.commit()
    return {"message": "Price recorded", "price_per_kg": price}

# --- SCRAP OPTIMIZER ENDPOINT ---

@app.get("/scrap/recommendation")
def scrap_recommendation(db: Session = Depends(get_db)):
    prices = db.query(BrassPrice).order_by(BrassPrice.recorded_at).all()
    if len(prices) < 2:
        return {"recommendation": "Not enough data yet"}
    
    latest = prices[-1].price_per_kg
    avg = sum(p.price_per_kg for p in prices) / len(prices)
    
    if latest > avg * 1.02:
        action = "SELL"
        reason = f"Current price ₹{latest} is above average ₹{avg:.0f} — good time to sell"
    else:
        action = "WAIT"
        reason = f"Current price ₹{latest} is below average ₹{avg:.0f} — wait for better rate"
    
    return {"action": action, "reason": reason, "current_price": latest, "7day_avg": round(avg, 2)}