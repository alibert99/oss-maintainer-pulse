import json

from maintainer_pulse.ai import _extract_output_text


def test_extract_output_text_prefers_response_shortcut():
    assert _extract_output_text({"output_text": "summary"}) == "summary"


def test_extract_output_text_reads_message_content():
    payload = {
        "output": [
            {
                "type": "message",
                "content": [
                    {"type": "output_text", "text": "first"},
                    {"type": "output_text", "text": "second"},
                ],
            }
        ]
    }

    assert _extract_output_text(payload) == "first\nsecond"


def test_extract_output_text_returns_empty_for_unexpected_payload():
    assert _extract_output_text(json.loads("{}")) == ""
