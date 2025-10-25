from fastapi import FastAPI, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base
import crud, schemas, os, shutil, uuid
from fastapi.staticfiles import StaticFiles
import glob

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Product API")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_upload_file(upload_file: UploadFile, upload_dir: str) -> str:
    """
    Stor uploaded to folder and return path.
    File name created uniquely (use UUID).
    """
    ext = os.path.splitext(upload_file.filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png"]:
        raise HTTPException(status_code=400, detail="File must be JPG or PNG")

    unique_name = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(upload_dir, unique_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return file_path


@app.post("/products/", response_model=schemas.Product)
def create_product(
    name: str = Form(...),
    category: str = Form(None),
    price: float = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    image_path = None
    if file:
        image_path = save_upload_file(file, UPLOAD_DIR)

    product = crud.create_product(db, name=name, category=category, price=price, image_path=image_path)

    # Tambahkan URL image
    if product.image_path:
        product.image_path = f"/uploads/{os.path.basename(product.image_path)}"

    return product


@app.get("/products/", response_model=list[schemas.Product])
def list_products(skip: int = 0, limit: int = 10, search: str = None, db: Session = Depends(get_db)):
    products = crud.list_products(db, skip=skip, limit=limit, search=search)
    for p in products:
        if p.image_path:
            p.image_path = f"/uploads/{os.path.basename(p.image_path)}"
    return products


@app.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.image_path:
        product.image_path = f"/uploads/{os.path.basename(product.image_path)}"
    return product


@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int,
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    image_path = None
    if file:
        # Delete old if exist
        if product.image_path:
            old_file_path = os.path.join(UPLOAD_DIR, os.path.basename(product.image_path))
            if os.path.exists(old_file_path):
                os.remove(old_file_path)

        # Store new file
        image_path = save_upload_file(file, UPLOAD_DIR)

    product = crud.update_product(db, product_id, name, description, price, image_path)

    if product.image_path:
        product.image_path = f"/uploads/{os.path.basename(product.image_path)}"

    return product


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    crud.delete_product(db, product_id)
    return {"message": "Deleted successfully"}


@app.post("/cleanup-uploads")
def cleanup_uploads(db: Session = Depends(get_db)):
    """
    Delete related files in uploads folder.
    """
    # Get all products image_path produk in database
    products = db.query(crud.Product).all()
    used_files = set()
    for p in products:
        if p.image_path:
            used_files.add(os.path.basename(p.image_path))

    # Get all files in uploads folder
    all_files = glob.glob(os.path.join(UPLOAD_DIR, "*"))

    deleted_files = []
    for file_path in all_files:
        filename = os.path.basename(file_path)
        if filename not in used_files:
            os.remove(file_path)
            deleted_files.append(filename)

    return {"deleted_files": deleted_files, "message": "Cleanup finishd"}
