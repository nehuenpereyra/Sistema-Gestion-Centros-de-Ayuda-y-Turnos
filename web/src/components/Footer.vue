<template>
  <footer
      class="d-flex justify-content-center justify-content-sm-center justify-content-md-center justify-content-lg-center align-items-lg-center justify-content-xl-center mt-auto"
      style="
        background-color: #3a6ba6;
        position: relative;
        clear: both;
        margin-top: -150px;
      "
    >
      <small
        class="d-xl-flex justify-content-xl-center"
        style="color: rgb(255, 255, 255)"
        ><br />{{title}} © 2020 - Contacto: {{contact}}<br /><br
      /></small>
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
