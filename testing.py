# pytest testing.py -vv -x
# -vv shows extended information
# -x makes it stop as soon as one test fails

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_add_item():

    response = client.post("/add-item", json={"name": "Bread", "quantity": 1})
    assert response.status_code == 200
    assert response.json() == {"msg": "Bread was added"}


def test_full_list():
    response = client.get("/get-full-list")
    assert response != None


def test_get_item_by_index(name="Bread", quantity=1):
    response = client.get("/get-by-index/0")
    assert response.status_code == 200
    assert response.json() == {"name": name, "quantity": quantity}
    return True


def test_get_item_by_name():
    response = client.get("/get-by-name?name=Bread")
    assert response.status_code == 200
    assert response.json() == {"name": "Bread", "quantity": 1}
    response = client.get("/get-by-name?name=Banana")
    assert response.status_code == 404
    assert response.json() == {"detail": f"Banana not found"}


def test_item_change():
    changes = {"name": "Tomatoes", "quantity": 14}
    response = client.put("/update-item?name=Bread", json=changes)
    assert response.status_code == 200
    assert test_get_item_by_index("Tomatoes", 14)


def test_item_delete():
    response = client.delete("/delete-item?name=Tomatoes")
    assert response.status_code == 200
    assert response.json() == "Deleted Tomatoes from your list"
