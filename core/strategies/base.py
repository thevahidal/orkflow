from abc import ABC, abstractmethod
from typing import Dict, List

from pydantic import BaseModel, Field


class ContextValue(BaseModel):
    value: str


class BaseMetadataSchmea(BaseModel):
    _context: Dict[str, ContextValue]


class BaseStrategy(ABC):
    class MetadataSchema(BaseMetadataSchmea):
        pass

    def validate_metadata(self, metadata):
        self.MetadataSchema.model_validate(metadata)

    def make_contextful_obj(self, metadata: dict):
        _context = metadata.pop("_context", {})
        for key, value in metadata:
            pass

    @abstractmethod
    def execute(self, data):
        """Execute the strategy with the provided data."""
        pass
