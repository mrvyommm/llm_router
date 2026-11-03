
from typing import Literal

from pydantic import BaseModel, Field

from structured_output import generate_structured


class InvestigationSummary(BaseModel):
    case_summary: str = Field(
        description="A concise summary of the supplied transaction case."
    )

    observations: list[str] = Field(
        description="Observations directly supported by the supplied information."
    )

    information_gaps: list[str] = Field(
        description="Important information that is missing or unavailable."
    )

    recommended_next_steps: list[str] = Field(
        description="Suggested investigation steps, not automatic account actions."
    )

    assessment_status: Literal[
        "insufficient_information",
        "requires_human_review",
    ]


if __name__ == "__main__":

    transaction_prompt = """
    Review the following transaction information and prepare an
    investigation summary.

    Customer: C123
    Transaction amount: INR 250000
    Average historical transaction amount: INR 15000
    Beneficiary: First-time beneficiary
    Transaction location: Different from the customer's usual location
    Customer authentication: Successful

    Identify observations, information gaps and recommended
    investigation steps.

    Do not claim that fraud has occurred.
    Do not invent missing facts.
    Do not recommend automatically approving or blocking the transaction.
    """

    result = generate_structured(
        prompt=transaction_prompt,
        model_id="gemini/gemini-2.5-flash",
        schema=InvestigationSummary,
    )

    print("\nStructured investigation result:\n")
    print(result.model_dump_json(indent=2))

    print("\nIndividual fields:\n")
    print("Status:", result.assessment_status)
    print("Observations:", result.observations)
