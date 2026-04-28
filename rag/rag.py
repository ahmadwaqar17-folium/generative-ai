from llm_config import llm
from agents import tools
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

# System message to guide the agent
system_message = (
    "You are a helpful ecommerce database assistant. "
    "Use the provided tools to answer questions about customers, products, and reviews. "
    "If a question cannot be answered using the available tools, politely inform the user "
    "that you don't have access to that specific information or provide a generic helpful response."
)

# Create the agent
agent = create_agent(llm, tools, system_prompt=system_message)

def run_chat():
    print("--- Ecommerce RAG Agent ---")
    print("Type 'exit' or 'quit' to stop.\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
            
        if not user_input.strip():
            continue
            
        try:
            # Invoke the agent
            response = agent.invoke({
                "messages": [HumanMessage(content=user_input)]
            })
            
            # The last message in the sequence is the agent's final response
            final_response = response["messages"][-1].content
            print(f"\nAgent: {final_response}\n")
            
        except Exception as e:
            print(f"\nError: {e}\n")

if __name__ == "__main__":
    run_chat()
