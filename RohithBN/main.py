from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

items = []

@app.get("/")
async def root():
    with open("static/index.html", "r") as file:
        return HTMLResponse(content=file.read(), status_code=200)

@app.get("/items", response_model=List[Item])
async def get_items():
    return items

@app.post("/items")
async def create_item(item: Item):
    items.append(item)
    return {"message": "Item added successfully", "item": item}
