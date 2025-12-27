from core.models import Action
from .base import BaseStrategy
from pydantic import BaseModel, Field


class PythonFunctionStrategy(BaseStrategy):
    """
    Strategy for executing Python functions.
    """

    class MetadataSchema(BaseModel):
        function_path: str

    def execute(self, action: Action, *args, **kwargs):
        """
        Execute the given Python function with provided arguments.
        Args:
            func (callable): The Python function to execute.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.
        Returns:
            The result of the function execution.
        """
        return
