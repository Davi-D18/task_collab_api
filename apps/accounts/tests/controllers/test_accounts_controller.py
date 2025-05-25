import pytest
import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


@pytest.fixture
def api_client():
    """Fixture para criar um cliente API."""
    return APIClient()


@pytest.fixture
def register_url():
    """Fixture para a URL de registro."""
    return reverse('register')


@pytest.fixture
def login_url():
    """Fixture para a URL de login."""
    return reverse('login')


@pytest.fixture
def refresh_url():
    """Fixture para a URL de atualização de token."""
    return reverse('token_refresh')


@pytest.fixture
def valid_user_data():
    """Fixture para dados válidos de registro de usuário."""
    return {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'newpassword123'
    }


@pytest.fixture
def existing_user():
    """Fixture para criar um usuário existente."""
    return User.objects.create_user(
        username='existinguser',
        email='existing@example.com',
        password='existingpassword123'
    )


@pytest.fixture
def test_user():
    """Fixture para criar um usuário de teste para login."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpassword123'
    )


@pytest.fixture
def valid_credentials_username():
    """Fixture para credenciais válidas usando nome de usuário."""
    return {
        'credential': 'testuser',
        'password': 'testpassword123'
    }


@pytest.fixture
def valid_credentials_email():
    """Fixture para credenciais válidas usando email."""
    return {
        'credential': 'test@example.com',
        'password': 'testpassword123'
    }


@pytest.fixture
def invalid_credentials():
    """Fixture para credenciais inválidas."""
    return {
        'credential': 'testuser',
        'password': 'wrongpassword'
    }


@pytest.mark.django_db
def test_register_valid_user_creates_user(api_client, register_url, valid_user_data):
    """Testa se um usuário válido pode ser registrado."""
    # Arrange - já feito pelas fixtures
    
    # Act
    response = api_client.post(
        register_url,
        data=json.dumps(valid_user_data),
        content_type='application/json'
    )
    
    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username='newuser').exists()
    assert response.data['username'] == 'newuser'
    assert response.data['email'] == 'newuser@example.com'
    assert 'password' not in response.data


@pytest.mark.django_db
def test_register_duplicate_username_returns_400(api_client, register_url, existing_user):
    """Testa se o registro falha quando um nome de usuário duplicado é fornecido."""
    # Arrange
    duplicate_data = {
        'username': 'existinguser',  # Nome de usuário já existente
        'email': 'new@example.com',
        'password': 'newpassword123'
    }
    
    # Act
    response = api_client.post(
        register_url,
        data=json.dumps(duplicate_data),
        content_type='application/json'
    )
    
    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    # Verifica se a mensagem de erro contém informações sobre o nome de usuário duplicado
    error_found = False
    for error in response.data['errors']:
        if error['field'] == 'username':
            error_found = True
            break
    assert error_found, "Erro de username não encontrado na resposta"


@pytest.mark.django_db
def test_register_duplicate_email_returns_400(api_client, register_url, existing_user):
    """Testa se o registro falha quando um email duplicado é fornecido."""
    # Arrange
    duplicate_data = {
        'username': 'newuser2',
        'email': 'existing@example.com',  # Email já existente
        'password': 'newpassword123'
    }
    
    # Act
    response = api_client.post(
        register_url,
        data=json.dumps(duplicate_data),
        content_type='application/json'
    )
    
    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    # Verifica se a mensagem de erro contém informações sobre o email duplicado
    error_found = False
    for error in response.data['errors']:
        if error['field'] == 'email':
            error_found = True
            break
    assert error_found, "Erro de email não encontrado na resposta"


@pytest.mark.django_db
def test_register_missing_fields_returns_400(api_client, register_url):
    """Testa se o registro falha quando campos obrigatórios estão ausentes."""
    # Arrange
    incomplete_data = {
        'username': 'incompleteuser',
        # Email ausente
        'password': 'incompletepassword123'
    }
    
    # Act
    response = api_client.post(
        register_url,
        data=json.dumps(incomplete_data),
        content_type='application/json'
    )
    
    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    # Verifica se a mensagem de erro contém informações sobre o campo ausente
    error_found = False
    for error in response.data['errors']:
        if error['field'] == 'email':
            error_found = True
            break
    assert error_found, "Erro de email ausente não encontrado na resposta"


@pytest.mark.django_db
def test_login_with_username_returns_tokens(api_client, login_url, test_user, valid_credentials_username):
    """Testa se o login funciona corretamente usando o nome de usuário."""
    # Arrange - já feito pelas fixtures
    
    # Act
    response = api_client.post(
        login_url,
        data=json.dumps(valid_credentials_username),
        content_type='application/json'
    )
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_login_with_email_returns_tokens(api_client, login_url, test_user, valid_credentials_email):
    """Testa se o login funciona corretamente usando o email."""
    # Arrange - já feito pelas fixtures
    
    # Act
    response = api_client.post(
        login_url,
        data=json.dumps(valid_credentials_email),
        content_type='application/json'
    )
    
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_login_invalid_credentials_returns_400(api_client, login_url, test_user, invalid_credentials):
    """Testa se o login falha quando credenciais inválidas são fornecidas."""
    # Arrange - já feito pelas fixtures
    
    # Act
    response = api_client.post(
        login_url,
        data=json.dumps(invalid_credentials),
        content_type='application/json'
    )
    
    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_token_refresh_returns_new_access_token(api_client, login_url, refresh_url, test_user, valid_credentials_username):
    """Testa se a atualização de token funciona corretamente."""
    # Arrange
    login_response = api_client.post(
        login_url,
        data=json.dumps(valid_credentials_username),
        content_type='application/json'
    )
    refresh_token = login_response.data['refresh']
    
    # Act
    refresh_response = api_client.post(
        refresh_url,
        data=json.dumps({'refresh': refresh_token}),
        content_type='application/json'
    )
    
    # Assert
    assert refresh_response.status_code == status.HTTP_200_OK
    assert 'access' in refresh_response.data


@pytest.mark.django_db
def test_token_refresh_invalid_token_returns_401(api_client, refresh_url):
    """Testa se a atualização de token falha quando um token inválido é fornecido."""
    # Arrange
    invalid_token = {'refresh': 'invalid-token'}
    
    # Act
    response = api_client.post(
        refresh_url,
        data=json.dumps(invalid_token),
        content_type='application/json'
    )
    
    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED