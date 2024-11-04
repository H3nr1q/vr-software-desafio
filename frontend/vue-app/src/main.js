import Vue from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import axios from 'axios'
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";


Vue.config.productionTip = false

// Inicialize o axios globalmente
Vue.prototype.$axios = axios

// Configure o axios com a baseURL
axios.defaults.baseURL = 'http://localhost:5000';

Vue.use(Toast, {
  // top-right, top-center, top-left, bottom-right, bottom-center, bottom-left.
  position: 'bottom-right',
  // place newest toast on the top
  newestOnTop: true,
  // the max number of toasts
  maxToasts: 20,
  // name of the Vue Transition or object with classes to use
  // only enter-active, leave-active and move are applied.
  transition: 'Vue-Toastification__bounce',
  // duration in ms
  // or an object: {enter: Number, leave: Number}
  transitionDuration: 750,
  // allows to dismiss by drag & swipe events
  draggable: true, 
  draggablePercent: 0.6,
  // auto pause when out of focus
  pauseOnFocusLoss: true,
  // auto pause on hover
  pauseOnHover: true,
  // close on click
  closeOnClick: true,
  // auto dismiss after this timeout
  timeout: 5000,
  // container element
  container: document.body,
  // custom classes
  toastClassName: [],
  // body classes
  bodyClassName: [],
  // show/hide the progress bar
  hideProgressBar: false,
  // show/hide the close button
  hideCloseButton: false,
  // custom icons here
  icon: true
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
