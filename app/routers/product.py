from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app import database
from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter()

# CREATE
@router.post("/", response_model=ProductResponse)
def create_product(request: ProductCreate, db: Session = Depends(database.get_db)):
    new_product = Product(**request.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# READ (dengan filter, pencarian, sorting, dan pagination)
@router.get("/")
def get_all_product(
    db: Session = Depends(database.get_db),
    keyword: str | None = Query(None, description="Search by name or category"),
    category: str | None = Query(None, description="Filter by category"),
    min_price: float | None = Query(None, description="Minimum price"),
    max_price: float | None = Query(None, description="Maksimum price"),
    sort_by: str | None = Query(None, description="Sort column: name, price, category"),
    sort_order: str | None = Query("asc", description="Sort: asc or desc"),
    page: int = Query(1, ge=1, description="Page number (start from 1)"),
    limit: int = Query(10, ge=1, le=100, description="Total item per page"),
):
    query = db.query(Product)

    # Filter pencarian bebas
    if keyword:
        query = query.filter(or_(
            Product.name.ilike(f"%{keyword}%"),
            Product.category.ilike(f"%{keyword}%")
        ))

    # Filter category
    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))

    # Filter price
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    # Hitung total sebelum pagination
    total_items = query.count()

    # Sorting
    if sort_by in ["name", "price", "category"]:
        sort_column = getattr(Product, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)

    # Pagination
    offset = (page - 1) * limit
    items = query.offset(offset).limit(limit).all()

    total_pages = (total_items + limit - 1) // limit if total_items else 1

    return {
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": page,
        "items": items
    }


# READ (by id)
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(database.get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# UPDATE
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, request: ProductUpdate, db: Session = Depends(database.get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in request.dict().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


# DELETE
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(database.get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"status": "success", "message": "Product deleted"}
