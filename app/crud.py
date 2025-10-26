from sqlalchemy.orm import Session
from app.models import Product

def create_product(db: Session, name: str, category: str, price: float, image_path: str = None):
    product = Product(name=name, category=category, price=price, image_path=image_path)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def list_products(db: Session, skip=0, limit=10, search=None):
    query = db.query(Product)
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def update_product(db: Session, product_id: int, name: str, category: str, price: float, image_path: str = None):
    product = get_product(db, product_id)
    if not product:
        return None
    product.name = name
    product.category = category
    product.price = price
    if image_path:
        product.image_path = image_path
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if product:
        db.delete(product)
        db.commit()
