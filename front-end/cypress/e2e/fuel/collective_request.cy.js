describe("Fluxo: Pedido de Abastecimento Coletivo (v2)", () => {
  it("deve criar um lote operacional com 3 viaturas", () => {
    // 1. Login
    cy.visit("/login");
    cy.get('input[name="username"]').type("username");
    cy.get('input[name="password"]').type("password");
    cy.get("button").contains("ENTRAR NO SISTEMA").click();

    // 2. Navegação (Ajusta o texto se necessário)
    cy.contains("Novo Lote (v2)").click();

    const matriculasLote = [];

    // 3. Selecionar 3 viaturas dinamicamente
    for (let i = 1; i <= 3; i++) {
      cy.get("select")
        .find("option")
        .eq(i)
        .then(($opt) => {
          const fullText = $opt.text();
          const matricula = fullText.split(" - ")[0];
          matriculasLote.push(matricula);

          cy.get("select").select($opt.val());
          // Pequena espera para o React processar o estado do array 'items'
          cy.wait(200);
        });
    }

    // 4. Preencher Descrição da Missão
    cy.get('input[placeholder*="Descrição do pedido de abasteciemento"]').type(
      "Teste com cypress - Escolta Engenheiro",
    );

    // 5. Atualizar quantidades nos inputs gerados
    cy.wrap(matriculasLote).each((matricula) => {
      cy.contains(".text-blue-700", matricula) // Procura a div específica da matrícula
        .closest("div.flex") // Sobe para o container da linha (flex)
        .find('input[type="number"]') // Encontra o input único desta linha
        .clear()
        .type("30");
    });

    // 6. Submeter
    cy.get("button").contains("SUBMETER LOTE OPERACIONAL").click();

    // 7. Validação Final
    cy.url().should("include", "/requestsv2");

    // Verifica se a primeira linha da tabela tem o estado PENDING
    cy.get("table tbody tr").first().should("contain", "PENDENTE");
  });
});
