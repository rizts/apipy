from pydantic import BaseModel

class ProductDB(BaseModel):
    id: int
    name: str
    category: str
    price: float
