<template>
  <form @submit.prevent="submit">
    <div class="produto-form-layout">
      <div class="produto-form-container">
        <div class="produto-data-row">
          <div class="produto-codigo">
            <label for="codigo">Código</label>
            <input
              type="text"
              id="codigo"
              :value="produto.id ? produto.id : codigo"
              class="form-control"
              disabled
            />
          </div>
          <div class="produto-descricao">
            <label for="descricao" class="form-label">Descrição</label>
            <input
              type="text"
              id="descricao"
              v-model="produto.descricao"
              class="form-control"
              required
              maxlength="60"
              pattern="[A-Za-z0-9\s]+"
            />
          </div>
          <div class="produto-custo">
            <label for="custo" class="form-label">Custo (R$)</label>
            <input
              v-model="produto.custo"
              class="form-control"
              step="0.01"
              placeholder="Preço de custo"
              v-money="{ 
                prefix: '', 
                decimal: '.', 
                thousands: '',
                precision: 3 
              }"
            />
          </div>
        </div>
        <div>
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
              <tr v-for="preco in produto.precos" :key="preco.lojaId">
                <td>{{ preco.lojaDescricao }}</td>
                <td>{{ preco.precoVenda }}</td>
                <td>
                  <button
                    type="button"
                    class="btn btn-warning"
                    @click="editarPreco(preco)"
                  >
                    <i class="bi bi-pencil"></i>
                  </button>
                  <button
                    type="button"
                    class="btn btn-danger"
                    @click="removerPreco(preco.lojaId)"
                  >
                    <i class="bi bi-trash"></i>
                  </button>
                </td>
              </tr>
              <tr>
                <td>
                  <select v-model="precosVenda.lojaId" class="form-control">
                    <option disabled value="">Selecione uma loja</option>
                    <option v-for="loja in lojas" :key="loja.id" :value="loja.id">
                      {{ loja.id }}-{{ loja.descricao }}
                    </option>
                  </select>
                </td>
                <td>
                  <input
                    v-model="precosVenda.precoVenda"
                    class="form-control"
                    placeholder="Preço de venda"
                    step="0.01"
                    v-money="{ 
                      prefix: '', 
                      decimal: '.', 
                      thousands: '',
                      precision: 3 
                    }"
                  />
                </td>
                <td>
                  <button type="button" class="btn btn-success" @click="adicionarPreco">
                    <i class="bi bi-plus"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="mb-3">
        <div class="produto-imagem-container">
          <img
            :src="`data:image/jpeg;base64,${produto.imagem}`"
            alt="Imagem do Produto"
            class="produto-imagem"
          />
          <input
            type="file"
            id="imagem"
            @change="onFileChange"
            accept=".jpg, .jpeg, .png"
          />
        </div>
      </div>
    </div>
    <button type="submit" class="btn btn-primary" :disabled="!temPrecoVenda()">
      <i class="bi bi-floppy-fill"></i>
      Salvar
    </button>
    <button type="button" class="btn btn-danger" @click="excluirProduto">
      <i class="bi bi-trash"></i>
      Excluir
    </button>
  </form>
</template>

<script>
export default {
  props: ["produtoData"],
  data() {
    return {
      codigo: "-1", 
      produto: {
        id: "",
        descricao: "",
        custo: "",
        precos: [],
        imagem: null,
      },
      lojas: [],
      precosVenda: { lojaId: "", precoVenda: "" }, // Dados temporários para um novo preço
    };
  },
  watch: {
    produtoData: {
      immediate: true,
      handler(newData) {
        if (newData) {
          this.produto = { ...newData };
          this.produto.imagem = newData.imagem;
        }
      },
    },
  },
  methods: {
    async onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        const validExtensions = ["image/jpeg", "image/png"];
        if (validExtensions.includes(file.type)) {
          const reader = new FileReader();
          reader.onload = (e) => {
            this.produto.imagem = e.target.result.split(",")[1];
          };
          reader.readAsDataURL(file);
        } else {
          alert("Por favor, selecione um arquivo JPG ou PNG.");
        }
      }
    },
    async carregarLojas() {
      try {
        const response = await this.$axios.get("/lojas");
        this.lojas = response.data;
      } catch (error) {
        console.error("Erro ao carregar lojas:", error);
      }
    },
    adicionarPreco() {
      const loja = this.lojas.find((loja) => loja.id === this.precosVenda.lojaId);
      if (!loja || !this.precosVenda.precoVenda) {
        return alert("Selecione uma loja e insira um preço de venda válido.");
      }
      
      const precoExistente = this.produto.precos.find(
        (preco) => preco.lojaId === this.precosVenda.lojaId
      );
      
      if (precoExistente) {
        this.$toast.error(`Já existe um preço cadastrado para esta loja!`);
        return;
      }

      this.produto.precos.push({
        lojaId: this.precosVenda.lojaId,
        lojaDescricao: loja.descricao,
        precoVenda: this.precosVenda.precoVenda,
      });

      this.precosVenda = { lojaId: "", precoVenda: "" };
    },
    removerPreco(lojaId) {
      this.produto.precos = this.produto.precos.filter(
        (preco) => preco.lojaId !== lojaId
      );
    },
    editarPreco(preco) {
      this.precosVenda = { ...preco };
      this.produto.precos = this.produto.precos.filter((p) => p.lojaId !== preco.lojaId);
    },
    async excluirProduto() {
      if (confirm("Tem certeza que deseja excluir este produto?")) {
        try {
          await this.$axios.delete(`/produto/${this.produtoData.id}`);
          this.$toast.success('Produto deletado com sucesso!');
          this.$emit("produtoExcluido");
        } catch (error) {
          console.error("Erro ao excluir produto:", error);
        }
      }
    },
    temPrecoVenda() {
      return this.produto.precos.some((preco) => preco.precoVenda > 0);
    },
    async submit() {
      const formData = new FormData();
      formData.append("descricao", this.produto.descricao);
      formData.append("custo", this.produto.custo);
      
      const byteCharacters = atob(this.produto.imagem);
      const byteNumbers = new Array(byteCharacters.length);
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      const blob = new Blob([byteArray], { type: "image/jpeg" });
      
      formData.append("imagem", blob);
      
      this.produto.precos.forEach((preco) => {
        formData.append("precos[]", JSON.stringify(preco)); // Usei 'precos[]' para enviar como uma lista
      });

      try {
        const response = this.produtoData
        ? await this.$axios.put(`/produto/${this.produtoData.id}`, formData)
        : await this.$axios.post("/produto", formData);
        
        if(response.status == 200){
          this.$toast.success(`Produto atualizado com sucesso!`);
        }
        else{
          this.$toast.success(`Produto cadastrado com sucesso!`);
        }
        this.$emit("produtoSalvo", response.data);
      } catch (error) {
        console.error("Erro ao salvar produto:", error);
      }
    },
  },
  async created() {
    await this.carregarLojas();
    if (!this.produtoData) {
      await this.obterProximoCodigo();
    }
  },
};
</script>
<style scoped>
.produto-form-container {
  display: flex;
  flex-direction: column;
  margin-right: 1%;
}

.produto-form-layout {
  display: flex;
  flex-direction: row;
}

.produto-data-row {
  display: flex;
  justify-content: space-between;
}

.produto-codigo {
  width: 10%;
}

.produto-descricao {
  width: 60%;
}

.produto-custo {
  width: 25%;
}

.produto-imagem-container {
  width: 200px; 
  height: 150px;
  overflow: hidden;
  position: relative; 
}

.produto-imagem {
  width: 100%; 
  height: auto;
  object-fit: cover;
}
</style>
