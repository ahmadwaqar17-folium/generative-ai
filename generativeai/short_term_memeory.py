from llm_config import llm

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

config = {
    "configurable": {"thread_id": "1"}
}

# memory
checkpointer = MemorySaver()

# IMPORTANT: tools must be provided (even empty list if supported)
agent = create_react_agent(
    model=llm,
    tools=[],
    checkpointer=checkpointer,
)

# first message
response = agent.invoke(
    {
        "messages": [
            HumanMessage(content="Hi, I am Ahmad"),
        ]
    },
    config=config
)

print(response["messages"][-1].content)

# second message (memory test)
response = agent.invoke(
    {
        "messages": [
            HumanMessage(content="What is my name?"),
        ]
    },
    config=config
)

print(response["messages"][-1].content)