import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/about",
    name: "About",
    component: () => import("@/views/About.vue"),
  },
  {
    path: "/centros/:center_id/reserva",
    name: "Reservation",
    component: () => import("@/views/Reservation.vue"),
  },
  {
    path: "/centro/solicitud",
    name: "HelpCenterRequest",
    component: () => import("@/views/HelpCenterRequest.vue"),
  },
  {
    path: "/centros/mapa",
    name: "HelpCenterMap",
    component: () => import("@/views/HelpCenterMap.vue"),
  },
  {
    path: "/centros",
    name: "HelpCenterList",
    component: () => import("@/views/HelpCenterList.vue")
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
