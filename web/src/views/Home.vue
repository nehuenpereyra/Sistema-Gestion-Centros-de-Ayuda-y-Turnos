<template>
  <div class="home">
    <div class="container py-4">
      <alert v-if="this.alert" :type="this.alert.type" :message="this.alert.message" />
      <div class="text-center py-2">
        <h2 class="text-dark mb-4">{{ config.titulo }}</h2>
        <div class="d-flex justify-content-center">
          <p class="text-secondary" style="max-width: 480px">
            {{ config.descripcion }}
          </p>
        </div>
        <div class="row">
          <div class="col-md-6 col-lg-3 d-flex justify-content-center mb-3">
            <simple-card
              title="Buscar Centro"
              description="Buscar en un mapa los centros de ayuda disponibles"
              icon="fas fa-map-marked-alt"
              link="/centros/mapa"
            />
          </div>
          <div class="col-md-6 col-lg-3 d-flex justify-content-center mb-3">
            <simple-card
              title="Solicitar Turno"
              description="Solicitar un turno de atención para uno de los centros de ayuda disponibles"
              icon="far fa-address-card"
              link="/centros"
            />
          </div>
          <div class="col-md-6 col-lg-3 d-flex justify-content-center mb-3">
            <simple-card
              title="Solicitar Centro"
              description="Solicitar la creación de un nuevo centro de ayuda"
              icon="fas fa-plus-circle"
              link="/centro/solicitud"
            />
          </div>
          <div class="col-md-6 col-lg-3 d-flex justify-content-center mb-3">
            <simple-card
              title="Estadísticas"
              description="Vér estadísticas de los centros de ayuda"
              icon="fas fa-chart-bar"
              link="/estadisticas"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SimpleCard from "@/components/SimpleCard.vue";
import Alert from "@/components/Alert.vue"
const axios = require("axios");

export default {
  name: "Home",
  components: {
    SimpleCard,
    Alert
  },
  data() {
    return {
      config: {
        contacto: "covid-19@gmail.com",
        descripcion:
          "pagina para centralizar las donaciones realizadas en los centros habilitados",
        estado_sitio: true,
        titulo: "Donaciones covid 19",
      },
      alert: this.$route.params.alert
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
          this.config = response.data;
        })
        .catch((e) => {
          console.log("Error");
          console.log(e);
        });
    },
  },
};
</script>
