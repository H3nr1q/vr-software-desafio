describe('API Test', () => {
  it('Verificando se rota esta retornando status 200', () => {
    
    const apiUrlProdutos = 'http://127.0.0.1:5000/produtos';

    cy.request(apiUrlProdutos)
      .then((response) => {
        expect(response.status).to.eq(200);
        expect(response.body).to.be.an('array');
        expect(response.body).to.have.length.greaterThan(0)
        response.body.forEach(item => {
          expect(item).to.have.all.keys('custo', 'descricao', 'id', 'imagem');
        });
      })
  })
})