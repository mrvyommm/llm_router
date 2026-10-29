import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

DEFAULT_MODEL=os.getenv("LLM_MODEL", "ollama/granite4:3b")
OLLAMA_API_BASE=os.getenv("OLLAMA_API_BASE", "http://localhost:11434")


def ask_model(prompt: str, model_id: str | None=None) -> dict:
    selected_model= model_id or DEFAULT_MODEL

    request_args = {
        "model": selected_model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }
    

    if selected_model.startswith("ollama/"):
        request_args["api_base"] = OLLAMA_API_BASE                  


    response = completion(**request_args)

    

    usage=response.usage

    return {
           "answer":response.choices[0].message.content,
           "model":response.model,
           "prompt_tokens":usage.prompt_tokens if usage else None,
           "completion_tokens":usage.completion_tokens if usage else None,
           "total_tokens":usage.total_tokens if usage else None,
    }



if __name__ == "__main__":
    result = ask_model("Explain MCP(model context protocol) in three simple sentences.")

    print("Answer:", result["answer"])
    print("Model:", result["model"])
    print("Prompt tokens:", result["prompt_tokens"])
    print("Completion tokens:", result["completion_tokens"])
    print("Total tokens:", result["total_tokens"])
