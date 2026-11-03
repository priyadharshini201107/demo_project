import unittest
from service import create_app, db
from service.models import Product
from tests.factories import ProductFactory


class ProductModelTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://"})
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_create_and_read(self):
        product = ProductFactory.make(name="Keyboard", description="USB keyboard", price=25.5)
        db.session.add(product)
        db.session.commit()
        found = Product.find(product.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.name, "Keyboard")
        self.assertEqual(found.description, "USB keyboard")
        self.assertEqual(found.price, 25.5)

    def test_update_description(self):
        product = ProductFactory.make(name="Mouse", description="Old")
        db.session.add(product)
        db.session.commit()
        original_id = product.id
        product.description = "Wireless mouse"
        db.session.commit()
        found = Product.find(original_id)
        self.assertEqual(found.id, original_id)
        self.assertEqual(found.description, "Wireless mouse")

    def test_delete(self):
        product = ProductFactory.make()
        db.session.add(product)
        db.session.commit()
        before = Product.query.count()
        db.session.delete(product)
        db.session.commit()
        self.assertEqual(Product.query.count(), before - 1)

    def test_list_all(self):
        self.assertEqual(Product.query.count(), 0)
        db.session.add_all([ProductFactory.make(), ProductFactory.make()])
        db.session.commit()
        self.assertEqual(Product.query.count(), 2)

    def test_find_by_name_category_availability(self):
        db.session.add_all([
            ProductFactory.make(name="Pen", category="Stationery", available=True),
            ProductFactory.make(name="Pen", category="Stationery", available=False),
            ProductFactory.make(name="Book", category="Books", available=True),
        ])
        db.session.commit()
        self.assertEqual(len(Product.find_by_name("Pen")), 2)
        self.assertEqual(len(Product.find_by_category("Stationery")), 2)
        self.assertEqual(len(Product.find_by_availability(True)), 2)


if __name__ == "__main__":
    unittest.main()
