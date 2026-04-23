from fastapi import Depends, FastAPI
from models import Product, User
import database_models
from database import session, engine
from sqlalchemy.orm import Session
from auth_api import router as auth_router
from product_api import router as product_router

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

@app.get('/')
def greet():
    return "welconme to the krishna world"


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(product_router, prefix="/api", tags=["Product"])


products = [
    Product(id=1, name="laptop", description="laptop", price=49.9, quantity=10 ),
    Product(id=2, name="mobile", description="mobile", price=49.9, quantity=10 ),
]

def init_db():
    db = session()

    count = db.query(database_models.Product).count()
    if count== 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

        db.commit()


init_db()
