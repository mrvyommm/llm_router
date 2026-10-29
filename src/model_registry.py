MODEL_REGISTRY = {
    "ollama/granite4:3b": {
        "provider": "ollama",
        "cost_type": "local",
        "supports_tool_calling": True,
        "status": "configured",

    },
}


def get_model(model_id: str) ->dict | None:

    return MODEL_REGISTRY.get(model_id)

if __name__ == "__main__":
    for model_id, details in MODEL_REGISTRY.items():
        print(model_id, details)

    print("\nlookup test:")
    print(get_model("ollama/granite4:3b"))
    print(get_model("unknown/model"))