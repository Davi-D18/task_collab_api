from django.urls import path, include


urlpatterns = [
    path('', include('apps.accounts.routes.accounts_routes')),
]
