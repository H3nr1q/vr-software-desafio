import Vue from 'vue'
import VueRouter from 'vue-router'
import ProdutosPage from '@/pages/ProdutosPage.vue'
import ProdutoCadastro from '@/pages/ProdutoCadastro.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/produto',
    component: ProdutosPage
  },
  {
    path: '/produto',
    name: 'Produtos',
    component: ProdutosPage
  },
  {
    path: '/produto/cadastro',
    name: 'CadastroProduto',
    component: ProdutoCadastro
  },
  {
    path: '/produto/editar/:id',
    name: 'EditarProduto',
    component: ProdutoCadastro
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
