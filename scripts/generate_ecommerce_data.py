import csv
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

NUM_ROWS = 200
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

FIRST_NAMES = [
    "Ava",
    "Ethan",
    "Sophia",
    "Liam",
    "Isabella",
    "Noah",
    "Mia",
    "Lucas",
    "Charlotte",
    "Amelia",
]

LAST_NAMES = [
    "Johnson",
    "Smith",
    "Brown",
    "Garcia",
    "Martinez",
    "Davis",
    "Miller",
    "Wilson",
    "Moore",
    "Taylor",
]

STREETS = [
    "Oak Street",
    "Maple Avenue",
    "Cedar Lane",
    "Pine Drive",
    "Willow Way",
    "Sunset Boulevard",
    "Hillcrest Road",
    "Riverview Terrace",
    "Highland Court",
    "Birch Place",
]

CITIES = [
    "Austin",
    "Seattle",
    "Denver",
    "Chicago",
    "San Diego",
    "Boston",
    "Phoenix",
    "Atlanta",
    "Portland",
    "Miami",
]

STATES = ["TX", "WA", "CO", "IL", "CA", "MA", "AZ", "GA", "OR", "FL"]

PRODUCT_CATEGORIES = [
    "Electronics",
    "Home & Kitchen",
    "Sports",
    "Beauty",
    "Toys",
    "Books",
    "Clothing",
    "Outdoors",
    "Automotive",
    "Pet Supplies",
]

ORDER_STATUSES = ["Processing", "Shipped", "Delivered", "Cancelled", "Returned"]
PAYMENT_METHODS = ["Credit Card", "PayPal", "Apple Pay", "Google Pay", "Gift Card"]
LOYALTY_TIERS = ["Bronze", "Silver", "Gold", "Platinum"]


def random_date(within_days: int = 365) -> datetime:
    """Return a random datetime within the past 'within_days'."""
    return datetime.now() - timedelta(
        days=random.randint(0, within_days),
        seconds=random.randint(0, 24 * 60 * 60),
    )


def random_phone() -> str:
    return f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}"


def random_address() -> str:
    return f"{random.randint(100, 9999)} {random.choice(STREETS)}"


def suffix_email(text: str) -> str:
    return text.lower().replace(" ", "")


def generate_customers(num_rows: int):
    customers = []
    for i in range(num_rows):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        customer_id = f"C{1000 + i}"
        city = random.choice(CITIES)
        state_index = CITIES.index(city) if city in CITIES else 0
        state = STATES[state_index]
        signup_date = random_date(730)
        tier = random.choices(LOYALTY_TIERS, weights=[50, 30, 15, 5])[0]
        customers.append(
            {
                "customer_id": customer_id,
                "first_name": first,
                "last_name": last,
                "email": f"{suffix_email(first)}.{suffix_email(last)}{random.randint(10, 99)}@example.com",
                "phone": random_phone(),
                "address": random_address(),
                "city": city,
                "state": state,
                "zip_code": f"{random.randint(10000, 99999)}",
                "signup_date": signup_date.strftime("%Y-%m-%d"),
                "loyalty_tier": tier,
            }
        )
    return customers


def generate_products(num_rows: int):
    products = []
    for i in range(num_rows):
        category = random.choice(PRODUCT_CATEGORIES)
        price = round(random.uniform(5, 250), 2)
        cost = round(price * random.uniform(0.4, 0.8), 2)
        products.append(
            {
                "product_id": f"P{1000 + i}",
                "name": f"{category} Item {i + 1}",
                "category": category,
                "price": f"{price:.2f}",
                "cost": f"{cost:.2f}",
                "stock_qty": random.randint(10, 500),
                "is_active": random.choice(["True", "False"]),
                "created_at": random_date(540).strftime("%Y-%m-%d"),
            }
        )
    return products


