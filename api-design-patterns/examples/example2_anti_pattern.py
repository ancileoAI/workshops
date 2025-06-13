import json
import logging
import re
import os
from typing import Optional
from datetime import datetime

import requests
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import boto3

app = FastAPI()
Base = declarative_base()
engine = create_engine(os.getenv(
    "DATABASE_URL", "postgresql://user:password@localhost:5432/ecommerce"))


def SessionLocal(): return Session(bind=engine)

# Database models
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


# Pydantic models
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


# The anti-pattern route - everything in one function
@app.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, request: Request):
    # Get database session
    db = SessionLocal()

    try:
        # Manually check if SKU already exists
        existing_product = db.query(Product).filter(
            Product.sku == product.sku).first()
        if existing_product:
            db.close()
            raise HTTPException(
                status_code=400, detail="Product with this SKU already exists")

        # Check if category exists
        category = db.query(Category).filter(
            Category.id == product.category_id).first()
        if not category:
            db.close()
            raise HTTPException(status_code=404, detail="Category not found")

        # Business logic to check inventory threshold
        if product.stock_quantity < 5:
            logging.warning(
                f"Low initial stock for product {product.sku}: {product.stock_quantity} units")

        # Create product record
        new_product = Product(
            sku=product.sku,
            name=product.name,
            description=product.description,
            price=product.price,
            stock_quantity=product.stock_quantity,
            category_id=product.category_id,
            is_active=product.is_active
        )

        # Add to database
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        # Format response data
        response_data = {
            "id": new_product.id,
            "sku": new_product.sku,
            "name": new_product.name,
            "description": new_product.description,
            "price": new_product.price,
            "stock_quantity": new_product.stock_quantity,
            "category_id": new_product.category_id,
            "is_active": new_product.is_active
        }

        # Synchronous call to third-party inventory system API
        try:
            inventory_api_url = os.getenv(
                "INVENTORY_API_URL", "https://inventory.example.com/api/v1")
            inventory_api_key = os.getenv("INVENTORY_API_KEY", "default-key")

            inventory_payload = {
                "sku": new_product.sku,
                "quantity": new_product.stock_quantity,
                "timestamp": datetime.now().isoformat()
            }

            requests.post(
                f"{inventory_api_url}/update-inventory",
                headers={"Authorization": f"Bearer {inventory_api_key}"},
                json=inventory_payload,
                timeout=5
            )
        except Exception as e:
            logging.error(f"Failed to update inventory system: {str(e)}")
            # Continue despite error - no retry mechanism

        # Synchronous call to AWS S3 for product catalog update
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv(
                    "AWS_ACCESS_KEY_ID", "default-access-key"),
                aws_secret_access_key=os.getenv(
                    "AWS_SECRET_ACCESS_KEY", "default-secret-key")
            )

            catalog_data = {
                "operation": "product_added",
                "product_data": response_data,
                "timestamp": datetime.now().isoformat()
            }

            s3_client.put_object(
                Bucket=os.getenv("S3_CATALOG_BUCKET", "product-catalog"),
                Key=f"catalog-updates/{new_product.sku}.json",
                Body=json.dumps(catalog_data)
            )
        except Exception as e:
            logging.error(f"Failed to update product catalog in S3: {str(e)}")
            # Continue despite error

        # Synchronous notification to Slack
        try:
            slack_webhook = os.getenv(
                "SLACK_WEBHOOK_URL", "https://hooks.slack.com/services/xxx/yyy/zzz")
            slack_payload = {
                "text": f"New product added: {new_product.name} (SKU: {new_product.sku}) with {new_product.stock_quantity} units in stock."
            }

            requests.post(slack_webhook, json=slack_payload, timeout=3)
        except Exception as e:
            logging.error(f"Failed to send Slack notification: {str(e)}")
            # Continue despite error

        return response_data

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}")

    finally:
        db.close()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
