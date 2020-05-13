import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify";
import VueGtag from "vue-gtag"; // Google Analytics

Vue.use(
  VueGtag,
  {
    config: { id: "UA-163755956-1" },
  },
  router
);

import { store } from "./store/store";

Vue.config.productionTip = false;

new Vue({
  store,
  router,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
