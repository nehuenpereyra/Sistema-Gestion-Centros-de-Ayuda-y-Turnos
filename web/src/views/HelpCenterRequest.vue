<template>
  <div
    class="container my-4"
    style="
      /*overflow: auto;*/ /*padding-bottom: 150px;*/ /*background: white;*/
    "
  ><div
        v-if="alert"
        class="alert alert-danger alert-dismissible fade show mt-2"
        role="alert"
      >
        Hubo un <strong>error</strong> en la solicitud del turno
        <button
          type="button"
          class="close"
          data-dismiss="alert"
          aria-label="Close"
        >
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
    <h5 class="mt-3">Solicitar Centro</h5>
    <div class="text-left">Los campos con (*) son obligatorios.</div>
    <div class="bg-white border rounded shadow-sm mt-3 p-3">
      <form method="post" @submit.prevent="submit">
        <div class="form-row">
          <div class="col">
            <div class="form-group">
              <label for="name_input">Nombre*</label>
              <input
                class="form-control"
                type="text"
                id="name_input"
                name="name"
                v-model="name"
                required
              />
            </div>
          </div>
        </div>
        <div class="form-row">
          <div class="col-12 col-sm-6">
            <div class="form-group">
              <label for="address_input">Dirección*</label>
              <input
                class="form-control"
                type="text"
                id="address_input"
                name="address"
                v-model="address"
                required
              />
            </div>
          </div>
          <div class="col-12 col-sm-6">
            <div class="form-group">
              <label for="phone_input">Teléfono*</label>
              <input
                class="form-control"
                type="tel"
                id="phone_input"
                name="phone"
                v-model="phone"
                required
              />
            </div>
          </div>
        </div>
        <div class="form-row">
          <div class="col-12 col-sm-6">
            <div class="form-group">
              <label for="opening_time_input">Hora de Apertura*</label>
              <input
                class="form-control"
                id="opening_time_input"
                type="time"
                name="opening_time"
                v-model="opening_time"
                required
              />
            </div>
          </div>
          <div class="col-12 col-sm-6">
            <div class="form-group">
              <label for="closing_time_input">Hora de Cierre*</label>
              <input
                class="form-control"
                id="closing_time_input"
                type="time"
                name="closing_time"
                v-model="closing_time"
                required
              />
            </div>
          </div>
        </div>
        <div class="form-row">
          <div class="col">
            <div class="form-group">
              <label for="type_input">Tipo de Centro*</label>
              <select
                class="form-control"
                id="type_input"
                name="type"
                v-model="type"
                required
              >
                <option disabled value="">Por favor, seleccione uno</option>
                <option
                  v-for="type of types"
                  :value="type.nombre"
                  :key="type.id"
                >
                  {{ type.nombre }}
                </option>
              </select>
            </div>
          </div>
        </div>
        <div class="form-row">
          <div class="col">
            <div class="form-group">
              <label for="town_input">Municipio*</label>
              <select
                class="form-control"
                id="town_input"
                name="town"
                v-model="town"
                required
              >
                <option disabled value="">Por favor, seleccione uno</option>
                <option v-for="town of towns" :value="town.name" :key="town.id">
                  {{ town.name }}
                </option>
              </select>
            </div>
          </div>
        </div>
        <div class="form-row">
          <div class="col">
            <div class="form-group">
              <label for="web_input">Sitio Web</label>
              <input
                class="form-control"
                type="url"
                id="web_input"
                name="web"
                v-model="web"
              />
            </div>
          </div>
        </div>
        <div class="form-row">
          <div class="col">
            <div class="form-group">
              <label for="email_input">Correo Electrónico</label>
              <input
                class="form-control"
                type="email"
                id="email_input"
                name="email"
                v-model="email"
              />
            </div>
          </div>
        </div>
        <label>Localización</label>
        <div style="height: 600px; width: 100%" class="border">
          <l-map
            :zoom="zoom"
            :center="center"
            :bounds="bounds"
            :max-bounds="maxBounds"
            @click="addMarker"
            style="height: 100%"
          >
            <l-tile-layer :url="url" />
            <l-marker  v-if="marker" :key="marker.lat" :lat-lng="marker"> </l-marker>
          </l-map>
        </div>
        <div class="d-flex justify-content-center justify-content-sm-end">
          <button class="btn btn-primary mt-3" type="submit">
            Enviar Solicitud
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { latLngBounds, Icon, latLng } from "leaflet";
import { LMap, LTileLayer, LMarker } from "vue2-leaflet";
const axios = require("axios");

delete Icon.Default.prototype._getIconUrl;
Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

const axiosApi = axios.create({
  baseURL: "https://grupo20.proyecto2020.linti.unlp.edu.ar",
  headers: { "Content-Type": "application/json" },
});

const axiosReferenceApi = axios.create({
  baseURL: "https://api-referencias.proyecto2020.linti.unlp.edu.ar",
});

export default {
  name: "HelpCenterRequest",
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  data() {
    return {
      name: "",
      address: "",
      phone: "",
      opening_time: "",
      closing_time: "",
      type: "",
      town: "",
      web: "",
      email: "",
      types: [],
      towns: [],
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
      marker: null,
      alert: false,
    };
  },
  methods: {
    addMarker(event) {
      this.marker = event.latlng;
    },
    async getTowns() {
      try {
        const firstResponse = await axiosReferenceApi.get("/municipios", {
          params: { per_page: 0 },
        });

        const response = await axiosReferenceApi.get("/municipios", {
          params: { per_page: firstResponse.data.total },
        });

        this.towns = Object.values(response.data.data.Town);
      } catch (error) {
        this.towns = [];
      }
    },
    async getHelpCenterTypes() {
      try {
        const firstResponse = await axiosApi.get("/api/tipos_centros", {
          params: { por_pagina: 0 },
        });

        const response = await axiosApi.get("/api/tipos_centros", {
          params: { por_pagina: firstResponse.data.total },
        });

        this.types = response.data.datos;
      } catch (error) {
        this.types = [];
      }
    },
    async submit() {
    this.alert = false;
      let send_data = {
        nombre: this.name,
        direccion: this.address,
        telefono: this.phone,
        hora_apertura: this.opening_time,
        hora_cierre: this.closing_time,
        tipo: this.type,
        municipio: this.town,
        web_url: this.web,
        email: this.email,
        latitud: this.latitude,
        longitud: this.longitude,
      };

      if (this.marker != null) {
        send_data["latitud"] = this.marker.lat;
        send_data["longitud"] = this.marker.lng;
      }
      console.log(send_data);
      /*
      try {
        const response = await axiosApi.post("/api/centro", send_data);
        console.log(response.data);
      } catch (error) {
        console.log(`error: ${error}`);
      }
      */

      axios
        .post(`https://grupo20.proyecto2020.linti.unlp.edu.ar/api/centro`, send_data, {
          headers: {
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          console.log(response);
          this.$router.push({ name: "Home" });
        })
        .catch((error) => {
          this.alert = true;
          this.error.push(error);
        });
    },
  },
  created() {
    this.getTowns();
    this.getHelpCenterTypes();
  },
};
</script>