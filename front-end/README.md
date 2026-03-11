
# Fuel Management System | Front-End Operacional
Este projeto é a interface de alta performance para a gestão logística de combustíveis. Não se trata de um CRUD comum, mas de uma aplicação desenhada para cenários reais: baixa conectividade, fluxos críticos de aprovação e alta densidade de dados.
Desenvolvido com React 19, Vite e Tailwind CSS v4, o sistema utiliza uma arquitetura modular que separa rigorosamente a interface da lógica de infraestrutura.

--------------------------------------------------------------------------------------------------------------------------------------

# Decisões de Arquitetura (Clean Architecture)
A organização das pastas reflete uma preocupação com a manutenção a longo prazo:

* Core (A espinha dorsal): Onde reside a inteligência que não depende da UI. Implementámos gestão de Sessão (JWT), interceptores de API e, crucialmente, uma camada de Offline-First utilizando IndexedDB para garantir que a operação não para se a internet falhar.
* Features (Verticalização): Cada funcionalidade (Dashboard, Requisições v1/v2, Veículos) é tratada como um micro-app. Isto permite que a equipa trabalhe em novas versões (como a FuelRequestV2) sem tocar no código estável da versão anterior.
* Shared (Reutilização): Uma biblioteca interna de componentes atómicos, hooks e utilitários que garante a consistência visual em todo o sistema.

--------------------------------------------------------------------------------------------------------------------------------------

# Diferenciais Técnicos

* Estado Assíncrono (TanStack Query): Toda a sincronização com o Django é gerida por cache inteligente, reduzindo o tráfego de rede e eliminando "loaders" desnecessários.
* Validação de Dados Dupla: Utilizamos React Hook Form com Zod/Yup para garantir que nenhum dado inválido saia do cliente, poupando recursos do servidor.
* Gestão de Estado Atómica: Com Zustand, mantemos o estado global (como preferências e alertas) leve e reativo, sem o peso do Redux.
* Visualização Analítica: Integração com Recharts para transformar logs de abastecimento em KPIs visuais imediatos para os gestores.

--------------------------------------------------------------------------------------------------------------------------------------

# Como Rodar o Ecossistema. 

# 1. Clonagem e Dependências

git clone https://github.com/endereco-do-projecto
cd front-end
npm install

# 2. Ambiente de Desenvolvimento
Certifica-te de configurar as URLs do Backend no ficheiro .env (Baseado no .env.example):

npm run dev

# 3. Garantia de Qualidade (Testes)
O sistema está coberto por testes E2E para garantir que os fluxos críticos de negócio nunca quebrem:

# Executar testes end-to-end com Cypress
npx cypress run

--------------------------------------------------------------------------------------------------------------------------------------

# Próximos Passos (Roadmap)

* i18n: Suporte multi-idioma (Português/Inglês) já em estrutura de pastas.
* PWA: Instalação nativa no browser para uso em dispositivos móveis no terreno.

--------------------------------------------------------------------------------------------------------------------------------------
# Engenharia de Software por Hilario Amamo
