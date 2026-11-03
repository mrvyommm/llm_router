import unittest
from unittest.mock import patch

from pydantic import BaseModel, Field, ValidationError

from structured_output import (
    generate_structured,
    StructuredOutputError,
)


class TestAssessment(BaseModel):
    risk_level: str
    confidence: float = Field(ge=0, le=1)
    indicators: list[str]


class TestStructuredOutput(unittest.TestCase):

    @patch("structured_output.route_request")
    def test_returns_validated_pydantic_object(self, mock_route):
        mock_route.return_value = {
            "answer": """
            {
                "risk_level": "high",
                "confidence": 0.95,
                "indicators": ["unusual amount", "new beneficiary"]
            }
            """
        }

        result = generate_structured(
            prompt="Assess transaction",
            model_id="gemini/gemini-2.5-flash",
            schema=TestAssessment,
        )

        self.assertIsInstance(result, TestAssessment)
        self.assertEqual(result.risk_level, "high")
        self.assertEqual(result.confidence, 0.95)

        mock_route.assert_called_once_with(
            prompt="Assess transaction",
            model_id="gemini/gemini-2.5-flash",
            request_options={
                "response_format": TestAssessment,
            },
        )

    @patch("structured_output.route_request")
    def test_rejects_invalid_json(self, mock_route):
        mock_route.return_value = {
            "answer": "This is not valid JSON"
        }

        with self.assertRaises(ValidationError):
            generate_structured(
                prompt="Assess transaction",
                model_id="gemini/gemini-2.5-flash",
                schema=TestAssessment,
            )

    @patch("structured_output.route_request")
    def test_rejects_schema_validation_failure(self, mock_route):
        mock_route.return_value = {
            "answer": """
            {
                "risk_level": "high",
                "confidence": 1.5,
                "indicators": []
            }
            """
        }

        with self.assertRaises(ValidationError):
            generate_structured(
                prompt="Assess transaction",
                model_id="gemini/gemini-2.5-flash",
                schema=TestAssessment,
            )

    @patch("structured_output.route_request")
    def test_rejects_empty_output(self, mock_route):
        mock_route.return_value = {"answer": None}

        with self.assertRaises(StructuredOutputError):
            generate_structured(
                prompt="Assess transaction",
                model_id="gemini/gemini-2.5-flash",
                schema=TestAssessment,
            )

    def test_rejects_non_pydantic_schema(self):
        with self.assertRaises(TypeError):
            generate_structured(
                prompt="Assess transaction",
                model_id="gemini/gemini-2.5-flash",
                schema=dict,
            )

    @patch("structured_output.route_request")
    def test_propagates_execution_failure(self, mock_route):
        mock_route.side_effect = RuntimeError("Provider unavailable")

        with self.assertRaisesRegex(
            RuntimeError,
            "Provider unavailable",
        ):
            generate_structured(
                prompt="Assess transaction",
                model_id="gemini/gemini-2.5-flash",
                schema=TestAssessment,
            )


if __name__ == "__main__":
    unittest.main()