
<script>
import { Bar, mixins } from 'vue-chartjs'
const { reactiveData } = mixins

const axios = require('axios');
        
const axiosApi = axios.create({
    baseURL: "https://admin-grupo20.proyecto2020.linti.unlp.edu.ar",
});

export default {
    name: "TurnsQuantityChart",
    extends: Bar,
    mixins: [reactiveData],
    data() {
        return {
            options: {
                legend: {
                    display: false
                },
                scales: {
                    yAxes: [
                        {
                            ticks: {
                                stepSize: 1
                            }
                        }
                    ],
                }
            }
        }
    },
    methods: {
        async fetchQuantityTurnsPerHelpCenter() {
            try {

                const response = await axiosApi.get("/api/centros/mas_turnos");

                this.chartData = {
                    labels: [],
                    datasets: [
                        {
                            data: [],
                            backgroundColor: []
                        }
                    ]
                }

                response.data.centros.forEach((each) => {
                    this.chartData.labels.push(each.nombre);
                    this.chartData.datasets[0].data.push(each.cantidad_turnos);
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
        this.fetchQuantityTurnsPerHelpCenter();
    },
    mounted () {
        this.renderChart(this.chartData, this.options)
    }
}
</script>
