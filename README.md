
# Fuel Management System (FMS)
Uma solução completa de Gestão Logística de Combustíveis, projectada para ambientes de alta demanda e rigor operacional. Este ecossistema integra um backend robusto em Django DRF (Clean Architecture/DDD) e um frontend reativo em React 19, focados em auditabilidade, performance e experiência de utilizador.

--------------------------------------------------------------------------------------------------------------------------------------


# O Domínio de Negócio
O sistema resolve o problema crítico do controle de consumo de frotas. Mais do que um simples registo, o FMS gere o ciclo de vida de uma Intenção de Abastecimento, desde a solicitação do usuario até à confirmação.
Versões de Operação:

* V1 (Individual): Pedidos ponto-a-ponto para uma única viatura.
* V2 (Coletivo/Missão): Criação de Lotes Operacionais (Bulk Requests). Um gestor seleciona múltiplas viaturas para uma missão (ex: Escolta ou Comboio) e define cotas específicas para cada uma num único processo de aprovação.

--------------------------------------------------------------------------------------------------------------------------------------


# Regras de Negócio e Lógica de Estados (Fluxo Hierárquico)
A inteligência do sistema reside na integridade dos estados entre o BulkRequest (Pai) e os BulkRequestItem (Filhos).
# 1. Estados do Lote (Pai):

* PENDING: O lote foi criado e aguarda revisão.
* APPROVED: O lote foi validado por um gestor. Ação cascata: Todos os itens filhos passam automaticamente para APPROVED.
* REJECTED: O lote foi negado. Ação cascata: Todos os itens filhos são invalidados.
* COMPLETED: O lote só é considerado concluído quando todos os itens filhos forem abastecidos (FUELED).

# 2. Sincronização Pai-Filho:

* Independência de Abastecimento: Embora a aprovação seja coletiva, o abastecimento é individual. Uma viatura do lote pode ser abastecida hoje e outra amanhã.
* Estado do Pai dinâmico: Se um item individual for cancelado, o sistema recalcula o total do lote em tempo real para manter os KPIs de consumo precisos.

--------------------------------------------------------------------------------------------------------------------------------------

# Inteligência de Dados (Dashboards & KPIs)
O sistema transforma dados brutos em decisões através de uma camada analítica que monitoriza:

* Fluxo Semanal (L): Gráfico de barras que identifica picos de consumo por dia da semana, permitindo prever a necessidade de stock.
* Distribuição por Tipo de Combustível: Gráfico circular (Pie) que separa o consumo de Gasolina vs Diesel, essencial para gestão de custos.
* Radar de Estados: Visualização imediata de quantos pedidos estão em Aprovação, Pendente ou Concluído.
* Performance da Frota: Ranking de consumo por viatura, identificando viaturas com gastos acima da média ou possíveis anomalias.
* Atividades Recentes: Timeline em tempo real das últimas transações no sistema.

--------------------------------------------------------------------------------------------------------------------------------------

# Resumo Técnico das CamadasBackend (The Engine)

* Arquitetura: Clean Architecture com separação modular. O domínio é puro (Pure Python), isolando as regras de negócio do Django/ORM.
* Segurança: RBAC (Role-Based Access Control) diferenciando Operador, Gestores e Administradores.
* Event-Driven: Uso de um EventBus interno para que o módulo de Combustível notifique o módulo de Notificações (Email/SMS) sem acoplamento direto.
* Integridade: Locks de concorrência e transações atómicas para evitar submissões duplicadas.

# Frontend (The Interface)

* Arquitetura: Modular por Features (v1, v2, Dashboard, Auth).
* Offline-First: Integração com IndexedDB no core/offline para resiliência de dados.
* Performance: Uso de TanStack Query para cache inteligente e Zustand para um estado global ultra-leve.
* UX Avançada: Formulários dinâmicos com React Hook Form e validações complexas com Zod.

--------------------------------------------------------------------------------------------------------------------------------------

# Como Executar o Ecossistema
O projeto está preparado para ser levantado rapidamente através de scripts de automação:

#    1. Backend:
   
   cd back-end && ./scripts/create_admin.sh && python manage.py runserver
   
#    2. Frontend:
   
   cd front-end && npm install && npm run dev
   
#    3. Testes Totais:
   
   ./scripts/run_all_tests.sh  # Executa Django Tests + Cypress E2E
   
   
--------------------------------------------------------------------------------------------------------------------------------------

# Arquitetura e Desenvolvimento por Hilario Amamo
Focado em sistemas de missão crítica onde a falha não é uma opção.
--------------------------------------------------------------------------------------------------------------------------------------

