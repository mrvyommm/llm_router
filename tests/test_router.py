import unittest
from unittest.mock import patch

from router import route_request


class TestRouter(unittest.TestCase):

    @patch("router.ask_model")
    def test_passes_prompt_and_selected_model(self, mock_ask_model):
        expected = {
            "answer": "Test response",
            "model": "ollama/granite4:3b",
            "prompt_tokens": 10,
            "completion_tokens": 5,
            "total_tokens": 15,
        }
        mock_ask_model.return_value = expected

        result = route_request(
            prompt="Test prompt",
            model_id="ollama/granite4:3b",
        )

        mock_ask_model.assert_called_once_with(
            prompt="Test prompt",
            model_id="ollama/granite4:3b",
        )
        self.assertEqual(result, expected)

    @patch("router.ask_model")
    def test_propagates_execution_failure(self, mock_ask_model):
        mock_ask_model.side_effect = RuntimeError("Model unavailable")

        with self.assertRaisesRegex(
            RuntimeError,
            "Model unavailable",
        ):
            route_request(
                prompt="Test prompt",
                model_id="ollama/granite4:3b",
            )


if __name__ == "__main__":
    unittest.main()
