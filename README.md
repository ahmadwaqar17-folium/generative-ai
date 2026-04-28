# 🤖 GenAI — LangChain & LangGraph Learning Repo

A single monorepo for experimenting with **LangChain**, **LangGraph**, and **Groq LLMs**.
Contains two sub-projects that share one virtual environment and one requirements file.

```
genai/
├── venv/                  ← single shared virtual environment
├── requirements.txt       ← all dependencies (shared)
├── .env                   ← your secrets (git-ignored)
├── .env.example           ← template — copy to .env and fill in
├── .gitignore
│
├── rag/                   ← 🗄️  Ecommerce RAG Agent (Postgres + LangGraph)
│   ├── rag.py             ← main chat loop
│   ├── agents.py          ← LangGraph tools (DB queries)
│   ├── llm_config.py      ← shared LLM initialisation
│   ├── seed.py            ← seed the Postgres database
│   └── README.md
│
└── generativeai/          ← 📚 LangChain Concept Examples
    ├── llm_config.py      ← shared LLM initialisation
    ├── basic_invoke.py
    ├── batching_example.py
    ├── streaming_example.py
    ├── strucured_output.py
    ├── short_term_memeory.py
    ├── tools_concept.py
    ├── agent.py
    ├── multiple_tolls_agent.py
    └── README.md
```

---

## ⚡ Quick Start

### 1. Clone the repo
```bash
git clone <your-repo-url>
cd genai
```

### 2. Create the shared virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
```

### 3. Install all dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env and fill in your API keys
```

| Variable | Where to get it | Used by |
|---|---|---|
| `GROQ_API_KEY` | https://console.groq.com | Both |
| `TAVILY_API_KEY` | https://app.tavily.com | `generativeai/` |
| `DATABASE_URL` | Supabase → Project Settings → Database | `rag/` |

---

## 🗄️ rag/ — Ecommerce RAG Agent

An AI agent that queries a **PostgreSQL (Supabase)** ecommerce database using natural language.

```bash
cd rag
python rag.py
```

→ See [rag/README.md](./rag/README.md) for full details.

---

## 📚 generativeai/ — LangChain Concept Examples

A collection of standalone scripts demonstrating core LangChain & LangGraph patterns.

```bash
cd generativeai
python basic_invoke.py
python streaming_example.py
# ... run any script individually
```

→ See [generativeai/README.md](./generativeai/README.md) for full details.

---

## 🛠️ Tech Stack

| Library | Purpose |
|---|---|
| [LangChain](https://python.langchain.com) | LLM abstraction & chains |
| [LangGraph](https://langchain-ai.github.io/langgraph/) | Stateful agent graphs |
| [Groq](https://groq.com) | Ultra-fast LLM inference |
| [Tavily](https://tavily.com) | Real-time web search |
| [psycopg2](https://www.psycopg.org/) | PostgreSQL adapter |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Env variable loading |

---

## 📝 Notes

- The `venv/` folder is **git-ignored** — each collaborator runs `pip install -r requirements.txt` after cloning.
- The `.env` file is **git-ignored** — never commit real API keys.
- Both sub-projects load `.env` via `python-dotenv`; since the venv is at root, make sure you run scripts from the `rag/` or `generativeai/` directories respectively so dotenv finds the root `.env`.
