from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., example="Tamarind Herbal Medicine")
    category: str = Field(..., example="Traditional Drinks")
    price: float = Field(..., example=15000.0)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    image_path: Optional[str] = None

    class Config:
        from_attributes = True

Product = ProductResponse