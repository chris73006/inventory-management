from fastapi import APIRouter, FastAPI, Depends, HTTPException, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
import logging

from src import models, schemas
from src.database import engine, get_db
from src.schemas import ProductCreate, ProductResponse, ProductUpdate, StockResponse
from .models import Product, Stock

# ✅ Initialize Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Initialize FastAPI
app = FastAPI()
router = APIRouter()

# ✅ Serve Static Files & Templates
app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

# ✅ Ensure database tables exist
models.Base.metadata.create_all(bind=engine)

# ✅ CORS Middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ POST: Create Product
@app.post("/products/", response_model=ProductResponse)
def create_product(
    product_data: ProductCreate = Body(...),
    db: Session = Depends(get_db)
):
    logger.info("🚀 Received Data: %s", product_data.dict())

    if not product_data.name or product_data.price is None or product_data.stock is None:
        raise HTTPException(status_code=400, detail="Product name, price, and stock are required.")

    if product_data.price < 0 or product_data.stock < 0:
        raise HTTPException(status_code=400, detail="Price and stock must be non-negative values.")

    new_product = Product(**product_data.dict())

    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        logger.info("✅ Product stored successfully in the database.")
    except Exception as e:
        db.rollback()
        logger.error("❌ Database error: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    return ProductResponse.from_orm(new_product)

# ✅ GET: Fetch Products
@app.get("/products/", response_model=List[ProductResponse])
def get_products(
    request: Request,
    name: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,
    sort_by: str = "name",
    order: str = "asc",
    db: Session = Depends(get_db)
):
    try:
        db.execute(text("SELECT 1"))
        logger.info("✅ Database connection successful.")

        query = db.query(Product)

        if name:
            query = query.filter(Product.name.ilike(f"%{name}%"))

        valid_sort_fields = ["name", "price", "stock", "discount_percentage"]
        if sort_by not in valid_sort_fields:
            raise HTTPException(status_code=400, detail=f"Invalid sort_by field '{sort_by}', must be one of {valid_sort_fields}")

        order_by_field = getattr(Product, sort_by, None)
        if not order_by_field:
            raise HTTPException(status_code=400, detail=f"Invalid sort field: {sort_by}")

        query = query.order_by(order_by_field.asc() if order == "asc" else order_by_field.desc())
        products = query.offset(offset).limit(limit).all()

        if not products:
            logger.warning("⚠️ No products found.")
            raise HTTPException(status_code=404, detail="No products found.")

        logger.info(f"📦 Retrieved {len(products)} products from database.")

        return [ProductResponse.from_orm(product) for product in products]

    except Exception as e:
        logger.error("❌ Database connection failed: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# ✅ GET: Fetch Stocks
@app.get("/stocks/", response_model=List[StockResponse])
def get_stocks(
    request: Request,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    try:
        db.execute(text("SELECT 1"))
        logger.info("✅ Database connection successful.")

        stocks = db.query(Stock).offset(offset).limit(limit).all()

        if not stocks:
            logger.warning("⚠️ No stock records found.")
            raise HTTPException(status_code=404, detail="No stock records found.")

        logger.info(f"📦 Retrieved {len(stocks)} stock entries from database.")
        return [StockResponse.from_orm(stock) for stock in stocks]

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        logger.error("❌ Database query failed: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Error retrieving stocks: {str(e)}")

# ✅ PUT: Update Product
@app.put("/products/{id}", response_model=ProductResponse)
def update_product(id: int, updated_product: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = updated_product.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields provided for update")

    for key, value in update_data.items():
        setattr(product, key, value)

    try:
        db.commit()
        db.refresh(product)
        logger.info("✅ Product updated successfully.")
    except Exception as e:
        db.rollback()
        logger.error("❌ Update error: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Database update failed: {str(e)}")

    return ProductResponse.from_orm(product)

# ✅ DELETE: Remove Product
@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    try:
        db.delete(product)
        db.commit()
        logger.info(f"🗑️ Deleted product {id}.")
    except Exception as e:
        db.rollback()
        logger.error("❌ Deletion error: %s", str(e))
        raise HTTPException(status_code=500, detail=f"Product deletion failed: {str(e)}")

    return {"message": "Product deleted successfully"}

