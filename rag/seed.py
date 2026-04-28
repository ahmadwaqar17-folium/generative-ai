"""
Ecommerce Database Seed Script
--------------------------------
Creates and populates tables for a realistic ecommerce dataset
to be used with LangChain RAG implementation.

Tables:
    - categories
    - products
    - customers
    - orders
    - order_items
    - reviews
"""

import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


# ─── Schema ────────────────────────────────────────────────────────────────────

CREATE_TABLES_SQL = """
-- Categories
CREATE TABLE IF NOT EXISTS categories (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

-- Products
CREATE TABLE IF NOT EXISTS products (
    id            SERIAL PRIMARY KEY,
    category_id   INTEGER REFERENCES categories(id),
    name          VARCHAR(200) NOT NULL,
    description   TEXT,
    price         NUMERIC(10, 2) NOT NULL,
    stock         INTEGER DEFAULT 0,
    brand         VARCHAR(100),
    sku           VARCHAR(50) UNIQUE,
    created_at    TIMESTAMP DEFAULT NOW()
);

-- Customers
CREATE TABLE IF NOT EXISTS customers (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(150) NOT NULL,
    email      VARCHAR(150) UNIQUE NOT NULL,
    city       VARCHAR(100),
    country    VARCHAR(100),
    joined_at  TIMESTAMP DEFAULT NOW()
);

-- Orders
CREATE TABLE IF NOT EXISTS orders (
    id           SERIAL PRIMARY KEY,
    customer_id  INTEGER REFERENCES customers(id),
    status       VARCHAR(50) DEFAULT 'pending',
    total        NUMERIC(10, 2),
    ordered_at   TIMESTAMP DEFAULT NOW()
);

-- Order Items
CREATE TABLE IF NOT EXISTS order_items (
    id          SERIAL PRIMARY KEY,
    order_id    INTEGER REFERENCES orders(id),
    product_id  INTEGER REFERENCES products(id),
    quantity    INTEGER NOT NULL,
    unit_price  NUMERIC(10, 2) NOT NULL
);

-- Reviews
CREATE TABLE IF NOT EXISTS reviews (
    id          SERIAL PRIMARY KEY,
    product_id  INTEGER REFERENCES products(id),
    customer_id INTEGER REFERENCES customers(id),
    rating      SMALLINT CHECK (rating BETWEEN 1 AND 5),
    title       VARCHAR(200),
    body        TEXT,
    reviewed_at TIMESTAMP DEFAULT NOW()
);
"""

# ─── Seed Data ─────────────────────────────────────────────────────────────────

CATEGORIES = [
    ("Electronics",     "Gadgets, devices, and accessories for everyday tech needs."),
    ("Clothing",        "Casual, formal, and sportswear for men and women."),
    ("Home & Kitchen",  "Appliances, cookware, and home decor essentials."),
    ("Books",           "Fiction, non-fiction, textbooks, and more."),
    ("Sports",          "Equipment and gear for outdoor and indoor sports."),
    ("Beauty",          "Skincare, haircare, and personal grooming products."),
    ("Toys",            "Educational and fun toys for children of all ages."),
    ("Automotive",      "Car accessories, tools, and maintenance products."),
]

