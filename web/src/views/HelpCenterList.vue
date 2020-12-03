<template>
    <div class="HelpCenterList">
        <div class="container my-4">
            <h5 class="mt-3">Centros de Ayuda</h5>

            <div v-if="helpCenters == null">
                Buscando centros de ayuda...
            </div>
            <div v-else-if="helpCenters.length == 0">
                No se encontraron centros de ayuda.
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

                <div class="d-flex justify-content-center justify-content-sm-end mt-3">
                    <sliding-pagination
                        :current="page.current"
                        :total="page.total"
                        @page-change="onChangePage"
                        :slidingEndingSize="1"
                        :classMap="{
                        'list': 'pagination',
                        'element': 'page-item',
                        'elementDisabled': 'disabled',
                        'elementActive': 'active',
                        'page': 'page-link'
                        }" />
                </div>
                
                <help-center-detail-modal
                    id="helpCenterDetailModal"
                    :helpCenter="currentHelpCenter"/>                
            </div>
        </div>
    </div>
</template>

<script>
import SlidingPagination from 'vue-sliding-pagination'
import HelpCenterDetailModal from '../components/HelpCenterDetailModal.vue';

const axios = require('axios');
        
const axiosApi = axios.create({
    baseURL: "https://grupo20.proyecto2020.linti.unlp.edu.ar",
    headers: { "Content-Type": "application/json" }
});

export default {
    components: { 
        SlidingPagination,
        HelpCenterDetailModal
    },
    name: "HelpCenterList",
    data() {
        return {
            page: {
                current: 1,
                total: null
            },
            helpCenters: null,
            currentHelpCenter: {}
        }
    },
    methods: {
        onChangePage(selectedPage) {
            this.page.current = selectedPage;
            this.getHelpCenters();
        },
        async getHelpCenters() {

            this.helpCenters = null;

            try {

                const response = await axiosApi.get("/api/centros", {
                    params: {
                        pagina: this.page.current
                    }
                });

                this.helpCenters = response.data.centros;
                this.page = {
                    current: response.data.pagina,
                    total: Math.ceil(response.data.total / response.data.por_pagina)
                };

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
    created() {
        this.getHelpCenters();
    }
}
</script>

<style>
    
</style>