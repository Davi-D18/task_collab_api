def check_permission(self):
        """
        Verifica se o campo 'user' no payload corresponde ao usuário autenticado.
        """
        user_id = self.request.data.get('usuario')  # ou 'username' se usar SlugRelatedField
        return str(user_id) == str(self.request.user)