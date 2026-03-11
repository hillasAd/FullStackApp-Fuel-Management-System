describe("Fluxo: Pedido de Abastecimento Individual", () => {
  it("deve realizar o fluxo completo dinamicamente", () => {
    // 1. Login
    cy.visit("/login");
    cy.get('input[name="username"]').type("username");
    cy.get('input[name="password"]').type("password");
    cy.get("button").contains("ENTRAR NO SISTEMA").click();

    // 2. Navegação no Menu
    cy.contains("Requisições (v1)").click();

    // 3. Abrir formulário
    cy.contains("NOVO PEDIDO").click();

    // 4. Preenchimento Dinâmico
    cy.get('select[name="vehicle_id"]')
      .find("option")
      .eq(1) // Seleciona a primeira viatura disponível (índice 1)
      .then((option) => {
        const fullText = option.text(); // Pega "LIST-01 - Toyota"
        const matricula = fullText.split(" - ")[0]; // Extrai apenas "LIST-01"

        // Guarda a matrícula para validar no final
        cy.wrap(matricula).as("viaturaSelecionada");

        // Efetua a seleção pelo valor (ID)
        cy.get('select[name="vehicle_id"]').select(option.val());
      });

    cy.get('input[name="liters"]').clear().type("20");

    // 5. Submissão
    cy.get("button").contains("SOLICITAR ABASTECIMENTO").click();

    // 6. Validação na Lista
    cy.url().should("include", "/requestsv1");

    // Recupera a matrícula guardada e verifica a primeira linha da tabela
    cy.get("@viaturaSelecionada").then((matricula) => {
      cy.get("table tbody tr")
        .first()
        .should("contain", matricula) // Procura a matrícula que o teste escolheu
        .and("contain", "PENDING"); // Garante que o status inicial é PENDING
    });
  });
});
