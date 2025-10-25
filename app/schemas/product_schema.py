from pydantic import BaseModel, Field

class Product(BaseModel):
    nama: str = Field(..., example="Tamarind Herbal Medicine")
    category: str = Field(..., example="Traditional Drinks")
    price: float = Field(..., example=15000.0)

class ProductResponse(BaseModel):
    status: str
    data: Product | None = None
