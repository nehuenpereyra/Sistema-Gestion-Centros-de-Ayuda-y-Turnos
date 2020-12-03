<template>
  <footer
      class="py-4 border-top"
      style="background-color: #3a6ba6; position: absolute;bottom: 0;width: 100%;">
      <small class="d-flex justify-content-center text-white">
        {{title}} © 2020 - Contacto: {{contact}}
      </small>
  </footer>
</template>

<script>
const axios = require("axios");

export default {
  name: "Footer",
  data() {
    return {
      title: "Donaciones covid 19",
      contact: "donaciones@covid19.com"
    };
  },
  created() {
    this.fetchCenters();
  },
  methods: {
    fetchCenters() {
      axios
        .get("http://127.0.0.1:5000/api/configuracion")
        .then((response) => {
          this.title = response.data.titulo;
          this.contact = response.data.contacto;
        })
        .catch((e) => {
          console.log("Error");
          console.log(e);
        });
    },
  },
};
</script>
