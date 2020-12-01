import Vue from "vue";
import App from "./App.vue";
import router from "./router";

Vue.config.productionTip = false;

import "../../app/static/bootstrap/css/bootstrap.min.css";
import "../../app/static/fonts/fontawesome-all.min.css";
import "leaflet/dist/leaflet.css";

// import "https://code.jquery.com/jquery-3.5.1.slim.min.js"
// import "https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js"

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
