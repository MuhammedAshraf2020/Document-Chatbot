from dataclasses import dataclass
from typing import Optional


@dataclass
class GeneratorConfig:
    """Configuration for text generators."""

    api_key: str
    generation_model_id: str  # Made this required instead of optional
    api_url: Optional[str] = None
    default_input_max_characters: int = 1000
    default_generation_max_output_tokens: int = 1000
    default_generation_temperature: float = 0.1
