from django.db import models
from django.core.exceptions import ValidationError

from core.strategies import StrategyRegistry


class State(models.Model):
    name = models.CharField(max_length=100)
    actions = models.ManyToManyField("Action", blank=True)
    # on_enter
    # on_exit

    def __str__(self):
        return self.name


class Action(models.Model):
    name = models.CharField(max_length=100)
    strategy = models.CharField(max_length=100)
    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    def clean(self):
        strategy = StrategyRegistry().get_strategy(self.strategy)
        if not strategy:
            raise ValidationError(
                {"strategy": f"Strategy '{self.strategy}' is not registered."}
            )

        try:
            strategy.validate_metadata(self.metadata)
        except Exception as error:
            raise ValidationError(error)

    def execute(self, *args, **kwargs):
        strategy = StrategyRegistry().get_strategy(self.strategy)
        strategy.execute(self, *args, **kwargs)


class Movement(models.Model):
    slug = models.SlugField(unique=True)
    from_states = models.ManyToManyField(State, related_name="movements_from")
    to_state = models.ForeignKey(
        State, related_name="movements_to", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.slug} -> {self.to_state.name}"


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