def generate_orders(customers, products, num_rows: int):
    orders = []
    order_items = []
    payments = []

    for i in range(num_rows):
        order_id = f"O{2000 + i}"
        order_date = random_date(365)
        customer = random.choice(customers)
        product = random.choice(products)
        quantity = random.randint(1, 4)
        unit_price = float(product["price"])
        discount_rate = random.choice([0, 0.05, 0.1, 0.15])
        discount = round(unit_price * discount_rate, 2)
        line_total = round((unit_price - discount) * quantity, 2)
        tax = round(line_total * 0.07, 2)
        shipping_fee = round(random.choice([0, 3.99, 6.99, 9.99]), 2)
        subtotal = line_total
        total = round(subtotal + tax + shipping_fee, 2)
        status = random.choices(
            ORDER_STATUSES, weights=[40, 30, 20, 5, 5]
        )[0]
        payment_method = random.choice(PAYMENT_METHODS)

        orders.append(
            {
                "order_id": order_id,
                "customer_id": customer["customer_id"],
                "order_date": order_date.strftime("%Y-%m-%d"),
                "status": status,
                "subtotal": f"{subtotal:.2f}",
                "tax": f"{tax:.2f}",
                "shipping_fee": f"{shipping_fee:.2f}",
                "total": f"{total:.2f}",
                "payment_method": payment_method,
                "shipping_address": f'{customer["address"]}, {customer["city"]}, {customer["state"]} {customer["zip_code"]}',
            }
        )

        order_items.append(
            {
                "order_item_id": f"OI{3000 + i}",
                "order_id": order_id,
                "product_id": product["product_id"],
                "quantity": quantity,
                "unit_price": f"{unit_price:.2f}",
                "discount": f"{discount:.2f}",
                "line_total": f"{line_total:.2f}",
            }
        )

        payment_status = (
            "Refunded"
            if status in {"Cancelled", "Returned"}
            else random.choices(
                ["Completed", "Pending", "Failed"],
                weights=[80, 15, 5],
            )[0]
        )

        if payment_status == "Failed":
            amount = round(total * random.uniform(0.0, 0.5), 2)
        elif payment_status == "Refunded":
            amount = 0.00
        else:
            amount = total

        payments.append(
            {
                "payment_id": f"PAY{4000 + i}",
                "order_id": order_id,
                "payment_date": (
                    order_date + timedelta(days=random.randint(0, 5))
                ).strftime("%Y-%m-%d"),
                "payment_method": payment_method,
                "amount": f"{amount:.2f}",
                "status": payment_status,
                "transaction_id": f"TXN-{uuid.uuid4().hex[:10].upper()}",
            }
        )

    return orders, order_items, payments


def write_csv(file_name: str, headers, rows):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DATA_DIR / file_name
    with file_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def main():
    random.seed()
    customers = generate_customers(NUM_ROWS)
    products = generate_products(NUM_ROWS)
    orders, order_items, payments = generate_orders(customers, products, NUM_ROWS)

    write_csv(
        "customers.csv",
        [
            "customer_id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "city",
            "state",
            "zip_code",
            "signup_date",
            "loyalty_tier",
        ],
        customers,
    )

    write_csv(
        "products.csv",
        [
            "product_id",
            "name",
            "category",
            "price",
            "cost",
            "stock_qty",
            "is_active",
            "created_at",
        ],
        products,
    )

    write_csv(
        "orders.csv",
        [
            "order_id",
            "customer_id",
            "order_date",
            "status",
            "subtotal",
            "tax",
            "shipping_fee",
            "total",
            "payment_method",
            "shipping_address",
        ],
        orders,
    )

    write_csv(
        "order_items.csv",
        [
            "order_item_id",
            "order_id",
            "product_id",
            "quantity",
            "unit_price",
            "discount",
            "line_total",
        ],
        order_items,
    )

    write_csv(
        "payments.csv",
        [
            "payment_id",
            "order_id",
            "payment_date",
            "payment_method",
            "amount",
            "status",
            "transaction_id",
        ],
        payments,
    )

    print(f"Synthetic datasets created in {DATA_DIR}")


if __name__ == "__main__":
    main()

