from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.utils.translation import gettext_lazy as _

schema_view = get_schema_view(
   openapi.Info(
      title=_("task_collab_api API"),
      default_version='v1',
      description=_("API para gerenciamento de tarefas colaborativas"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/v1/tasks/', include('apps.tasks.urls')),
   path('api/v1/accounts/', include('apps.accounts.urls')),
   
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
