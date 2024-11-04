<!-- src/components/ProdutoModal.vue -->

<template>
  <div v-if="show" class="modal fade" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            {{ localProduto ? "Editar Produto" : "Novo Produto" }}
          </h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>
        <div class="modal-body">
          <ProdutoForm 
            :produtoData="localProduto" 
            @produtoSalvo="produtoSalvo" 
          />

          <!-- Tabela de lojas e preços de venda -->
          <h5 class="mt-4">Preços de Venda por Loja</h5>
          <table class="table">
            <thead>
              <tr>
                <th>Loja</th>
                <th>Preço de Venda (R$)</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="preco in localProduto.precos" :key="preco.lojaId">
                <td>{{ preco.id - preco.lojaDescricao }}</td>
                <td>{{ preco.precoVenda }}</td>
                <td>
                  <button class="btn btn-primary" @click="editarPreco(preco)">
                    Editar
                  </button>
                  <button class="btn btn-danger" @click="excluirPreco(preco)">
                    Excluir
                  </button>
                </td>
              </tr>
              <!-- Linha para adicionar novo preço -->
              <tr>
                <td>
                  <select v-model="novoPreco.lojaId" class="form-control">
                    <option disabled value="">Selecione uma loja</option>
                    <option v-for="loja in lojas" :key="loja.id" :value="loja.id">
                      {{ loja.codigo }} - {{ loja.descricao }}
                    </option>
                  </select>
                </td>
                <td>
                  <input
                    type="number"
                    v-model="novoPreco.precoVenda"
                    class="form-control"
                    placeholder="Preço de venda"
                    required
                  />
                </td>
                <td>
                  <button type="button" class="btn btn-success" @click="adicionarPreco">
                    Adicionar
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="close">Fechar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ProdutoForm from "./ProdutoForm.vue";

export default {
  components: { ProdutoForm },
  props: ["produtoData"],
  data() {
    return {
      show: false, // Controla a visibilidade do modal
      localProduto: null,
      produto: {...this.produtoData},
      lojas: [],
      novoPreco: { lojaId: "", precoVenda: "" },
    };
  },
  methods: {
    open(produto) {
    this.localProduto = { ...produto};
    
    this.show = true; // Exibe o modal
    console.log("Modal deve estar aberto:", this.show);
    },
    close() {
      this.show = false; // Oculta o modal
    },
    produtoSalvo(produto) {
      // Manipulador para quando o produto for salvo no ProdutoForm
      this.close();  // Fecha o modal após salvar o produto
      this.$emit('produtoSalvo', produto);  // Emite o evento para o componente pai (ProdutosPage)
    },
    adicionarPreco() {
      const loja = this.lojas.find((loja) => loja.id === this.novoPreco.lojaId);
      if (!loja || !this.novoPreco.precoVenda) {
        return alert("Selecione uma loja e insira um preço de venda válido.");
      }

      this.localProduto.precos.push({
        lojaId: this.novoPreco.lojaId,
        lojaDescricao: loja.descricao,
        precoVenda: this.novoPreco.precoVenda,
      });
      this.novoPreco = { lojaId: "", precoVenda: "" };
    },
    async carregarLojas() {
      const response = await this.$axios.get("/lojas");
      this.lojas = response.data;
    },
    async excluirPreco(preco) {
      try {
        await this.$axios.delete(`/produto/${this.produtoData.id}/preco/${preco.lojaId}`);
        this.produtoData.precos = this.produtoData.precos.filter(
          (p) => p.lojaId !== preco.lojaId
        );
      } catch (error) {
        console.error("Erro ao excluir preço:", error);
      }
    },
  },
  async created() {
    await this.carregarLojas();
  },
};
</script>
