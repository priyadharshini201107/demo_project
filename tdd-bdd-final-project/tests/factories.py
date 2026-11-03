from faker import Faker
from service.models import Product

fake = Faker()


class ProductFactory:
    @staticmethod
    def make(**kwargs):
        values = {
            "name": fake.word().title(),
            "description": fake.sentence(),
            "price": round(fake.pyfloat(min_value=1, max_value=500, right_digits=2), 2),
            "category": fake.word().title(),
            "available": fake.pybool(),
        }
        values.update(kwargs)
        return Product(**values)
