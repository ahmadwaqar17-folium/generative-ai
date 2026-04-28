from llm_config import llm

response = llm.invoke("Explain async/await in JavaScript within 2 lines")
print("Response content:")
print(response.content)
print("\nFull response object:")
print(response)
print("\nResponse type:")
print(type(response))
