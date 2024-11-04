<template>
  <div class="container mt-5">
    <h2 v-if="produto">Editar Produto</h2>
    <h2 v-else>Cadastrar Novo Produto</h2>
    <hr>
    <ProdutoForm 
      :produtoData="produto" 
      @produtoSalvo="irParaLista" 
      @produtoExcluido="irParaLista"
    />
  </div>
</template>

<script>
import ProdutoForm from '@/components/ProdutoForm.vue';

export default {
  components: { ProdutoForm },
  data() {
    return { 
      produto: null 
    };
  },
  methods: {
    async carregarProduto() {
      const produtoId = this.$route.params.id;
      if (produtoId) {
        const response = await this.$axios.get(`/produtolojas/${produtoId}`);
        const dados = response.data;
        const produtoComPrecos = {
          ...dados[0].produto,
          precos: dados.map(item => ({
            lojaId: item.loja.id,
            lojaDescricao: item.loja.descricao,
            precoVenda: item.preco_venda
          }))
        };
        this.produto = produtoComPrecos
      }
    },
    irParaLista() { 
      if (this.$route.path !== '/produto') {
        this.$router.push('/produto');
      }
    }
  },
  mounted() {
    this.carregarProduto();
  }
};
</script>
