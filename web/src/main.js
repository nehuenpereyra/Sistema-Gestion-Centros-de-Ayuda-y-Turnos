import Vue from "vue";
import App from "./App.vue";
import router from "./router";

Vue.config.productionTip = false;

import "../../app/static/bootstrap/css/bootstrap.min.css";
import "../../app/static/fonts/fontawesome-all.min.css";
import "leaflet/dist/leaflet.css";

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
