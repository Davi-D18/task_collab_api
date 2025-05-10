from django.contrib import admin
from apps.tasks.models.tasks import Tasks


@admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'titulo', 'descricao', 'prioridade', 'prazo', 'status', 'criado_em')
    list_filter = ('status', 'prioridade', 'usuario',)
    search_fields = ('titulo', 'descricao')
    ordering = ('-criado_em',)
    list_per_page = 20
    list_editable = ('status',)