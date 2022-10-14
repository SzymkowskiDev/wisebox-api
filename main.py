import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from schemas import Item as SchemaItem
from schemas import Magazine as SchemaMagazine

from schemas import Item
from schemas import Magazine

from models import Item as ModelItem
from models import Magazine as ModelMagazine

import os
from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.post('/item/', response_model=SchemaItem)
async def item(item: SchemaItem):
    db_item = ModelItem(product=item.product, quantity=item.quantity, price=item.price, location=item.location, status=item.status, magazine_id=item.magazine_id)
    db.session.add(db_item)
    db.session.commit()
    return db_item


@app.get('/item/')
async def item():
    item = db.session.query(ModelItem).all()
    return item


@app.post('/magazine/', response_model=SchemaMagazine)
async def magazine(magazine: SchemaMagazine):
    db_magazine = ModelMagazine(name=magazine.name, description=magazine.description, avatar=magazine.avatar, location=magazine.location)
    db.session.add(db_magazine)
    db.session.commit()
    return db_magazine


@app.get('/magazine/')
async def magazine():
    magazine = db.session.query(ModelMagazine).all()
    return magazine


# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)