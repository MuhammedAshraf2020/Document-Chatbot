from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class EmbedderConfig:
    """Configuration for embedders."""

    embedding_model_id: str
    api_key: Optional[str] = None
    extra_params: Dict[str, Any] = None
