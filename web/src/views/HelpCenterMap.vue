<template>
  <div
    class="container text-center flex-row justify-content-center align-content-center"
  >
    <h4 class="text-left mt-4">Mapa de los Centros de Ayuda</h4>
    <div style="display: flex; justify-content: center">
      <div style="height: 600px; width: 100%" class="border">
        <l-map
          :zoom="zoom"
          :center="center"
          :bounds="bounds"
          :max-bounds="maxBounds"
          style="height: 100%"
        >
          <l-tile-layer :url="url" />
          <l-marker
            v-for="item in markers"
            :key="item.name"
            :lat-lng="item.location"
          >
            <l-popup>
              <div>
                <h3>{{ item.name }}</h3>
                <div>Dirección: {{ item.direction }}</div>
                <div>Horario: {{ item.schedule }}</div>
                <div>Telefono: {{ item.telephone }}</div>
              </div>
            </l-popup>
          </l-marker>
        </l-map>
      </div>
    </div>
  </div>
</template>

<script>
import { latLng, latLngBounds, Icon } from "leaflet";
import { LMap, LTileLayer, LMarker, LPopup } from "vue2-leaflet";
const axios = require("axios");

delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

export default {
  name: "HelpCenterMap",
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPopup,
  },
  data() {
    return {
      zoom: 9,
      center: latLng(-34.658, -58.474),
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      bounds: latLngBounds([
        [-34.1959, -58.966],
        [-35.077, -57.73],
      ]),
      maxBounds: latLngBounds([
        [-34.1959, -58.966],
        [-35.077, -57.73],
      ]),
      markers: [],
    };
  },
  created() {
    this.fetchCenters();
  },
  methods: {
    fetchCenters() {
      axios
        .get("https://admin-grupo20.proyecto2020.linti.unlp.edu.ar/api/tipos_centros", {
          params: { por_pagina: 0 },
        })
        .then((response) => {
          axios
            .get("https://admin-grupo20.proyecto2020.linti.unlp.edu.ar/api/centros", {
              params: { por_pagina: response.data.total },
            })
            .then((response) => {
              response.data.centros.forEach((item) => {
                if (item.latitude != null)
                  this.markers.push({
                    name: item.nombre,
                    direction: item.direccion,
                    telephone: item.telefono,
                    schedule: `${item.hora_apertura} - ${item.hora_cierre}`,
                    location: latLng(item.latitude, item.longitude),
                  });
              });
            })
            .catch((e) => {
              console.log("Error");
              console.log(e);
            });
        })
        .catch((e) => {
          console.log("Error");
          console.log(e);
        });
    },
  },
};
</script>