PRODUCTS = [
    # Electronics
    (1, "Wireless Noise-Cancelling Headphones", "Premium over-ear headphones with active noise cancellation, 30-hour battery, and foldable design.", 149.99, 85, "SoundMax", "ELEC-001"),
    (1, "4K Smart TV 55 inch",                  "Ultra HD Smart TV with HDR, built-in streaming apps, and voice control.", 699.99, 30, "VisionPro", "ELEC-002"),
    (1, "Mechanical Gaming Keyboard",            "RGB backlit mechanical keyboard with tactile switches and anti-ghosting.", 89.99, 120, "KeyMaster", "ELEC-003"),
    (1, "USB-C Fast Charger 65W",               "GaN technology charger compatible with laptops, phones, and tablets.", 39.99, 200, "ChargePlus", "ELEC-004"),
    (1, "Portable Bluetooth Speaker",            "Waterproof speaker with 360° sound, 20-hour battery, and built-in microphone.", 59.99, 150, "SoundMax", "ELEC-005"),
    (1, "Smartwatch Pro Series 5",               "Fitness tracker with heart rate monitor, GPS, sleep tracking, and 7-day battery.", 249.99, 60, "FitTech", "ELEC-006"),
    # Clothing
    (2, "Men's Slim Fit Chinos",                "Stretch cotton chinos available in multiple colors — perfect for casual and semi-formal wear.", 49.99, 300, "UrbanWear", "CLOT-001"),
    (2, "Women's Running Tights",               "High-waist compression leggings with moisture-wicking fabric and side pockets.", 34.99, 250, "ActiveFit", "CLOT-002"),
    (2, "Unisex Graphic Hoodie",                "100% cotton fleece hoodie with a bold front print — cozy and stylish.", 44.99, 180, "StreetStyle", "CLOT-003"),
    (2, "Formal Oxford Shirt",                  "Classic slim-fit shirt in premium wrinkle-resistant fabric, ideal for office wear.", 39.99, 220, "UrbanWear", "CLOT-004"),
    # Home & Kitchen
    (3, "Air Fryer 5.5L",                       "Digital air fryer with 8 pre-set cooking modes, rapid hot air for crispy results.", 99.99, 75, "KitchenPro", "HOME-001"),
    (3, "Stainless Steel Cookware Set 10-Piece", "Dishwasher-safe non-stick pots and pans with tempered glass lids.", 129.99, 50, "ChefElite", "HOME-002"),
    (3, "Robot Vacuum Cleaner",                  "Smart mapping, auto-charging, and app control for effortless floor cleaning.", 279.99, 40, "CleanBot", "HOME-003"),
    (3, "Memory Foam Pillow",                    "Contour memory foam pillow with cooling gel layer for better sleep quality.", 45.99, 160, "SleepWell", "HOME-004"),
    # Books
    (4, "Atomic Habits",                         "A proven framework for improving every day by James Clear.", 16.99, 500, "Avery", "BOOK-001"),
    (4, "The Pragmatic Programmer",              "A classic guide to software craftsmanship and developer best practices.", 49.99, 200, "Addison-Wesley", "BOOK-002"),
    (4, "Deep Work",                             "Rules for focused success in a distracted world by Cal Newport.", 14.99, 350, "Grand Central", "BOOK-003"),
    (4, "Python Crash Course",                   "Hands-on, project-based introduction to programming with Python.", 39.99, 280, "No Starch Press", "BOOK-004"),
    # Sports
    (5, "Adjustable Dumbbell Set 5-52.5 lbs",   "Space-saving dumbbells that replace 15 sets — quick-adjust mechanism.", 349.99, 35, "IronFlex", "SPRT-001"),
    (5, "Yoga Mat Non-Slip 6mm",                 "Extra thick eco-friendly TPE yoga mat with alignment lines and carry strap.", 29.99, 400, "ZenFit", "SPRT-002"),
    (5, "Mountain Bike Helmet",                  "Lightweight MIPS-certified helmet with 21 vents and adjustable fit system.", 79.99, 90, "TrailGuard", "SPRT-003"),
    # Beauty
    (6, "Vitamin C Serum 30ml",                  "Brightening serum with 20% Vitamin C, hyaluronic acid, and Vitamin E.", 24.99, 300, "GlowLab", "BEAU-001"),
    (6, "Electric Face Cleanser Brush",          "Silicone sonic brush with 3 speed settings for deep pore cleansing.", 39.99, 120, "SkinTech", "BEAU-002"),
    # Toys
    (7, "LEGO Architecture Set",                 "Build iconic world landmarks — 694 pieces for ages 12+.", 59.99, 100, "LEGO", "TOYS-001"),
    (7, "Remote Control Monster Truck",          "1:10 scale RC truck with rechargeable battery and 30+ mph speed.", 69.99, 80, "TurboRace", "TOYS-002"),
    # Automotive
    (8, "Car Dash Cam 4K",                       "Wide-angle night-vision dash camera with loop recording and parking mode.", 89.99, 110, "DriveSafe", "AUTO-001"),
    (8, "Tire Inflator Portable",                "Cordless electric pump with digital display — works for cars, bikes, and balls.", 49.99, 130, "AirBoost", "AUTO-002"),
]

CUSTOMERS = [
    ("Alice Johnson",   "alice@example.com",   "New York",   "USA"),
    ("Bob Smith",       "bob@example.com",     "London",     "UK"),
    ("Carol White",     "carol@example.com",   "Toronto",    "Canada"),
    ("David Brown",     "david@example.com",   "Sydney",     "Australia"),
    ("Emma Wilson",     "emma@example.com",    "Berlin",     "Germany"),
    ("Frank Garcia",    "frank@example.com",   "Madrid",     "Spain"),
    ("Grace Lee",       "grace@example.com",   "Seoul",      "South Korea"),
    ("Henry Martinez",  "henry@example.com",   "Karachi",    "Pakistan"),
    ("Irene Taylor",    "irene@example.com",   "Dubai",      "UAE"),
    ("James Anderson",  "james@example.com",   "Chicago",    "USA"),
    ("Karen Thomas",    "karen@example.com",   "Paris",      "France"),
    ("Liam Jackson",    "liam@example.com",    "Cape Town",  "South Africa"),
]

ORDER_STATUSES = ["pending", "processing", "shipped", "delivered", "cancelled"]

REVIEW_TITLES = [
    "Absolutely love it!",
    "Great value for money",
    "Does exactly what it says",
    "Exceeded my expectations",
    "Solid product, would buy again",
    "Decent but has some quirks",
    "Not bad, not great",
    "Very disappointed",
    "Terrible quality",
    "Five stars, highly recommend",
]

