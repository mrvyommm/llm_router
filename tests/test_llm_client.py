import unittest
from unittest.mock import patch

from llm_client import ask_model


class TestLLMClient(unittest.TestCase):

    @patch("llm_client.completion")
    def test_forwards_request_options(self, mock_completion):
        mock_completion.return_value = type(
            "MockResponse",
            (),
            {
                "choices": [
                    type(
                        "MockChoice",
                        (),
                        {
                            "message": type(
                                "MockMessage",
                                (),
                                {"content": "Test answer"},
                            )()
                        },
                    )()
                ],
                "model": "gemini/gemini-2.5-flash",
                "usage": None,
            },
        )()

        ask_model(
            prompt="Test prompt",
            model_id="gemini/gemini-2.5-flash",
            request_options={"temperature": 0.2},
        )

        call_args = mock_completion.call_args.kwargs

        self.assertEqual(call_args["temperature"], 0.2)
        self.assertEqual(
            call_args["model"],
            "gemini/gemini-2.5-flash",
        )

    def test_rejects_reserved_options(self):
        with self.assertRaisesRegex(ValueError, "reserved"):
            ask_model(
                prompt="Test prompt",
                model_id="gemini/gemini-2.5-flash",
                request_options={"model": "ollama/granite4:3b"},
            )


if __name__ == "__main__":
    unittest.main()