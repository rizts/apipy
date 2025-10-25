from fastapi import FastAPI
from app.routers import product

app = FastAPI(
    title="API Herbal Medicine",
    description="Sample CRUD API Herbal Medicine products with automatic Swagger documentation.",
    version="1.0.0"
)

# Register router
app.include_router(product.router, prefix="/product", tags=["Product"])

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Welcome to SEM Herbal Medicine API"}
