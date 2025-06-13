# config/settings.py
import os

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/ecommerce")
    INVENTORY_API_URL = os.getenv("INVENTORY_API_URL", "https://inventory.example.com/api/v1")
    INVENTORY_API_KEY = os.getenv("INVENTORY_API_KEY", "default-key")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "default-access-key")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "default-secret-key")
    S3_CATALOG_BUCKET = os.getenv("S3_CATALOG_BUCKET", "product-catalog")
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "https://hooks.slack.com/services/xxx/yyy/zzz")

settings = Settings()


# db/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from config.settings import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# db/models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, func
from db.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True)


# schemas/product.py
from pydantic import BaseModel, validator
from typing import Optional
import re

class ProductCreate(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int
    category_id: int
    is_active: bool = True
    
    @validator('sku')
    def validate_sku(cls, v):
        if not re.match(r'^[A-Z0-9]{6,12}$', v):
            raise ValueError('SKU must be 6-12 alphanumeric characters')
        return v
    
    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than zero')
        return v
    
    @validator('stock_quantity')
    def validate_stock(cls, v):
        if v < 0:
            raise ValueError('Stock quantity cannot be negative')
        return v


class ProductResponse(BaseModel):
    id: int
    sku: str
    name: str
    description: Optional[str]
    price: float
    stock_quantity: int
    category_id: int
    is_active: bool

    class Config:
        orm_mode = True


# repositories/product_repository.py
from sqlalchemy.orm import Session
from db.models import Product, Category
from typing import Optional

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_product_by_sku(self, sku: str) -> Optional[Product]:
        return self.db.query(Product).filter(Product.sku == sku).first()
    
    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == category_id).first()
    
    def create_product(self, product_data: dict) -> Product:
        product = Product(**product_data)
        self.db.add(product)
        return product

# services/inventory_service.py
import requests
import logging
from datetime import datetime
from config.settings import settings

class InventoryService:
    @staticmethod
    async def update_external_inventory(sku: str, quantity: int):
        try:
            inventory_payload = {
                "sku": sku,
                "quantity": quantity,
                "timestamp": datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{settings.INVENTORY_API_URL}/update-inventory",
                headers={"Authorization": f"Bearer {settings.INVENTORY_API_KEY}"},
                json=inventory_payload,
                timeout=5
            )
            response.raise_for_status()
            return True
        except Exception as e:
            logging.error(f"Failed to update inventory system: {str(e)}")
            return False


# services/storage_service.py
import boto3
import json
import logging
from datetime import datetime
from config.settings import settings

class S3StorageService:
    @staticmethod
    async def update_product_catalog(product_data: dict):
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            
            catalog_data = {
                "operation": "product_added",
                "product_data": product_data,
                "timestamp": datetime.now().isoformat()
            }
            
            s3_client.put_object(
                Bucket=settings.S3_CATALOG_BUCKET,
                Key=f"catalog-updates/{product_data['sku']}.json",
                Body=json.dumps(catalog_data)
            )
            return True
        except Exception as e:
            logging.error(f"Failed to update product catalog in S3: {str(e)}")
            return False


# services/notification_service.py
import requests
import logging
from config.settings import settings

class NotificationService:
    @staticmethod
    async def send_slack_notification(message: str):
        try:
            slack_payload = {"text": message}
            response = requests.post(
                settings.SLACK_WEBHOOK_URL, 
                json=slack_payload, 
                timeout=3
            )
            response.raise_for_status()
            return True
        except Exception as e:
            logging.error(f"Failed to send Slack notification: {str(e)}")
            return False


# services/product_service.py
import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.product import ProductCreate
from repositories.product_repository import ProductRepository
from services.inventory_service import InventoryService
from services.storage_service import S3StorageService
from services.notification_service import NotificationService

class ProductService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
        self.db = db
    
    def create_product(self, product_data: ProductCreate):
        # Check if product SKU already exists
        if self.repository.get_product_by_sku(product_data.sku):
            raise HTTPException(status_code=400, detail="Product with this SKU already exists")
        
        # Check if category exists
        if not self.repository.get_category_by_id(product_data.category_id):
            raise HTTPException(status_code=404, detail="Category not found")
        
        # Business logic
        if product_data.stock_quantity < 5:
            logging.warning(f"Low initial stock for product {product_data.sku}: {product_data.stock_quantity} units")
        
        # Create product object
        product_dict = product_data.dict()
        new_product = self.repository.create_product(product_dict)
        
        try:
            # Commit changes
            self.db.commit()
            self.db.refresh(new_product)
            
            # Convert to response format
            product_response = {
                "id": new_product.id,
                "sku": new_product.sku,
                "name": new_product.name,
                "description": new_product.description,
                "price": new_product.price,
                "stock_quantity": new_product.stock_quantity,
                "category_id": new_product.category_id,
                "is_active": new_product.is_active
            }
            
            return product_response
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# routes/product_routes.py
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from schemas.product import ProductCreate, ProductResponse
from services.product_service import ProductService
from services.inventory_service import InventoryService
from services.storage_service import S3StorageService
from services.notification_service import NotificationService
from db.database import get_db

router = APIRouter(prefix="/products", tags=["products"])

def process_background_tasks(
    product_data: dict,
):
    # Update external inventory system
    InventoryService.update_external_inventory(
        product_data["sku"], 
        product_data["stock_quantity"]
    )
    
    # Update S3 catalog
    S3StorageService.update_product_catalog(product_data)
    
    # Send Slack notification
    NotificationService.send_slack_notification(
        f"New product added: {product_data['name']} (SKU: {product_data['sku']}) with {product_data['stock_quantity']} units in stock."
    )


@router.post("/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Use service layer to handle business logic
    product_service = ProductService(db)
    new_product = product_service.create_product(product)
    
    # Schedule background tasks
    background_tasks.add_task(
        process_background_tasks,
        product_data=new_product
    )
    
    return new_product


# main.py
from fastapi import FastAPI
from routes import product_routes
import logging

# Configure logging (can be in different module)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(title="E-commerce Product API")


# Register routes
app.include_router(product_routes.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
