from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget

from core.models import State, Action, Movement, Workflow


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass


class StateInline(admin.TabularInline):
    model = State
    extra = 0


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    pass


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    pass
