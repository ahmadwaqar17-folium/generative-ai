from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from llm_config import llm

@tool
def get_weather(location: str) -> str:
    """Get the current weather at a location."""
    return f"It's currently cold in {location}."

llm_with_tools = llm.bind_tools([get_weather])

def run_conversation(user_input: str):
    messages = [HumanMessage(content=user_input)]
    
    ai_msg = llm_with_tools.invoke(messages)
    messages.append(ai_msg)
    
    while ai_msg.tool_calls:
        for tool_call in ai_msg.tool_calls:
            tool_result = get_weather.invoke(tool_call["args"])
            
            messages.append(ToolMessage(
                content=tool_result,
                tool_call_id=tool_call["id"]
            ))
        
        # Get next response from model
        ai_msg = llm_with_tools.invoke(messages)
        messages.append(ai_msg)
    
    return ai_msg.content


print(run_conversation("What's the weather in Lahore?"))