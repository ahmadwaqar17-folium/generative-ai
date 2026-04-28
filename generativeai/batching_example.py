from llm_config import llm

# Batching: Runs multiple LLM calls in parallel. Control concurrency with config={"max_concurrency": 5}
print("Batch processing queries:")
responses = llm.batch([
    "what is 2+2",
    "what is 3+4",
    "what is 5*8"
])
for idx, response in enumerate(responses, 1):
    print(f"Query {idx} response: {response.content}")
