<template>
  <nav id="nav" class="navbar navbar-light navbar-expand-md">
    <div class="container-fluid">
      <router-link class="navbar-brand text-white" to="/">
        {{ title }}
      </router-link>
    </div>
  </nav>
</template>

<script>
const axios = require("axios");

export default {
  name: "Navbar",
  data() {
    return {
      title: "Donaciones covid 19",
    };
  },
  created() {
    this.fetchCenters();
  },
  methods: {
    fetchCenters() {
      axios
        .get("https://admin-grupo20.proyecto2020.linti.unlp.edu.ar/api/configuracion")
        .then((response) => {
          this.title = response.data.titulo;
        })
        .catch((e) => {
          console.log("Error");
          console.log(e);
        });
    },
  },
};
</script>

<style>
#nav {
  background: #3a6ba6;
}
</style>