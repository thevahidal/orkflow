from typing import Dict, Any
from django.db import models
from django.core.exceptions import ValidationError

from core.guards.registry import GuardRegistry
from core.strategies import StrategyRegistry


class State(models.Model):
    name = models.CharField(max_length=100)
    actions = models.ManyToManyField("Action", blank=True)
    metadata = models.JSONField(blank=True, null=True)

    enter_guard = models.CharField(max_length=100, blank=True)
    exit_guard = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    # def clean(self) -> None:
    #     enter_guard = GuardRegistry.get(self.enter_guard)
    #     exit_guard = GuardRegistry.get(self.exit_guard)
    #
    #     for guard in (enter_guard, exit_guard):
    #         if not guard:
    #             raise ValidationError({"guard": f"Guard '{guard}' is not registered."})


class Action(models.Model):
    name = models.CharField(max_length=100)
    strategy = models.CharField(max_length=100)
    metadata = models.JSONField(blank=True, null=True)
    on_finish_transition = models.ForeignKey(
        "Transition", on_delete=models.SET_NULL, null=True
    )

    def __str__(self) -> str:
        return self.name

    def _get_strategy(self):
        strategy = StrategyRegistry.get(self.strategy)
        if not strategy:
            raise ValidationError(
                {"strategy": f"Strategy '{self.strategy}' is not registered."}
            )
        return strategy

    def clean(self) -> None:
        strategy = self._get_strategy()

        try:
            self.metadata = strategy.validate_metadata(self).model_dump()
        except ValidationError:
            raise
        except Exception as exc:
            raise ValidationError({"metadata": str(exc)})

    def execute(self, instance, inputs: Dict[str, Any], *args, **kwargs):
        strategy = self._get_strategy()
        strategy.execute(
            instance=instance,
            action=self,
            inputs=inputs,
            *args,
            **kwargs,
        )
        if (
            self.on_finish_transition
            and self.on_finish_transition.from_state_id == instance._current_state_id
        ):
            instance._current_state_id = self.on_finish_transition.to_state_id
            instance.save()


class Transition(models.Model):
    from_state = models.ForeignKey(
        State, related_name="transition_from", on_delete=models.CASCADE, null=True
    )
    to_state = models.ForeignKey(
        State, related_name="transition_to", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.from_state.name} ->‌ {self.to_state.name}"

    class Meta:
        unique_together = (("from_state", "to_state"),)


# class LogEntry(models.Model):
#     def __str__(self):
#         return str(self.id)


class Workflow(models.Model):
    states = models.ManyToManyField(State, related_name="workflows", blank=True)


class Workflowable(models.Model):
    _workflow = models.ForeignKey(
        Workflow, related_name="workflowables", on_delete=models.CASCADE
    )
    _current_state = models.ForeignKey(
        State, related_name="workflowables", on_delete=models.CASCADE
    )

    class Meta:
        abstract = True

    def clean(self):
        if (
            self._workflow_id
            and self._current_state_id
            and not self._workflow.states.filter(id=self._current_state_id).exists()
        ):
            raise ValidationError(
                {"_current_state": "Current state must belong to workflow states"}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    #
    # def _run_exit_guard(self):
    #     state: State = self._current_state
    #     if state.exit_guard:
    #         guard = GuardRegistry.get(state.exit_guard)
    #         if not guard:
    #             raise ValidationError("Exit guard not found")
    #         guard.can_exit(self)
    #
    # def _run_enter_guard(self, next_state: State):
    #     if next_state.enter_guard:
    #         guard = GuardRegistry.get(next_state.enter_guard)
    #         if not guard:
    #             raise ValidationError("Enter guard not found")
    #         guard.can_enter(self)
