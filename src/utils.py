import random
from typing import List

from faker import Faker, providers

PRODUCTS = [
    "CozyCloud Memory Foam Pillow",
    "HyperDrive Wireless Charger",
    "AquaStream Water Purifier",
    "FlexStep Fitness Tracker",
    "BrilliantBeam LED Projector",
    "GourmetNation Coffee Maker",
    "WhisperCalm Noise-Cancelling Headphones",
    "SnapShot Instant Camera",
    "EverBloom Indoor Herb Garden Kit",
    "StreamLine Laptop Backpack",
    "CrispView Air Purifier",
    "SmartLock Fingerprint Door Lock",
    "SolarCharge Portable Phone Charger",
    "AromaLux Essential Oil Diffuser",
    "GripTight Smartphone Gimbal",
    "HarmonyStream Meditation App Subscription",
    "CulinaryCraft Stainless Steel Cookware Set",
    "BreezeAir Portable Air Conditioner",
    "NightLite Smart Lamp",
]


class ProductNameProvider(providers.BaseProvider):

    def product_name(self):
        return random.choice(PRODUCTS)


fake = Faker()
fake.add_provider(ProductNameProvider)


def generate_customer_order(num_items=1):
    """
        Generates a fake customer order with basic details.
    Sonic ",",Electric Toothbrush

        Args:
            num_items (int, optional): Number of items in the order. Defaults to 1.

        Returns:
            dict: A dictionary representing a fake customer order.
    """
    customer = {
        "name": fake.name(),
        "email": fake.email(),
        "address": fake.address(),
    }
    order = {"customer": customer, "order_id": fake.pyint(), "items": []}
    for _ in range(num_items):
        # Generate basic product details
        product = {
            "name": fake.product_name(),
            "price": round(
                random.uniform(10, 100), 2
            ),  # Random price between $10 and $100
            "quantity": random.randint(
                1, 3
            ),  # Random quantity between 1 and 3
        }
        order["items"].append(product)
    return order


def generate_orders(num_orders=10) -> List[dict]:
    """
    Generates a list of fake customer orders.

    Args:
        num_orders (int, optional): Number of orders to generate. Defaults to 10.

    Returns:
        list: A list of dictionaries representing fake customer orders.
    """
    orders = []
    for _ in range(num_orders):
        # Randomly choose number of items between 1 and 5
        num_items = random.randint(1, 5)
        orders.append(generate_customer_order(num_items))

    return orders
