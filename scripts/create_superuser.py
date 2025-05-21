#!/usr/bin/env python
import os
import django
import sys

from django.contrib.auth import get_user_model
from django.db import IntegrityError

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE', 'core.settings.production'))
django.setup()

User = get_user_model()

def create_superuser():
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    
    if not (username and email and password):
        print("⚠️ Variáveis de ambiente para superusuário não definidas. Pulando criação.")
        return
    
    try:
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            print(f"✅ Superusuário '{username}' criado com sucesso!")
        else:
            print(f"ℹ️ Superusuário '{username}' já existe.")
    except IntegrityError:
        print("⚠️ Erro ao criar superusuário: nome de usuário ou email já existe.")
    except Exception as e:
        print(f"❌ Erro ao criar superusuário: {str(e)}")

if __name__ == "__main__":
    create_superuser()