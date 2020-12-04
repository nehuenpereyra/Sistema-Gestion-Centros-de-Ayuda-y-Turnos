<template>
  <div id="app" style="min-height: 100%">
    <div style="margin-bottom: 100px">
      <navbar />
      <div
        class="container clear-top"
        style="overflow: auto; padding-bottom: 150px"
      >
        <router-view />
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";

const axios = require('axios');
const axiosApi = axios.create({
  baseURL: "https://admin-grupo20.proyecto2020.linti.unlp.edu.ar"
});

export default {
  name: "App",
  components: {
    Navbar,
    Footer,
  },
  data() {
    return {
      pageStatus: null
    }
  },
  methods: {
    async fetchPageStatus() {

      try {
        
        const response = await axiosApi.get("/api/configuracion");
        this.pageStatus = {
          title: response.data.titulo,
          description: response.data.descripcion,
          contact: response.data.contacto,
          active: response.data.estado_sitio
        }
        
      } catch (error) {
        
        this.pageStatus = {
          active: false
        }

      }

    }
  },
  created() {
    this.fetchPageStatus();
  },
  watch: {
    $route() {
      this.fetchPageStatus();
    },
    pageStatus() {
      if (!this.pageStatus.active)
        this.$router.push({ name: "Maintenance" });
    }

  }
};
</script>
