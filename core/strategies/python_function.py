from core.models import Action
from .base import BaseMetadataSchema, BaseStrategy
from pydantic import BaseModel, Field


class PythonFunctionStrategy(BaseStrategy):
    """
    Strategy for executing Python functions.
    """

    class MetadataSchema(BaseMetadataSchema):
        function_path: str

    def execute(self, instance, action: Action, *args, **kwargs):
        return
