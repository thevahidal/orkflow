from django.core.exceptions import ValidationError
from django.http import Http404
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from core.serializers import StateSerializer, ActionSerializer
from django.shortcuts import get_object_or_404


class WorkflowableMixin:
    workflowable_model = None

    def get_workflowable(self):
        return get_object_or_404(
            self.workflowable_model,
            id=self.kwargs["workflowable_id"],
        )


class WorkflowableStatesViewSet(WorkflowableMixin, viewsets.ViewSet):
    """
    GET  /workflowables/{workflowable_id}/states
    GET  /workflowables/{workflowable_id}/states/{state_id}/actions
    POST /workflowables/{workflowable_id}/states/{state_id}/actions/{action_id}/execute
    """

    def get_serializer_context(self):
        context = {}
        context["workflowable_instance"] = self.get_workflowable()
        return context

    def list(self, request, workflowable_id=None):
        workflowable = self.get_workflowable()
        states = workflowable._workflow.states.all()
        return Response(
            StateSerializer(
                states, many=True, context=self.get_serializer_context()
            ).data
        )

    @action(detail=False, methods=["get"], url_path=r"(?P<state_id>\d+)/actions")
    def state_actions(self, request, workflowable_id=None, state_id=None):
        workflowable = self.get_workflowable()

        state = workflowable._workflow.states.filter(id=state_id).first()
        if not state:
            raise Http404("State not part of workflow")

        actions = state.actions.all()
        return Response(
            ActionSerializer(
                actions, many=True, context=self.get_serializer_context()
            ).data
        )

    @action(
        detail=False,
        methods=["post"],
        url_path=r"(?P<state_id>\d+)/actions/(?P<action_id>\d+)/execute",
    )
    def execute_action(
        self, request, workflowable_id=None, state_id=None, action_id=None
    ):
        workflowable = self.get_workflowable()

        state = workflowable._workflow.states.filter(id=state_id).first()
        if not state:
            raise Http404("State not part of workflow")

        action = state.actions.filter(id=action_id).first()
        if not action:
            raise Http404("Action not allowed in this state")

        if workflowable._current_state_id != state.id:
            return Response(
                {"detail": "Action not allowed in current state"},
                status=status.HTTP_409_CONFLICT,
            )

        try:
            inputs = request.data.get("inputs", {})

            action.execute(instance=workflowable, inputs=inputs)

            return Response({"status": "executed"}, status=status.HTTP_200_OK)
        except ValidationError as e:
            raise serializers.ValidationError(e)
