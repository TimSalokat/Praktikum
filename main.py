#uvicorn main:app --reload

from __future__ import annotations
from unicodedata import name
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

shopping_list:dict[int, dict] = {
    # 0: {
    #     "name": "Apples",
    #     "quantity" : "4"
    # },
    # 1: {
    #     "name": "Bread",
    #     "quantity": "1"
    # },
    # 2: {
    #     "name": "Orange Juice",
    #     "quantity": "2"
    # }

}

class NewItem(BaseModel):
    name: str
    quantity: int

@app.get("/")
async def read_main():
    return {"msg": "Hello"}

@app.get("/get-by-index/{item_index}")
async def get_by_index(item_index: int):
    return shopping_list[item_index]


@app.get("/get-by-name")
async def get_by_name(name: str):
    for item in shopping_list:
        if shopping_list[item]["name"] == name:
            return shopping_list[item]
    raise HTTPException(status_code=404, detail=f"{name} not found")

@app.get("/get-full-list")
async def get_full_list():
    return shopping_list

@app.post("/add-item")
async def add_item(new_item : NewItem):
    for i in shopping_list:
        if(shopping_list[i]["name"] == new_item.name):
            return {"msg": f"{new_item.name} already in list"}

    shopping_list[len(shopping_list)] = new_item.dict()
    return {"msg": f"{new_item.name} was added"}
    # return shopping_list[len(shopping_list) - 1]

if __name__ == "__main__":
    pass
