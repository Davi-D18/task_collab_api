from rest_framework.exceptions import PermissionDenied


def verificar_acesso_anonimo(user, request=None):
    # Verifica se é uma view fake do Swagger
    if getattr(request, 'swagger_fake_view', False):
        # Retorna silenciosamente para permitir a geração do esquema Swagger
        return

    # Verifica se o usuário é anônimo
    if not user or user.is_anonymous:
        raise PermissionDenied("Acesso não autorizado. É necessário estar autenticado para acessar esta API.")