REVIEW_BODIES = [
    "This product completely transformed my daily routine. The quality is exceptional and it arrived well-packaged.",
    "I was hesitant at first given the price, but it's totally worth every penny. Very happy with this purchase.",
    "Works exactly as described. Setup was straightforward and the performance has been consistent.",
    "I've been using this for 3 months now and it still works like day one. Impressive build quality.",
    "Good product overall. Shipping was fast and the item matched the description perfectly.",
    "It's fine for the price. A few minor issues but nothing that affects day-to-day use significantly.",
    "Average experience. I expected more based on the reviews, but it gets the job done.",
    "Stopped working after 2 weeks. Customer support was slow to respond. Would not recommend.",
    "The quality doesn't match the price. Felt cheap and flimsy out of the box.",
    "One of the best purchases I've made this year. My whole family loves it!",
]


def seed(conn):
    cur = conn.cursor()

    print("📦 Creating tables...")
    cur.execute(CREATE_TABLES_SQL)
    conn.commit()
    print("   ✅ Tables created.")

    # ── Categories ──────────────────────────────────────────────────────────
    print("📂 Seeding categories...")
    execute_values(
        cur,
        "INSERT INTO categories (name, description) VALUES %s ON CONFLICT (name) DO NOTHING",
        CATEGORIES,
    )
    conn.commit()

    # ── Products ─────────────────────────────────────────────────────────────
    print("🛒 Seeding products...")
    execute_values(
        cur,
        """INSERT INTO products (category_id, name, description, price, stock, brand, sku)
           VALUES %s ON CONFLICT (sku) DO NOTHING""",
        PRODUCTS,
    )
    conn.commit()

    # ── Customers ─────────────────────────────────────────────────────────────
    print("👤 Seeding customers...")
    execute_values(
        cur,
        "INSERT INTO customers (name, email, city, country) VALUES %s ON CONFLICT (email) DO NOTHING",
        CUSTOMERS,
    )
    conn.commit()

    # Fetch IDs
    cur.execute("SELECT id FROM products ORDER BY id")
    product_ids = [r[0] for r in cur.fetchall()]

    cur.execute("SELECT id FROM customers ORDER BY id")
    customer_ids = [r[0] for r in cur.fetchall()]

    # ── Orders + Order Items ──────────────────────────────────────────────────
    print("📋 Seeding orders and order items...")
    for customer_id in customer_ids:
        num_orders = random.randint(1, 4)
        for _ in range(num_orders):
            days_ago = random.randint(0, 365)
            ordered_at = datetime.now() - timedelta(days=days_ago)
            status = random.choice(ORDER_STATUSES)

            cur.execute(
                "INSERT INTO orders (customer_id, status, total, ordered_at) VALUES (%s, %s, %s, %s) RETURNING id",
                (customer_id, status, 0, ordered_at),
            )
            order_id = cur.fetchone()[0]

            # 1-5 items per order
            items = random.sample(product_ids, k=random.randint(1, 5))
            order_total = 0
            for product_id in items:
                cur.execute("SELECT price FROM products WHERE id = %s", (product_id,))
                unit_price = float(cur.fetchone()[0])
                qty = random.randint(1, 3)
                order_total += unit_price * qty
                cur.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, %s, %s, %s)",
                    (order_id, product_id, qty, unit_price),
                )

            cur.execute("UPDATE orders SET total = %s WHERE id = %s", (round(order_total, 2), order_id))
    conn.commit()

    # ── Reviews ──────────────────────────────────────────────────────────────
    print("⭐ Seeding reviews...")
    for product_id in product_ids:
        num_reviews = random.randint(2, 6)
        reviewers = random.sample(customer_ids, k=min(num_reviews, len(customer_ids)))
        for customer_id in reviewers:
            rating = random.randint(1, 5)
            title = random.choice(REVIEW_TITLES)
            body = random.choice(REVIEW_BODIES)
            days_ago = random.randint(0, 300)
            reviewed_at = datetime.now() - timedelta(days=days_ago)
            cur.execute(
                """INSERT INTO reviews (product_id, customer_id, rating, title, body, reviewed_at)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (product_id, customer_id, rating, title, body, reviewed_at),
            )
    conn.commit()

    # ── Summary ──────────────────────────────────────────────────────────────
    cur.execute("SELECT COUNT(*) FROM categories"); print(f"\n   📂 Categories : {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM products");   print(f"   🛒 Products   : {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM customers");  print(f"   👤 Customers  : {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM orders");     print(f"   📋 Orders     : {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM order_items");print(f"   📦 Order items: {cur.fetchone()[0]}")
    cur.execute("SELECT COUNT(*) FROM reviews");    print(f"   ⭐ Reviews    : {cur.fetchone()[0]}")

    cur.close()


if __name__ == "__main__":
    print(f"🔌 Connecting to database...")
    conn = psycopg2.connect(DATABASE_URL)
    print("   ✅ Connected!\n")
    try:
        seed(conn)
        print("\n✅ Database seeded successfully!")
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {e}")
        raise
    finally:
        conn.close()
