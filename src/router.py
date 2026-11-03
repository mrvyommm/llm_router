from llm_client import ask_model

def route_request(
        prompt: str,
        model_id: str,
        request_options: dict | None =  None,
        ) -> dict:
    """
    Execute a request using an explicitly selected model.

    request_options allows callers to pass additional supported
    LiteLLM request parameters without changing the router.
    """


    return ask_model(
        prompt=prompt,
        model_id=model_id,
        request_options=request_options,
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