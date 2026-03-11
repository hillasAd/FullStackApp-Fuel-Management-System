import pytest
from unittest.mock import MagicMock
from modules.fuel.presentation.permissions import IsManager

def test_permissao_manager_deve_negar_se_usuario_for_comum():
    permission = IsManager()
    request = MagicMock()
    request.user.role = "USER"
    
    assert permission.has_permission(request, None) is False

def test_permissao_manager_deve_permitir_se_usuario_for_manager():
    permission = IsManager()
    request = MagicMock()
    request.user.role = "MANAGER"
    
    assert permission.message == "Apenas gestores podem realizar esta acção."
