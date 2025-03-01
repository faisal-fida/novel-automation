import google.generativeai as genai
import json
from typing import Dict


class Translator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._configure_genai()

    def _configure_genai(self):
        """Configure the Gemini API with safety settings."""
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(
            "gemini-1.5-flash",
            generation_config={"response_mime_type": "application/json"},
            safety_settings=[
                {"category": cat, "threshold": "BLOCK_NONE"}
                for cat in [
                    "HARM_CATEGORY_DANGEROUS",
                    "HARM_CATEGORY_HARASSMENT",
                    "HARM_CATEGORY_HATE_SPEECH",
                    "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "HARM_CATEGORY_DANGEROUS_CONTENT",
                ]
            ],
        )

    def translate_to_french(self, text: str) -> Dict[str, str]:
        """Translate given text to French using Gemini API."""
        prompt = f"""{text}
        
        Your task is to translate the following text into French:
        
        Ensure that the translation is grammatically accurate, fluent, and faithful to the original text.
        Return the translation using the following JSON schema:
        
        data = {{
            "translated_text": "str"
        }}
        
        Return a valid JSON object.
        """

        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except json.JSONDecodeError:
            print(f"Error decoding JSON response: {response.text}")
            try:
                return eval(response.text)
            except Exception as e:
                return {"translated_text": f"Translation failed: {e}"}
