from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class TextGeneratorBase(ABC):
    """Base abstract class for text generators."""

    @abstractmethod
    def __init__(
        self,
        api_key: str,
        api_url: Optional[str] = None,
        default_input_max_characters: int = 1000,
        default_generation_max_output_tokens: int = 1000,
        default_generation_temperature: float = 0.1,
    ):
        pass

    @abstractmethod
    def process_text(self, text: str) -> str:
        """Process input text before generation."""
        pass

    @abstractmethod
    def generate_text(
        self,
        prompt: str,
        chat_history: List[Dict[str, str]] = [],
        max_output_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> Optional[str]:
        """Generate text based on prompt and parameters."""
        pass

    def construct_prompt(self, prompt: str, role: str = "user") -> Dict[str, str]:
        """Construct a message dictionary for chat models."""
        return {"role": role, "content": prompt}
