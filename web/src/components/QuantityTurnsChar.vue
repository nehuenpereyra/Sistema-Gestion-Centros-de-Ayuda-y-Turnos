<script>
import { Line } from "vue-chartjs";
const axios = require("axios");

export default {
  extends: Line,
  mounted() {
    this.getData();
  },
  methods: {
    async getData() {
      try {
        const response = await axios.get(
          "https://admin-grupo20.proyecto2020.linti.unlp.edu.ar/api/cantidad_turnos/"
        );
        console.log("Aca");
        console.log();
        let days = [];
        let quantity = [];
        response.data.forEach((data) => {
          days.push(data.fecha);
          quantity.push(data.cantidad);
        });
        this.renderChart(
          {
            labels: days,
            datasets: [
              {
                data: quantity,
                backgroundColor: "transparent",
                borderColor: "rgba(1, 116, 188, 0.50)",
                pointBackgroundColor: "rgba(171, 71, 188, 1)",
              },
            ],
          },
          {
            legend: {
              display: false,
            },
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              yAxes: [
                {
                  ticks: {
                    stepSize: 1,
                  },
                },
              ],
            },
          }
        );
      } catch (error) {
        console.log(error);
      }
    },
  },
};
</script>