from fastapi import APIRouter, Depends
from models import ProductCreate, ProductUpdate
import database_models
from database import get_db
from sqlalchemy.orm import Session
from auth_token import get_current_user

router = APIRouter()

@router.get("/products")
def get_all_products(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_products = db.query(database_models.Product).all()
    return db_products

@router.get("/product/{id}")
def get_product(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    else:
        return "Product not found"

@router.post("/product")
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return "Product added successfully"

@router.put("/product")
def update_product(id: int, product: ProductUpdate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product updated successfully"
    else:
         return "Product not found"

@router.delete("/product")
def delete_product(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted successfully"
    else:
        return "Product not found"
