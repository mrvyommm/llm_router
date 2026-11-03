from pydantic import BaseModel
from router import route_request


class StructuredOutputError(Exception):
    """Raised when the model does not return usable structured output"""



def generate_structured(
        prompt: str,
        model_id: str,
        schema: type[BaseModel]
) -> BaseModel:
    """Generate a structured output and validate against a pydantic schema.
    """
    if not isinstance(schema, type) or not issubclass(schema, BaseModel):
        raise TypeError("schema must be a Pydantic BaseModel class ")
    
    response = route_request(
        prompt=prompt,
        model_id=model_id,
        request_options={
            "response_format":schema,
        },
    )

    raw_output = response.get("answer")

    if not isinstance(raw_output, str) or not raw_output.strip():
        raise StructuredOutputError(
            "Model returned empty or unusable structured output"
        )

    return schema.model_validate_json(raw_output)
    