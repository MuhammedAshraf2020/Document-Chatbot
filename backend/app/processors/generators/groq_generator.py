import logging
from typing import Dict, List, Optional

from groq import Groq

from .base import TextGeneratorBase
from .config import GeneratorConfig
from .exceptions import (
    ClientNotInitializedException,
    GenerationException,
    ModelNotSetException,
)


class GroqTextGenerator(TextGeneratorBase):
    """Groq implementation of text generator."""

    def __init__(
        self,
        api_key: str,
        generation_model_id: str,
        api_url: Optional[str] = None,
        default_input_max_characters: int = 2000,
        default_generation_max_output_tokens: int = 2000,
        default_generation_temperature: float = 0.1,
    ):
        self.config = GeneratorConfig(
            api_key=api_key,
            generation_model_id=generation_model_id,
            api_url=api_url,
            default_input_max_characters=default_input_max_characters,
            default_generation_max_output_tokens=default_generation_max_output_tokens,
            default_generation_temperature=default_generation_temperature,
        )

        self.client = Groq(
            api_key=self.config.api_key,
        )

        self.logger = logging.getLogger(__name__)

    def process_text(self, text: str) -> str:
        """Process input text by truncating to maximum length."""
        return text[: self.config.default_input_max_characters].strip()

    def generate_text(
        self,
        prompt: str,
        chat_history: List[Dict[str, str]] = [],
        max_output_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> Optional[str]:
        """Generate text using Groq's API."""
        if not self.client:
            raise ClientNotInitializedException("Groq client was not initialized")

        if not self.config.generation_model_id:
            raise ModelNotSetException("Generation model for Groq was not set")

        max_tokens = (
            max_output_tokens or self.config.default_generation_max_output_tokens
        )
        temp = temperature or self.config.default_generation_temperature

        messages = list(chat_history)
        messages.append(self.construct_prompt(prompt=prompt))

        try:
            response = self.client.chat.completions.create(
                model=self.config.generation_model_id,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temp,
            )

            if not response or not response.choices or not response.choices[0].message:
                raise GenerationException("Invalid response from Groq")

            return response.choices[0].message.content

        except Exception as e:
            self.logger.error(f"Error generating text with Groq: {str(e)}")
            raise GenerationException(f"Failed to generate text: {str(e)}")
