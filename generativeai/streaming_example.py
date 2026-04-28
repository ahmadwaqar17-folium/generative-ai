from llm_config import llm

# Streaming: Returns partial responses as they are generated instead of waiting for the full response
print("Streaming response (NestJS dependency injection, 100 words):")
for chunk in llm.stream("explain dependency injection in nestjs in 100 words"):
    print(chunk.content, end="  ", flush=True)
print()
