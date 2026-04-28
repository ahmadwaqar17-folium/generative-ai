import os
from dotenv import load_dotenv
import psycopg2
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from llm_config import llm

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# 1. Top Customers Chain
top_customers_prompt = ChatPromptTemplate.from_template(
    """
You are a data formatter.

Convert this raw database output into a clean, structured report:

{data}

Format:
- Rank customers
- Show total spent
- Make it readable and concise
"""
)
top_customers_chain = top_customers_prompt | llm | StrOutputParser()

# 2. Low Stock Products Chain
low_stock_prompt = ChatPromptTemplate.from_template(
    """
You are an inventory analyst.

Given product stock data:
{data}

Return:
- Critical stock items
- Sorted by urgency
- Highlight risks
"""
)
low_stock_chain = low_stock_prompt | llm | StrOutputParser()

# 3. Bad Reviews Chain
reviews_prompt = ChatPromptTemplate.from_template(
    """
You are a customer experience analyst.

Analyze this review dataset:
{data}

Provide:
- Summary of issues
- Repeat customers with complaints
- Business insight
"""
)
reviews_chain = reviews_prompt | llm | StrOutputParser()



@tool
def get_top_customers():
    """Returns the top 3 customers with the highest total purchasing amount in a structured report."""
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
                
                # Convert raw data to structured JSON-like list
                raw_data = [
                    {"name": r[0], "total_spent": float(r[1])}
                    for r in results
                ]
                
                # Use the chain for data intelligence layer
                return top_customers_chain.invoke({"data": raw_data})
                
    except Exception as e:
        return f"Error fetching top customers: {e}"

@tool
def get_low_stock_products():
    """Returns an analysis of products where the stock level is low (less than 100 units)."""
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
                
                # Convert raw data
                raw_data = [
                    {"name": r[0], "stock": r[1], "brand": r[2]}
                    for r in results
                ]
                
                # Use the chain for inventory analysis
                return low_stock_chain.invoke({"data": raw_data})
                
    except Exception as e:
        return f"Error fetching low stock products: {e}"

@tool
def get_customers_with_bad_reviews():
    """Returns an analysis of customers who have submitted bad reviews (rating 1 or 2)."""
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
                
                # Convert raw data
                raw_data = [
                    {"name": r[0], "email": r[1], "rating": r[2], "review": r[3]}
                    for r in results
                ]
                
                # Use the chain for customer experience analysis
                return reviews_chain.invoke({"data": raw_data})
                
    except Exception as e:
        return f"Error fetching customers with bad reviews: {e}"

# List of tools available for the agent
tools = [get_top_customers, get_low_stock_products, get_customers_with_bad_reviews]
