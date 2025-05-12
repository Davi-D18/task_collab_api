from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated, PermissionDenied


class IsOwner(BasePermission):
    """
    Classe de permissão que permite acesso apenas se o usuário autenticado for o mesmo do campo 'user' do objeto.
    Para ações de criação, verifica o payload antes de salvar.

    Atributos:
        Nenhum

    Herda de:
        BasePermission: Classe base para permissões customizadas no Django REST Framework
    """

    def has_permission(self, request, view):
        # Bypass para geração de esquema (Swagger/OpenAPI)
        if getattr(view, 'swagger_fake_view', False):
            return True

        # Requer autenticação
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated("Você precisa estar autenticado para usar esta API.")

        # Se for criação, valida payload
        if request.method == 'POST':
            user_id = request.data.get('usuario')
            if str(user_id) != str(request.user):
                raise PermissionDenied("Você não pode criar tarefa para outro usuário.")

        return True

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Verifica se o usuário tem permissão para acessar um objeto específico.
        Usado para operações de recuperação/atualização/exclusão em instâncias existentes.

        Args:
            request: A requisição sendo feita
            view: A view sendo acessada
            obj: O objeto sendo acessado

        Returns:
            bool: True se o usuário solicitante for dono do objeto, False caso contrário
        """
        return obj.usuario == request.user

    def has_check_permission(self) -> bool:
        """
        Chamado manualmente na view para operações de criação.
        Verifica se o ID do usuário nos dados da requisição corresponde ao usuário solicitante.

        Args:
            self: Instância da classe IsOwner

        Returns:
            bool: True se o ID do usuário corresponder ao usuário solicitante, False caso contrário
        """
        user_id = self.request.data.get('usuario')
        return str(user_id) == str(self.request.user)
