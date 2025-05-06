import requests
from typing import Optional
import os
from tenacity import retry, stop_after_attempt, wait_fixed

TRANSLATE_URL = "https://deep-translate1.p.rapidapi.com/language/translate/v2"
HEADERS = {
    "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
    "x-rapidapi-host": "deep-translate1.p.rapidapi.com",
    "Content-Type": "application/json",
}


def return_none(retry_state):
    return None


class TranslationService:
    @staticmethod
    @retry(stop=stop_after_attempt(3),
           wait=wait_fixed(2),
           retry_error_callback=return_none
           )
    def translate_text(
        text: str, source_lang: str = "ru", target_lang: str = "en"
    ) -> Optional[str]:
        payload = {"q": text, "source": source_lang, "target": target_lang}
        response = requests.post(
            TRANSLATE_URL, json=payload, headers=HEADERS, timeout=5
        )
        response.raise_for_status()
        return response.json()["data"]["translations"]["translatedText"]
