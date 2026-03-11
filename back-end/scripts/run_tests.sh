#!/bin/bash

# 1. Ativar o venv (ajusta o caminho se o teu venv tiver outro nome)
source venv/Scripts/activate || source venv/bin/activate

echo "🚀 A preparar ambiente de testes..."

# 2. Garantir que as dependências estão ok
pip install -r requirements.txt --quiet

# 3. Correr migrações (evita erros de DB nos testes)
python manage.py migrate

echo "🧪 A executar testes do Django (DRF)..."

# 4. Executar os testes
# Se usares o test runner padrão do Django:
python manage.py test

# SE USARES PYTEST (Recomendado para Clean Arch):
# pytest

echo "✅ Testes concluídos!"
