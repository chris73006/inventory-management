from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime
class ProductCreate(BaseModel):

    name: str
    category: str = "Uncategorized"
    price: float
    stock:int
    discount_percentage: float = 0.0  # ✅ Added
    seller_name: Optional[str]="Unknown"  # ✅ Added
    seller_contact: Optional[str]="N/A"  # ✅ Added

    class Config:
        from_attributes = True  # ✅ Enables SQLAlchemy conversion

class ProductResponse(BaseModel):
   
    name: str
    price: float
    stock: int
    discount_percentage: Optional[float] = 0.0  # ✅ Provide default value
    seller_name: Optional[str] = "Unknown"  # ✅ Provide default value
    seller_contact: Optional[str] = "N/A"  # ✅ Provide default value

    


    class Config:
        from_attributes = True 

class ProductUpdate(BaseModel):
    name: Optional[str]  # ✅ Corrected type hint
    category: Optional[str]  # ✅ Category added

    price: Optional[float]  # ✅ Corrected type hint
    stock: Optional[int]  # ✅ Corrected type hint
    discount_percentage: Optional[float]  # ✅ Corrected type hint
    seller_name: Optional[str]  # ✅ Allows updates without errors
    seller_contact: Optional[str]  # ✅ Allows updates without errors

    class Config:
        from_attributes = True  # ✅ Consistent placement
from pydantic import BaseModel, Field

class StockResponse(BaseModel):
    
    id: int
    product_name: str
    quantity: int
    price_per_unit: float
    last_updated:datetime


    class Config:
        from_attributes = True