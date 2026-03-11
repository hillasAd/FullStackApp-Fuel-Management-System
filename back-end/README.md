
# FUEL MANAGEMENT SYSTEM
--------------------------------------------------------------------------------------------------------------------------------------

# Objetivos e Requisitos do Sistema
O sistema orquestra três fluxos fundamentais:

* Auth Module: Gestão de identidade e autenticação via JWT.
* Fuel Management: Módulo core versionado para controlo de combustível.
* v1: Gestão de abastecimentos individuais por viatura.
* v2: Gestão operacional por Lotes de Viaturas.
* Notifications: Motor de comunicação desacoplado (Email e SMS).

# Funcionalidades de Infraestrutura:

* Idempotência e transações atômicas seguras.
* RBAC (Role-Based Access Control) e ABAC.
* Observabilidade (Correlation ID e logs de rastreabilidade).

--------------------------------------------------------------------------------------------------------------------------------------

# Arquitetura de Pastas
Estrutura de monólito modular com isolamento de responsabilidades:

config/                 # Configurações globais, JWT, PostgreSQL, Exceptions
shared/                 # Middleware, padronização de respostas, EventBus
modules/                # Domínios de negócio isolados
    authentication/
    notifications/
    fuel/               # Core v1
    fuelv2/             # Core v2 (Lotes)
    dashboard/          # KPIs e cálculos analíticos

--------------------------------------------------------------------------------------------------------------------------------------

# Definição dos Módulos

# 1. Authentication & Notifications

* Authentication: Módulo independente focado em login e tokens. Não possui dependências com outros módulos.
* Notifications: Reage a Eventos de Domínio publicados no EventBus. Suporta SMTP e Mock de SMS, garantindo desacoplamento total do fluxo de combustível.

# 2. Fuel & FuelV2 (Core Domain)
A lógica de negócio está protegida em camadas que não dependem do framework:

* Domain: Entidades puras, Value Objects e interfaces (Repository Pattern). Zero dependência de Django ou DRF.
* Application: Casos de uso e orquestração de eventos.
* Infrastructure: Implementação concreta do Django ORM, QuerySets e Locks de concorrência.
* Presentation: Views e Serializers DRF. Converte HTTP em DTOs e invoca os casos de uso.
* Integrations: Portas de comunicação entre módulos (Ports) preparadas para comunicação via Broker (Kafka/RabbitMQ) no futuro.

--------------------------------------------------------------------------------------------------------------------------------------

# Estratégia de Testes
A pirâmide de testes garante a estabilidade do sistema:

* Unitários: Entidades e regras de negócio isoladas.
* Integração: Persistência, Transações e Eventos.

--------------------------------------------------------------------------------------------------------------------------------------

# Como Executar o Projeto

# 1. Preparar o Ambiente

git clone https://github.com/endereco-do-projecto
cd back-end
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Instalação e Configuração

pip install -r requirements.txt


* Variáveis de Ambiente: Renomeie .env.example para .env e preencha as credenciais. Certifique-se de criar a Base de Dados PostgreSQL manualmente.

# 3. Automatização (Scripts de Apoio)
Estes scripts automatizam tarefas recorrentes:

* Configurar Admin: ./scripts/create_admin.sh (Edite o ficheiro para definir as suas credenciais).
* Testes Backend: ./scripts/run_tests.sh
* Testes E2E (Front+Back): ./scripts/run_all_tests.sh

# 4. Inicialização do Servidor

python manage.py migrate                    # criar estrutura das tabelas na base de dados
python manage.py seed_dashboard             # inserir dados aleatorios para analise: 10 viaturas; 500 requisicoes na v1 e 2000 na v2
python manage.py runserver                  # correr o servidor backend

# 5. Cobertura de Código

pytest --cov=modules

--------------------------------------------------------------------------------------------------------------------------------------

# Desenvolvido por Hilario Amamo
--------------------------------------------------------------------------------------------------------------------------------------
