from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.tasks.controllers.tasks_controller import TasksViewSet

router = DefaultRouter()
router.register('', TasksViewSet)

urlpatterns = [
    path('', include(router.urls))
]