#!/bin/bash

# ==============================================================================
# SCRIPT DE TESTES E2E (FRONTEND)
# ==============================================================================
# Descrição: Inicia o servidor Vite, corre o Cypress e encerra tudo no final.
# Permissão de Execução: chmod +x scripts/run_frontend_tests.sh
# Dependência: npm install -D wait-on
# ==============================================================================

echo "🚀 A preparar testes do Frontend..."

# 1. Instala dependências caso não existam (opcional/rápido)
npm install --quiet

# 2. Inicia o Vite em background e guarda o PID (Process ID)
echo "💻 A iniciar servidor Vite (Modo Dev)..."
npm run dev &
VITE_PID=$!

# 3. Aguarda o servidor estar pronto na porta 5173 (timeout de 30s)
echo "⏳ A aguardar pelo servidor em http://localhost:5173..."
if npx wait-on http://localhost:5173 --timeout 30000; then
    echo "✅ Servidor pronto! A iniciar Cypress..."
    
    # 4. Executa o Cypress em modo headless (apenas terminal)
    npx cypress run
    CY_STATUS=$?
else
    echo "❌ Erro: O servidor Vite não iniciou a tempo (Timeout)."
    CY_STATUS=1
fi

# 5. Limpeza: Mata o processo do Vite para libertar a porta
echo "🧹 A encerrar o servidor Vite (PID: $VITE_PID)..."
kill $VITE_PID

# Sai com o código de status do Cypress (0 = sucesso, 1 = falha)
exit $CY_STATUS
