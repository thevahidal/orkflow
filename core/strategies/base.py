from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, Any, List, Literal
import string

from django.core.exceptions import ValidationError
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from core.models import Action


class MetadataInput(BaseModel):
    name: str
    type: Literal["int", "str", "datetime", "date", "time", "bool", "float"] = Field(
        default="str"
    )
    required: bool = Field(default=False)


class BaseMetadataSchema(BaseModel):
    context: Dict[str, str] = Field(default_factory=dict)
    inputs: List[MetadataInput] = Field(default_factory=list)
    is_disabled: bool = Field(default=False)
    is_automatic: bool = Field(default=False)


class BaseStrategy(ABC):
    class MetadataSchema(BaseMetadataSchema):
        pass

    @classmethod
    def validate_metadata(cls, action: "Action"):
        return cls.MetadataSchema.model_validate(action.metadata)

    def validate_inputs(self, instance, action: "Action", inputs: Dict[str, Any]):
        for input in self.get_metadata(instance, action, inputs).inputs:
            if input.required and (
                input.name not in inputs.keys() or not inputs[input.name]
            ):
                raise ValidationError({"inputs": f"Key {input.name} is missing"})

            if inputs[input.name]:
                try:
                    from datetime import date, time, datetime  # noqa

                    eval(f"{input.type}('{inputs[input.name]}')")
                except TypeError:
                    raise ValidationError(
                        {"inputs": f"Key {input.name} should be of type {input.type}"}
                    )

    @classmethod
    def make_contextful_metadata(
        cls, instance: Any, action: "Action", inputs: Dict[str, Any]
    ):
        raw_metadata = action.metadata.copy()
        context = raw_metadata.get("context", {})

        resolved = {
            key: cls._resolve_value(value, instance, context, inputs)
            for key, value in raw_metadata.items()
        }
        return cls.MetadataSchema(**resolved)

    @classmethod
    def get_metadata(cls, instance, action: "Action", inputs: Dict[str, Any]):
        """
        Returns validated + context-resolved metadata
        """
        return cls.make_contextful_metadata(
            instance=instance, action=action, inputs=inputs
        )

    @abstractmethod
    def execute(
        self, instance, action: "Action", inputs: Dict[str, Any], *args, **kwargs
    ):
        self.validate_inputs(instance, action, inputs)
        return self.get_metadata(instance, action, inputs)

    @classmethod
    def _resolve_value(
        cls, value: Any, instance: Any, context: Dict[str, str], inputs: Dict[str, Any]
    ) -> Any:
        if isinstance(value, str):
            return cls._render_template(value, instance, context, inputs)

        if isinstance(value, list):
            return [
                cls._resolve_value(item, instance, context, inputs) for item in value
            ]

        if isinstance(value, dict):
            return {
                k: cls._resolve_value(v, instance, context, inputs)
                for k, v in value.items()
            }

        return value

    @staticmethod
    def _render_template(
        template: str, instance: Any, context: Dict[str, str], inputs: Dict[str, Any]
    ) -> str:
        formatter = string.Formatter()

        result = template
        for _, field_name, _, _ in formatter.parse(template):
            if not field_name:
                continue

            ctx = context.get(field_name)
            if not ctx:
                continue

            resolved = BaseStrategy._resolve_context_value(ctx, instance, inputs)
            if resolved is not None:
                result = result.replace(f"{{{field_name}}}", str(resolved))

        return result

    @staticmethod
    def _resolve_context_value(expr: str, instance: Any, inputs: Dict[str, Any]) -> Any:
        """
        Supports expressions like:
        $this.foo.bar
        """
        if not expr.startswith("$this.") and not expr.startswith("$inputs."):
            return None

        if expr.startswith("$this."):
            attr_path = expr.removeprefix("$this.").split(".")
            value = instance

            for attr in attr_path:
                value = getattr(value, attr, None)
                if value is None:
                    break

        if expr.startswith("$inputs."):
            expr_value = expr.replace("$inputs.", "")
            value = inputs.get(expr_value)

        return value
