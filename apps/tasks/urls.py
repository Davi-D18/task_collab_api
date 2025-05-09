from django.urls import path, include


urlpatterns = [
    path('', include('apps.tasks.routes.tasks_routes')),
]
