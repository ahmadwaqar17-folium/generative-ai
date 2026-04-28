# 📚 GenerativeAI — LangChain Concept Examples

A collection of standalone Python scripts that demonstrate **core LangChain and LangGraph patterns** using the **Groq** LLM.

Each script is self-contained and focuses on one concept — great for learning or referencing patterns quickly.

---

## 📁 Scripts

| File | Concept | Description |
|---|---|---|
| `basic_invoke.py` | Basic Invocation | Simple one-shot LLM call using `.invoke()` |
| `batching_example.py` | Batching | Send multiple prompts at once with `.batch()` |
| `streaming_example.py` | Streaming | Stream tokens in real-time with `.stream()` |
| `strucured_output.py` | Structured Output | Get typed JSON output using `with_structured_output()` |
| `short_term_memeory.py` | Memory | Maintain conversation history (short-term memory) |
| `tools_concept.py` | Tools | Define and bind custom tools to an LLM |
| `agent.py` | Basic Agent | Single-tool LangGraph agent with `create_agent` |
| `multiple_tolls_agent.py` | Multi-Tool Agent | Agent with Tavily search + calculator tools |
| `llm_config.py` | Shared Config | LLM initialisation (imported by other scripts) |

---

## ▶️ How to Run

> Make sure you are in the root `genai/` directory with the shared venv activated first.

```bash
# From the repo root
source venv/bin/activate

# Run any script individually
cd generativeai
python basic_invoke.py
python streaming_example.py
python agent.py
# etc.
```

---

## 🔑 Environment Variables

These live in the root `.env` file (see [../.env.example](../.env.example)):

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ | Used by ALL scripts for LLM inference |
| `TAVILY_API_KEY` | ✅ (for `multiple_tolls_agent.py`) | Real-time web search |

---

## 🧠 Concept Map

```
LangChain Basics
├── basic_invoke.py        → llm.invoke("...")
├── batching_example.py    → llm.batch([...])
└── streaming_example.py   → llm.stream("...")

Structured Output
└── strucured_output.py    → llm.with_structured_output(Schema)

Memory
└── short_term_memeory.py  → ChatMessageHistory / RunnableWithHistory

Tools & Agents
├── tools_concept.py       → @tool decorator + bind_tools
├── agent.py               → create_agent() single tool
└── multiple_tolls_agent.py → multi-tool agent (Tavily + calculator)
```

---

## 💡 LLM Used

All scripts use **Groq's `qwen/qwen3-32b`** model via the `llm_config.py` shared config:

```python
from langchain.chat_models import init_chat_model
llm = init_chat_model("groq:qwen/qwen3-32b")
```

To switch models, edit `llm_config.py` — the change applies to all scripts automatically.
