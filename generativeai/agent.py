from langchain.agents import create_agent
from llm_config import llm 
from langchain.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get the current weather at a location."""
    return f"It's currently cold in {location}."

agent=create_agent(
    model = llm ,
    tools=[get_weather],
    system_prompt="you are helpul assistant"


)
response=agent.invoke({"messages":[{"role":"user","content":"what is the weather in lahore?"}]})
print(response)
print("###########################################",response["messages"][-1].content)