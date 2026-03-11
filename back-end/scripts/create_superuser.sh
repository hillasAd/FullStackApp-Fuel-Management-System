#!/bin/bash

# ==============================================================================
# SCRIPT DE CRIAÇÃO DE SUPERUSER (DJANGO)
# ==============================================================================
# Permissão de Execução: chmod +x scripts/create_admin.sh
# Execução: ./scripts/create_admin.sh
# ==============================================================================

# 1. Carrega as variáveis do .env se existir (opcional)
if [ -f .env ]; then
  # O xargs garante que as variáveis sejam exportadas corretamente para o ambiente do script
  export $(grep -v '^#' .env | xargs)
fi

echo "🚀 A criar superuser via Django Shell..."

# 2. Executa o comando injetando Python diretamente no Shell do Django
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()
# Podes usar valores fixos ou tentar ler do .env carregado acima
username = 'admin'
email = 'admin@exemplo.com'
password = '#123admin@'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username, 
        email=email, 
        password=password,
        role='ADMIN'
    )
    print(f'✅ Superuser "{username}" criado com sucesso!')
else:
    print(f'ℹ️  Superuser "{username}" já existe. Operação ignorada.')
EOF

# 3. Status final
echo "🏁 Script de administração concluído."
