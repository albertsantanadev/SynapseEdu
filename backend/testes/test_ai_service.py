import json
from unittest.mock import MagicMock, patch

import pytest

from app.services.ai_service import generate_description, AIServiceError


def _mock_groq_response(content: str):
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=content))]
    return mock_response


@patch("app.services.ai_service.Groq")
def test_generate_description_success(mock_groq_class):
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _mock_groq_response(
        json.dumps({"description": "Uma ótima aula.", "tags": ["a", "b", "c"]})
    )
    mock_groq_class.return_value = mock_client

    result = generate_description("Álgebra Linear", "PDF")

    assert result["description"] == "Uma ótima aula."
    assert result["tags"] == ["a", "b", "c"]


@patch("app.services.ai_service.Groq")
def test_generate_description_truncates_tags_to_three(mock_groq_class):
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _mock_groq_response(
        json.dumps({"description": "desc", "tags": ["a", "b", "c", "d", "e"]})
    )
    mock_groq_class.return_value = mock_client

    result = generate_description("Título qualquer", "Vídeo")

    assert len(result["tags"]) == 3


@patch("app.services.ai_service.Groq")
def test_generate_description_invalid_json_raises_ai_service_error(mock_groq_class):
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = _mock_groq_response("isso não é JSON")
    mock_groq_class.return_value = mock_client

    with pytest.raises(AIServiceError):
        generate_description("Título", "Link")


@patch("app.services.ai_service.Groq")
def test_generate_description_api_failure_raises_ai_service_error(mock_groq_class):
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("timeout")
    mock_groq_class.return_value = mock_client

    with pytest.raises(AIServiceError):
        generate_description("Título", "PDF")