from enum import Enum
from typing import Any, Dict, Optional

from .base import TextGeneratorBase
from .groq_generator import GroqTextGenerator
from .openai_generator import OpenAITextGenerator


class GeneratorType(Enum):
    OPENAI = "OPENAI"
    GROQ = "GROQ"


class TextGeneratorFactory:
    """Factory class for creating text generators."""

    DEFAULT_MODELS = {
        GeneratorType.OPENAI.value: "gpt-4o-mini",
        GeneratorType.GROQ.value: "mixtral-8x7b-32768",
    }

    @staticmethod
    def create_generator(
        generator_type: GeneratorType,
        api_key: str,
        model_id: Optional[str] = None,
        api_url: Optional[str] = None,
        default_input_max_characters: int = 1000,
        default_generation_max_output_tokens: int = 1000,
        default_generation_temperature: float = 0.1,
    ) -> TextGeneratorBase:
        """Create a text generator instance based on the specified type."""

        generators = {
            GeneratorType.OPENAI.value: OpenAITextGenerator,
            GeneratorType.GROQ.value: GroqTextGenerator,
        }
        generator_class = generators.get(generator_type)
        if not generator_class:
            raise ValueError(f"Unsupported generator type: {generator_type}")

        # Use default model if none provided
        if not model_id:
            model_id = TextGeneratorFactory.DEFAULT_MODELS[generator_type]

        return generator_class(
            api_key=api_key,
            generation_model_id=model_id,  # Pass model ID to generator
            api_url=api_url,
            default_input_max_characters=default_input_max_characters,
            default_generation_max_output_tokens=default_generation_max_output_tokens,
            default_generation_temperature=default_generation_temperature,
        )
