import json

import products
from cart import dao
from products import Product


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> list:
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    items = []
    for cart_detail in cart_details:
        # Safely parse the JSON contents instead of eval
        contents = json.loads(cart_detail['contents'])
        items.extend(contents)

    # Fetch products in a single call to reduce database hits
    unique_product_ids = list(set(items))
    products_map = {product.id: product for product in products.get_products(unique_product_ids)}
    
    # Map the product objects back to the original order
    cart_products = [products_map[product_id] for product_id in items if product_id in products_map]
    return cart_products


def add_to_cart(username: str, product_id: int):
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    dao.delete_cart(username)
