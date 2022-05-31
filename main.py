# uvicorn main:app --reload

from __future__ import annotations
from unicodedata import name
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

shopping_list: dict[int, dict] = {}


class NewItem(BaseModel):
    name: str
    quantity: int


@app.get("/")
async def read_main():
    return {"msg": "Hello"}


@app.get("/get-by-index/{item_index}")
async def get_by_index(item_index: int):
    return shopping_list[item_index]


async def get_index_by_name(name: str):
    item_index = None
    for item in shopping_list:
        if shopping_list[item]["name"] == name:
            item_index = item
            break

    if item_index == None:
        raise HTTPException(status_code=404, detail=f"{name} not found")
    else:
        return item_index


@app.get("/get-by-name")
async def get_by_name(name: str):
    item = await get_index_by_name(name)
    return shopping_list[item]


@app.get("/get-full-list")
async def get_full_list():
    return shopping_list


@app.post("/add-item")
async def add_item(new_item: NewItem):
    for i in shopping_list:
        if shopping_list[i]["name"] == new_item.name:
            return {"msg": f"{new_item.name} already in list"}

    shopping_list[len(shopping_list)] = new_item.dict()
    return {"msg": f"{new_item.name} was added"}


@app.put("/update-item")
async def update_item(name: str, item_changes: NewItem):
    item_to_change = shopping_list[await get_index_by_name(name)]
    if item_changes.name != None:
        item_to_change["name"] = item_changes.name
    if item_changes.quantity != None:
        item_to_change["quantity"] = item_changes.quantity

    return {"msg": f"{item_to_change} changed"}


@app.delete("/delete-item")
async def delete_item(name: str):
    del shopping_list[await get_index_by_name(name)]
    return f"Deleted {name} from your list"


if __name__ == "__main__":
    pass
