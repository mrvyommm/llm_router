from llm_client import ask_model

def route_request(prompt: str,model_id: str) -> dict:
    """Execute request using an explicityly selected mmodel"""


    return ask_model(
        prompt=prompt,
        model_id=model_id,
    )



if __name__ == "__main__" :
    result =  route_request(
        prompt="Explain model context protocol (MCP) in three simple bullet points",
        model_id="ollama/granite4:3b",
        )

    print("Answer:", result["answer"])
    print("Model:", result["model"])
    print("Prompt tokens:", result["prompt_tokens"])
    print("Completion tokens:", result["completion_tokens"])
    print("Total tokens:", result["total_tokens"])