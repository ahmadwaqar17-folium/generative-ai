# 🗄️ RAG — Ecommerce Database Agent

An AI-powered conversational agent that answers questions about an **ecommerce database** (customers, products, orders, reviews) hosted on **PostgreSQL / Supabase**, using **LangGraph** and **Groq**.

---

## 📁 Files

| File | Purpose |
|---|---|
| `rag.py` | Main chat loop — run this to start the agent |
| `agents.py` | LangGraph tool definitions (DB query tools) |
| `llm_config.py` | LLM initialisation using Groq |
| `seed.py` | Seeds the Postgres database with sample ecommerce data |

---

## 🛠️ Tools Available to the Agent

| Tool | Description |
|---|---|
| `get_top_customers` | Top 3 customers by total spend |
| `get_low_stock_products` | Products with stock < 100 units |
| `get_customers_with_bad_reviews` | Customers who left 1★ or 2★ reviews |

---

## ▶️ How to Run

> Make sure you are in the root `genai/` directory with the shared venv activated first.

```bash
# From the repo root
source venv/bin/activate

# Seed the database (first time only)
cd rag
python seed.py

# Start the chat agent
python rag.py
```

**Example conversation:**
```
--- Ecommerce RAG Agent ---
You: Who are the top customers?
Agent: The top 3 customers by spending are ...

You: Which products are low on stock?
Agent: The following products have less than 100 units ...

You: exit
Goodbye!
```

---

## 🔑 Environment Variables

These live in the root `.env` file (see [../.env.example](../.env.example)):

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ | Groq inference API key |
| `DATABASE_URL` | ✅ | PostgreSQL connection string (e.g., from Supabase) |

---

## 🧠 Architecture

```
User Input
    │
    ▼
 LangGraph ReAct Agent (Groq LLM)
    │
    ├─ get_top_customers()          ──► PostgreSQL
    ├─ get_low_stock_products()     ──► PostgreSQL
    └─ get_customers_with_bad_reviews() ──► PostgreSQL
    │
    ▼
 Final Response
```
