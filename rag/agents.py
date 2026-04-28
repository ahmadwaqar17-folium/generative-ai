import os
from dotenv import load_dotenv
import psycopg2
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from llm_config import llm

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@tool
def get_top_customers():
    """Returns the top 3 customers with the highest total purchasing amount."""
    query = """
    SELECT c.name, SUM(o.total) as total_spent
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    GROUP BY c.name
    ORDER BY total_spent DESC
    LIMIT 3;
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                results = cur.fetchall()
                return [f"Customer: {r[0]}, Total Spent: ${r[1]:.2f}" for r in results]
    except Exception as e:
        return f"Error fetching top customers: {e}"

@tool
def get_low_stock_products():
    """Returns products where the stock level is low (less than 100 units available)."""
    query = """
    SELECT name, stock, brand
    FROM products
    WHERE stock < 100
    ORDER BY stock ASC;
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                results = cur.fetchall()
                if not results:
                    return "No products are currently low on stock."
                return [f"Product: {r[0]}, Stock: {r[1]}, Brand: {r[2]}" for r in results]
    except Exception as e:
        return f"Error fetching low stock products: {e}"

@tool
def get_customers_with_bad_reviews():
    """Returns customers who have submitted bad reviews (rating 1 or 2)."""
    query = """
    SELECT DISTINCT c.name, c.email, r.rating, r.body
    FROM customers c
    JOIN reviews r ON c.id = r.customer_id
    WHERE r.rating <= 2;
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                results = cur.fetchall()
                if not results:
                    return "No bad reviews found."
                return [f"Customer: {r[0]}, Rating: {r[2]}, Review: {r[3]}" for r in results]
    except Exception as e:
        return f"Error fetching customers with bad reviews: {e}"

# List of tools available for the agent
tools = [get_top_customers, get_low_stock_products, get_customers_with_bad_reviews]

