from typing import Any
from rest_framework import serializers
from core.models import State, Action, Transition, Workflow


class TransitionSerializer(serializers.ModelSerializer):
    from_state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())
    to_state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())

    class Meta:
        model = Transition
        fields = [
            "id",
            "from_state",
            "to_state",
        ]


class ActionSerializer(serializers.ModelSerializer):
    metadata = serializers.SerializerMethodField()

    def get_metadata(self, obj: Action):
        strategy = obj._get_strategy()
        instance = self.context.get("workflowable_instance")
        return strategy.get_metadata(
            instance=instance, action=obj, inputs={}
        ).model_dump()

    class Meta:
        model = Action
        fields = ["id", "name", "strategy", "metadata"]

    def to_representation(self, instance: Action) -> dict[str, Any]:
        representation = super().to_representation(instance)
        if "metadata" in representation and "context" in representation["metadata"]:
            del representation["metadata"]["context"]

        return representation


class StateSerializer(serializers.ModelSerializer):
    # transition_from = TransitionSerializer(many=True)
    transition_to = TransitionSerializer(many=True)
    actions = ActionSerializer(many=True)

    class Meta:
        model = State
        fields = ["id", "name", "transition_to", "actions"]


class WorkflowSerializer(serializers.ModelSerializer):
    states = serializers.PrimaryKeyRelatedField(many=True, queryset=State.objects.all())

    class Meta:
        model = Workflow
        fields = ["id", "states"]
