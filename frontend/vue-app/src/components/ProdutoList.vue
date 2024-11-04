<template>
  <div>
    <div class="filtros">
      <div class="produto-codigo">
        <label for="codigo">Código</label>
        <input v-model="filtros.codigo" class="form-control" placeholder="Filtrar por código" @input="filtrarProdutos" />
      </div>
      <div class="produto-descricao">
        <label for="codigo">Descrição</label>
        <input v-model="filtros.descricao" class="form-control" placeholder="Filtrar por descrição" @input="filtrarProdutos" />
      </div>
      <div class="produto-custo">
        <label for="codigo">Custo</label>
        <input v-model="filtros.custo" class="form-control" placeholder="Filtrar por custo" type="number" @input="filtrarProdutos" />
      </div>
    </div>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Código</th>
          <th>Descrição</th>
          <th>Custo</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="produto in produtosFiltrados" :key="produto.id">
          <td>{{ produto.id }}</td>
          <td>{{ produto.descricao }}</td>
          <td>{{ produto.custo }}</td>
          <td>
            <button class="btn btn-primary me-2" @click="$emit('editarProduto', produto)">
              <i class="bi bi-pencil"></i>
            </button>
            <button class="btn btn-danger" @click="$emit('excluirProduto', produto)">
              <i class="bi bi-trash"></i>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: ['produtos'],
  data() {
    return {
      filtros: {
        codigo: '',
        descricao: '',
        custo: '',
        precoVenda: ''
      },
      produtosFiltrados: []
    };
  },
  watch: {
    produtos: {
      immediate: true,
      handler() {
        this.filtrarProdutos();
      }
    }
  },
  methods: {
    filtrarProdutos() {
      this.produtosFiltrados = this.produtos.filter(produto => {
        const codigoMatch = this.filtros.codigo
          ? produto.id.toString().includes(this.filtros.codigo)
          : true;
        const descricaoMatch = this.filtros.descricao
          ? produto.descricao.toLowerCase().includes(this.filtros.descricao.toLowerCase())
          : true;
        const custoMatch = this.filtros.custo
          ? produto.custo.toString().includes(this.filtros.custo)
          : true;
        // const precoVendaMatch = this.filtros.precoVenda
        //   ? produto.precos.some(preco => preco.precoVenda === parseFloat(this.filtros.precoVenda))
        //   : true;

        return codigoMatch && descricaoMatch && custoMatch; //&& precoVendaMatch;
      });

    }
  },
  mounted() {
    this.produtosFiltrados = this.produtos;
  }
};
</script>
<style scoped>
.filtros{
  display: flex;
  justify-content: space-between;
  padding-bottom: 1%;
  padding: auto;
}
.produto-codigo{
  width: 10%;
}

.produto-descricao{
  width: 60%;
}

.produto-custo{
  width: 25%;
}
</style>
