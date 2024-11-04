<template>
  <div class="container mt-5">
    <div class="content-header">
      <h2>Consulta de Produtos</h2>
      <button class="btn btn-primary" @click="irParaCadastro">
        <i class="bi bi-cart-plus-fill"></i>
        Novo Produto
      </button>
    </div>
    <hr>
    <ProdutoList 
      :produtos="produtos" 
      @editarProduto="abrirModalEdicao" 
      @excluirProduto="excluirProduto"
    />
  </div>
</template>

<script>
import ProdutoList from '@/components/ProdutoList.vue';
import ProdutoModal from '@/components/ProdutoModal.vue';

export default {
  components: { ProdutoList, ProdutoModal },
  data() {
    return { produtos: [] };
  },
  methods: {
    irParaCadastro() {
      this.$router.push('/produto/cadastro');
    },
    async carregarProdutos() {
      try {
        const response = await this.$axios.get('/produtos');
        this.produtos = response.data;
      } catch (error) {
        console.error('Erro ao carregar produtos:', error);
      }
    },
    async abrirModalEdicao(produto) {
      this.$router.push({ name: 'EditarProduto', params: { id: produto.id } });
    },
    async excluirProduto(produto) {
      try {
        await this.$axios.delete(`/produto/${produto.id}`);
        this.carregarProdutos();
        this.$toast.success('Produto deletado com sucesso!');
      } catch (error) {
        console.error('Erro ao excluir produto:', error);
        this.$toast.error(`Erro ao excluir produto:${error}`);
      }
    }
  },
  mounted() {
    this.carregarProdutos();
  }
};
</script>
<style scoped>
.content-header{
  display: flex;
  justify-content: space-between;
}
</style>