<template>
    <div class="HelpCenterList">
        <div class="container my-4">
            <h5 class="mt-3">Centros de Ayuda</h5>

            <div v-if="helpCenters == null">
                Buscando centros de ayuda...
            </div>
            <div v-else>
                <ul class="list-group border rounded shadow-sm mt-3">
                    <li v-for="helpCenter of helpCenters" :key="helpCenter.id" class="list-group-item">
                        <div class="row d-flex">
                            <div class="col-12 d-flex justify-content-center justify-content-sm-start col-sm mb-2 mb-sm-0">
                                <div class="text-center text-sm-left">
                                    <span class="d-block">{{ helpCenter.nombre }}</span>
                                    <small>{{ helpCenter.tipo }}<br></small>
                                    <small>{{ helpCenter.municipio }}<br></small>
                                    <small>{{ helpCenter.hora_apertura }}hs - {{ helpCenter.hora_cierre }}hs<br></small>
                                </div>
                            </div>
                            <div class="col-12 col-sm-auto d-flex justify-content-center align-items-center">
                                <router-link :to="urlForCenter(helpCenter)" class="btn btn-primary btn-sm mr-1">
                                    <i class="far fa-address-book"></i>
                                </router-link>
                                <button type="button" @click="setCurrentHelpCenter(helpCenter)" class="btn btn-primary btn-sm" data-toggle="modal" data-target="#helpCenterDetailModal">
                                    <i class="fas fa-eye"></i>
                                </button>
                            </div>
                        </div>
                    </li>
                </ul>
                <nav class="d-flex justify-content-center justify-content-sm-end mt-3">
                    <ul class="pagination">
                        <li class="page-item"><a class="page-link" href="#" aria-label="Previous"><span aria-hidden="true">«</span></a></li>
                        <li class="page-item"><a class="page-link" href="#">1</a></li>
                        <li class="page-item"><a class="page-link" href="#">2</a></li>
                        <li class="page-item"><a class="page-link" href="#">3</a></li>
                        <li class="page-item"><a class="page-link" href="#">4</a></li>
                        <li class="page-item"><a class="page-link" href="#" aria-label="Next"><span aria-hidden="true">»</span></a></li>
                    </ul>
                </nav>
                <help-center-detail-modal
                    id="helpCenterDetailModal"
                    :helpCenter="currentHelpCenter"/>
            </div>
        </div>
    </div>
</template>

<script>
import HelpCenterDetailModal from '../components/HelpCenterDetailModal.vue';

const axios = require('axios');
        
const axiosApi = axios.create({
    baseURL: "http://localhost:5000",
    headers: { "Content-Type": "application/json" }
});

export default {
    components: { HelpCenterDetailModal },
    name: "HelpCenterList",
    data() {
        return {
            helpCenters: null,
            currentHelpCenter: {}
        }
    },
    methods: {
        async getHelpCenters() {
            
            try {

                const response = await axiosApi.get("/api/centros");

                this.helpCenters = response.data.centros;

            } catch (error) {
                
                this.helpCenters = []

            }

        },
        urlForCenter(helpCenter) {
            return `/centros/${helpCenter.id}/reserva`
        },
        setCurrentHelpCenter(helpCenter) {
            this.currentHelpCenter = helpCenter;
        }
    },
    computed: {
        previousPage() {
            return {
                name: this.$route.name
            }
        }
    },
    created() {
        this.getHelpCenters();
        console.log(`pagina: ${this.$route.query.pagina}`);
    }
}
</script>

<style>

</style>