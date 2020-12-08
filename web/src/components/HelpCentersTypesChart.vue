
<script>
import { Doughnut, mixins } from 'vue-chartjs'
const { reactiveData } = mixins

const axios = require('axios');
        
const axiosApi = axios.create({
    baseURL: "http://localhost:5000",
});

export default {
    name: "HelpCentersTypesChart",
    extends: Doughnut,
    mixins: [reactiveData],
    methods: {
        async fetchHelpCentersTypes() {
            
            try {

                const firstResponse = await axiosApi.get("/api/tipos_centros", {
                    params: { por_pagina: 0 },
                });

                const response = await axiosApi.get("/api/tipos_centros", {
                    params: { por_pagina: firstResponse.data.total },
                });

                this.chartData = {
                    labels: [],
                    datasets: [
                        {
                            data: [],
                            backgroundColor: []
                        }
                    ]
                }

                response.data.datos.forEach((each) => {
                    this.chartData.labels.push(each.nombre);
                    this.chartData.datasets[0].data.push(each.cantidad_centros);
                    this.chartData.datasets[0].backgroundColor.push(this.randomColor());
                });
            
            } catch (error) {

                this.chartData = null;

            }            
            
        },
        randomColor() {
            return '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6)
        }
    },
    created() {
        this.fetchHelpCentersTypes();
    },
    mounted () {
        this.renderChart(this.chartData, this.options)
    }
}
</script>
