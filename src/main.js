import Vue from 'vue'
import App from './App.vue'
import axios from 'axios';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import routes from './router'
import VueRouter from 'vue-router'
import Vuex from 'vuex'
Vue.use(VueRouter)
// axios.defaults.baseURL = 'http://202.120.1.63:6545';
Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    count: 0,
    color: ['#325B69', '#698570', '#AE5548', '#6D9EA8', '#9CC2B0', '#C98769']
  }
});
const router = new VueRouter({
  routes 
})
Vue.config.productionTip = false
Vue.prototype.$axios = axios
Vue.use(ElementUI);
new Vue({
  store,
  router,
  data: {
    charts: []
  },
  render: h => h(App),
}).$mount('#app')

