from django.urls import path, include
from rest_framework.routers import DefaultRouter

from oms_demo.views import OrderStatesView


router = DefaultRouter()


router.register(
    r"orders/(?P<workflowable_id>\d+)/states",
    OrderStatesView,
    basename="order-states",
)


urlpatterns = [
    path("api/v1/", include(router.urls)),
]
