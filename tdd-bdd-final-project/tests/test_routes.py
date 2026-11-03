import unittest
from service import create_app, db


class ProductRouteTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://"})
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_product(self, name="Pen"):
        return self.client.post("/products", json={
            "name": name, "description": "Blue ink", "price": 2.5,
            "category": "Stationery", "available": True
        })

    def test_create_and_read(self):
        response = self.create_product()
        self.assertEqual(response.status_code, 201)
        product_id = response.get_json()["id"]
        read = self.client.get(f"/products/{product_id}")
        self.assertEqual(read.status_code, 200)
        self.assertEqual(read.get_json()["name"], "Pen")

    def test_update(self):
        created = self.create_product()
        product_id = created.get_json()["id"]
        response = self.client.put(f"/products/{product_id}", json={"description": "Black ink"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["description"], "Black ink")

    def test_delete(self):
        created = self.create_product()
        product_id = created.get_json()["id"]
        response = self.client.delete(f"/products/{product_id}")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, b"")
        self.assertEqual(self.client.get(f"/products/{product_id}").status_code, 404)

    def test_list_and_filters(self):
        self.create_product("Pen")
        self.create_product("Pencil")
        self.assertEqual(len(self.client.get("/products").get_json()), 2)
        self.assertEqual(len(self.client.get("/products?category=Stationery").get_json()), 2)
        self.assertEqual(len(self.client.get("/products?available=true").get_json()), 2)


if __name__ == "__main__":
    unittest.main()
