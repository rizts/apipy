from fastapi import APIRouter, HTTPException
from app.schemas.product_schema import Product, ProductResponse
from app.models.product_model import ProductDB

router = APIRouter()

# Simulate temporary database
fake_db = []

@router.post("/", response_model=ProductResponse)
def create_product(product: Product):
    """Add new herbal medicine product"""
    new_id = len(fake_db) + 1
    product_data = ProductDB(id=new_id, **product.dict())
    fake_db.append(product_data)
    return {"status": "success", "data": product_data}

@router.get("/", response_model=list[ProductResponse])
def list_product():
    """List all of herbal medicine products"""
    return [{"status": "success", "data": p} for p in fake_db]

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    """Get detailed product by ID"""
    for p in fake_db:
        if p.id == product_id:
            return {"status": "success", "data": p}
    raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/{product_id}")
def delete_product(product_id: int):
    """Delete product by ID"""
    for i, p in enumerate(fake_db):
        if p.id == product_id:
            fake_db.pop(i)
            return {"status": "success", "message": "Product deleted"}
    raise HTTPException(status_code=404, detail="Product not found")
