from rest_framework import serializers
from core.models import State, Action


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["id", "name"]


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
