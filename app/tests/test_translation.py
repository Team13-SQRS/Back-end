import pytest
from unittest.mock import patch
from app.services.translate import TranslationService

# Temporary tests for the TranslationService class
# Not comprehensive and should be expanded
@patch("app.services.translate.requests.post")
def test_translate_text_success(mock_post):
    mock_post.return_value.json.return_value = {
        "data": {
            "translations": {
                "translatedText": "Hello"
            }
        }
    }
    mock_post.return_value.status_code = 200
    result = TranslationService.translate_text("Привет")
    assert result == "Hello"


@patch("app.services.translate.requests.post")
def test_translate_text_failure(mock_post):
    mock_post.side_effect = Exception("API failure")
    result = TranslationService.translate_text("Привет")
    assert result is None
