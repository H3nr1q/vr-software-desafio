<!-- src/components/PrecoModal.vue -->

<template>
  <div class="modal fade" ref="modalPreco" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ precoData ? 'Editar Preço' : 'Adicionar Preço' }}</h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="salvarPreco">
            <div class="mb-3">
              <label for="loja" class="form-label">Loja</label>
              <select id="loja" v-model="preco.lojaId" class="form-control" :disabled="precoData">
                <option v-for="loja in lojas" :key="loja.id" :value="loja.id">
                  {{ loja.codigo }} - {{ loja.descricao }}
                </option>
              </select>
            </div>
            <div class="mb-3">
              <label for="precoVenda" class="form-label">Preço de Venda (R$)</label>
              <input type="number" id="precoVenda" v-model="preco.precoVenda" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Salvar</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['produtoId'],
  data() {
    return {
      lojas: [],  // Lojas disponíveis para seleção
      preco: { lojaId: null, precoVenda: '' },  // Dados do preço
      precoData: null  // Dados de preço para edição (se houver)
    };
  },
  methods: {
    async open(preco = null) {
      this.precoData = preco;
      this.preco = preco ? { ...preco } : { lojaId: null, precoVenda: '' };
      await this.carregarLojas();  // Carrega lojas antes de abrir o modal
      $(this.$refs.modalPreco).modal('show');
    },
    close() {
      $(this.$refs.modalPreco).modal('hide');
    },
    async carregarLojas() {
      // Requisição para carregar as lojas do backend
      const response = await this.$axios.get('/lojas');
      this.lojas = response.data;
    },
    async salvarPreco() {
      try {
        if (this.precoData) {
          await this.$axios.put(`/produto/${this.produtoId}/preco/${this.preco.lojaId}`, this.preco);
        } else {
          await this.$axios.post(`/produto/${this.produtoId}/preco`, this.preco);
        }
        this.$emit('precoSalvo');  // Emite o evento para o componente pai
        this.close();
      } catch (error) {
        console.error('Erro ao salvar preço:', error);
      }
    }
  }
};
</script>
