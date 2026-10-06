import os
import csv
import random
from datetime import date, timedelta

random.seed(42)

N_CUSTOMERS = 5000
N_ORDERS = 200000
OUT_DIR = "data"
os.makedirs(OUT_DIR, exist_ok=True)

SEGMENTS = ["Consumer", "Corporate", "Small Business"]
COUNTRIES = {
    "DE": ["Berlin", "Munich", "Hamburg", "Frankfurt"],
    "TR": ["Istanbul", "Ankara", "Izmir", "Adana"],
    "FR": ["Paris", "Lyon", "Marseille"],
    "NL": ["Amsterdam", "Rotterdam", "Utrecht"],
    "ES": ["Madrid", "Barcelona", "Valencia"],
    "IT": ["Rome", "Milan", "Turin"],
}
CATEGORIES = {
    "Electronics": (49.0, 1499.0),
    "Home & Kitchen": (9.0, 399.0),
    "Clothing": (7.0, 199.0),
    "Sports": (12.0, 549.0),
    "Books": (4.0, 59.0),
    "Toys": (5.0, 129.0),
}
STATUSES = ["completed"] * 70 + ["shipped"] * 15 + ["pending"] * 10 + ["cancelled"] * 5
PAYMENTS = ["credit_card", "debit_card", "paypal", "bank_transfer"]
CHANNELS = ["web", "mobile", "store"]
FIRST = ["Anna", "Mehmet", "Luca", "Sophie", "Ayse", "Pierre", "Julia", "Marco", "Elif", "Noah"]
LAST = ["Schmidt", "Yilmaz", "Rossi", "Martin", "Kaya", "Bernard", "Weber", "Conti", "Demir", "Jansen"]

START = date(2026, 1, 1)
END = date(2026, 9, 30)
DAYS = (END - START).days


def rand_date(start, span_days):
    return start + timedelta(days=random.randint(0, span_days))


# --- customers ---
customers = []
for i in range(1, N_CUSTOMERS + 1):
    country = random.choice(list(COUNTRIES))
    customers.append({
        "customer_id": f"C{i:05d}",
        "full_name": f"{random.choice(FIRST)} {random.choice(LAST)}",
        "email": f"user{i}@example.com",
        "segment": random.choice(SEGMENTS),
        "country": country,
        "city": random.choice(COUNTRIES[country]),
        "signup_date": rand_date(date(2023, 1, 1), 1095).isoformat(),
    })

with open(f"{OUT_DIR}/customers.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=customers[0].keys())
    w.writeheader()
    w.writerows(customers)

# --- orders ---
customer_ids = [c["customer_id"] for c in customers]
orders = []
for i in range(1, N_ORDERS + 1):
    category = random.choice(list(CATEGORIES))
    lo, hi = CATEGORIES[category]
    r = random.random()
    if r < 0.005:
        cid = ""                                   # empty customer_id
    elif r < 0.008:
        cid = f"C{random.randint(90000, 99999)}"   # orphan customer_id
    else:
        cid = random.choice(customer_ids)
    qty = random.randint(1, 5)
    if random.random() < 0.01:
        qty = -qty                                 # negative quantity
    orders.append({
        "order_id": f"O{i:07d}",
        "customer_id": cid,
        "order_date": rand_date(START, DAYS).isoformat(),
        "status": random.choice(STATUSES),
        "product_category": category,
        "quantity": qty,
        "unit_price": round(random.uniform(lo, hi), 2),
        "payment_method": random.choice(PAYMENTS),
        "channel": random.choice(CHANNELS),
    })

# duplicate order_id rows
duplicates = random.sample(orders, int(N_ORDERS * 0.005))
orders.extend(dict(d) for d in duplicates)
random.shuffle(orders)

with open(f"{OUT_DIR}/orders.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=orders[0].keys())
    w.writeheader()
    w.writerows(orders)

print(f"customers: {len(customers)} rows")
print(f"orders: {len(orders)} rows (including {len(duplicates)} duplicates)")