from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Manipulador de exceções personalizado que padroniza o formato das respostas de erro.
    """
    # Primeiro, obtém a resposta padrão
    response = exception_handler(exc, context)
    
    # Se não houver resposta, deixa o DRF lidar com isso
    if response is None:
        return response
    
    # Inicializa a estrutura de resposta padronizada
    error_response = {
        "title": "Erro",
        "errors": []
    }
    
    # Processa os erros com base no tipo de dados da resposta
    if isinstance(response.data, dict):
        # Se for um dicionário com campos específicos
        if "detail" in response.data:
            # Erro geral (não associado a um campo específico)
            error_response["errors"].append({
                "field": "general",
                "message": str(response.data["detail"])
            })
        else:
            # Para erros de validação com múltiplos campos
            for field, errors in response.data.items():
                if isinstance(errors, list):
                    for error in errors:
                        error_response["errors"].append({
                            "field": field,
                            "message": str(error)
                        })
                else:
                    error_response["errors"].append({
                        "field": field,
                        "message": str(errors)
                    })
    elif isinstance(response.data, list):
        # Se for uma lista de erros
        for item in response.data:
            error_response["errors"].append({
                "field": "general",
                "message": str(item)
            })
    else:
        # Caso seja uma string ou outro tipo
        error_response["errors"].append({
            "field": "general",
            "message": str(response.data)
        })
    
    # Substitui o conteúdo da resposta pelo formato padronizado
    response.data = error_response
    
    return response