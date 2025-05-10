from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Permite ação apenas se o usuário autenticado for o mesmo que o campo `user` do objeto.
    Para ações de criação, verifica o payload antes de salvar.
    """

    def has_permission(self, request, view):
        # Permite acesso ao endpoint; checagem mais fina em `has_object_permission`
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Para retrieve/update/delete de instâncias existentes
        return obj.user == request.user

    def has_create_permission(self, request, view):
        # Chamado manualmente na view para criação
        user_id = request.data.get('user')
        return str(user_id) == str(request.user.id)
