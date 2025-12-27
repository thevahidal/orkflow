from core.views import WorkflowableStatesViewSet
from oms_demo.models import Order


class OrderStatesView(WorkflowableStatesViewSet):
    workflowable_model = Order
