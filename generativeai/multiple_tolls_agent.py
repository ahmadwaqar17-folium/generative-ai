import getpass
import os

tavily_api_key = os.getenv("TAVILY_API_KEY")


from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from llm_config import llm 

tavily_tool = TavilySearch(
    max_results=5,
    topic="general",
    # include_answer=False,
    # include_raw_content=False,
    # include_images=False,
    # include_image_descriptions=False,
    # search_depth="basic",
    # time_range="day",
    # include_domains=None,
    # exclude_domains=None
)
from langchain.tools import tool
import operator
import ast

@tool("calculator", description="Performs arithmetic calculations. Use this for any math problems.")
def calculator(expression: str) -> str:
    """Safely evaluate simple mathematical expressions."""
    try:
        # Parse and evaluate safely (limited to basic math)
        tree = ast.parse(expression, mode='eval')
        result = eval(compile(tree, '<string>', 'eval'), {"__builtins__": {}}, {
            "abs": abs, "round": round,
            "min": min, "max": max,
            **{op.__name__: op for op in [operator.add, operator.sub, operator.mul, 
                                         operator.truediv, operator.pow, operator.mod]}
        })
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

agent=create_agent(model=llm,tools=[tavily_tool,calculator])
input="What is the current population of Pakistan and what is the 2+2?"
result = agent.invoke({
    "messages": [
        {"role": "user", "content": input}
    ]
})

print(result["messages"][-1].content)