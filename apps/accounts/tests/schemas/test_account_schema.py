import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from apps.accounts.schemas.account_schema import UserSerializer, TokenObtainPairSerializer

User = get_user_model()


@pytest.fixture
def user_data():
    """Fixture para dados de usuário de teste."""
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword123'
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
    """Fixture para criar um usuário de teste para tokens."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpassword123'
    )


@pytest.fixture
def credentials_username():
    """Fixture para credenciais válidas usando nome de usuário."""
    return {
        'credential': 'testuser',
        'password': 'testpassword123'
    }


@pytest.fixture
def credentials_email():
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
def test_user_serialization_returns_correct_data(existing_user):
    """Testa se a serialização de um usuário retorna os dados corretos."""
    # Arrange
    serializer = UserSerializer(existing_user)
    
    # Act
    data = serializer.data
    
    # Assert
    assert data['username'] == 'existinguser'
    assert data['email'] == 'existing@example.com'
    assert 'password' not in data


@pytest.mark.django_db
def test_user_deserialization_valid_data_creates_user(user_data):
    """Testa se a deserialização de dados válidos cria um usuário corretamente."""
    # Arrange
    serializer = UserSerializer(data=user_data)
    
    # Act
    is_valid = serializer.is_valid()
    user = serializer.save()
    
    # Assert
    assert is_valid is True
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.check_password('testpassword123') is True


@pytest.mark.django_db
def test_user_deserialization_duplicate_username_fails_validation(existing_user):
    """Testa se a deserialização falha quando um nome de usuário duplicado é fornecido."""
    # Arrange
    duplicate_data = {
        'username': 'existinguser',  # Nome de usuário já existente
        'email': 'new@example.com',
        'password': 'newpassword123'
    }
    
    # Act
    serializer = UserSerializer(data=duplicate_data)
    is_valid = serializer.is_valid()
    
    # Assert
    assert is_valid is False
    assert 'username' in serializer.errors


@pytest.mark.django_db
def test_user_deserialization_duplicate_email_fails_validation(existing_user):
    """Testa se a deserialização falha quando um email duplicado é fornecido."""
    # Arrange
    duplicate_data = {
        'username': 'newuser',
        'email': 'existing@example.com',  # Email já existente
        'password': 'newpassword123'
    }
    
    # Act
    serializer = UserSerializer(data=duplicate_data)
    is_valid = serializer.is_valid()
    
    # Assert
    assert is_valid is False
    assert 'email' in serializer.errors


@pytest.mark.django_db
def test_token_obtain_with_username_returns_tokens(test_user, credentials_username):
    """Testa se o token é gerado corretamente usando o nome de usuário como credencial."""
    # Arrange
    serializer = TokenObtainPairSerializer(data=credentials_username)
    
    # Act
    is_valid = serializer.is_valid()
    
    # Assert
    assert is_valid is True
    assert 'access' in serializer.validated_data
    assert 'refresh' in serializer.validated_data


@pytest.mark.django_db
def test_token_obtain_with_email_returns_tokens(test_user, credentials_email):
    """Testa se o token é gerado corretamente usando o email como credencial."""
    # Arrange
    serializer = TokenObtainPairSerializer(data=credentials_email)
    
    # Act
    is_valid = serializer.is_valid()
    
    # Assert
    assert is_valid is True
    assert 'access' in serializer.validated_data
    assert 'refresh' in serializer.validated_data


@pytest.mark.django_db
def test_token_obtain_invalid_credentials_raises_exception(test_user, invalid_credentials):
    """Testa se a validação falha quando credenciais inválidas são fornecidas."""
    # Arrange
    serializer = TokenObtainPairSerializer(data=invalid_credentials)
    
    # Act & Assert
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


@pytest.mark.django_db
def test_token_contains_username(test_user):
    """Testa se o token gerado contém o nome de usuário no payload."""
    # Arrange & Act
    token = TokenObtainPairSerializer.get_token(test_user)
    
    # Assert
    assert token['username'] == 'testuser'