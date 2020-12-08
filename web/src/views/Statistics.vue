<template>
    <div class="container-fluid" style="max-width: 1200px;">
        <h5 class="my-3">Estadísticas</h5>
        <div class="row">
            <div class="col-lg-7 col-xl-8">
                <div class="card shadow mb-4">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h6 class="text-primary font-weight-bold m-0">Cantidad de turnos solicitados esta semana</h6>
                    </div>
                    <div class="card-body">
                        <QuantityTurnsChar />
                    </div>
                </div>
            </div>
            <div class="col-lg-5 col-xl-4">
                <div class="card shadow mb-4">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h6 class="text-primary font-weight-bold m-0">Tipos de centros más solicitados</h6>
                    </div>
                    <div class="card-body">
                        <help-centers-types-chart />
                    </div>
                </div>
          </div>
        </div>
        <div class="row">
            <div class="col-lg-6 mb-4">
                <div class="card shadow mb-4">
                    <div class="card-header py-3">
                        <h6 class="text-primary font-weight-bold m-0">Centros con más turnos solicitados</h6>
                    </div>
                    <div class="card-body">
                        <turns-quantity-chart />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

import QuantityTurnsChar from "../components/QuantityTurnsChar.vue"
import HelpCentersTypesChart from '../components/HelpCentersTypesChart.vue';
import TurnsQuantityChart from '../components/TurnsQuantityChart.vue';

export default {
    name: "Statistics",
    components: {
        QuantityTurnsChar,
        HelpCentersTypesChart,
        TurnsQuantityChart
    }
};
</script>
