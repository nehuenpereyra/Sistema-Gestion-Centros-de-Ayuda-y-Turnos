<template>
   <div class="container text-center flex-row justify-content-center align-content-center">
                <div v-if="alert" class="alert alert-danger alert-dismissible fade show mt-2" role="alert">
                    Hubo un <strong>error</strong> en la solicitud del turno
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <h4 class="text-left mt-4">Solicitar turno para el centro x</h4>
                <div class="text-left">Los campos con (*) son obligatorios.</div>
                <div class="shadow-sm mt-3 p-3">
                    <form class="text-left user" method="post" @submit.prevent="postTurn" >
                        <div class="form-group row">
                            <div class="col-sm-6 mb-3 mb-sm-0"><label>Email*</label><input class="form-control" type="email" placeholder="email" name="email" required v-model="email"></div>
                            <div class="col-sm-6"><label>Telefono donante</label><input class="form-control" type="tel" placeholder="telefono donante" name="phone_donant" v-model="telephone"></div>
                        </div>
                        <div class="form-group"><label>Fecha del turno a solicitar*</label><input required class="form-control" type="date" v-model="date_request" v-bind:min="new Date().toISOString().substring(0, 10)"></div>
                        <div class="form-group"><label>Horario del turno a solicitar*</label>
                            <select class="form-control" v-model="selected" required>
                                <option disabled value="">Seleccione un horario disponible</option>
                                <option v-for="item in turns" :key="item.index" v-bind:value="{ time_init: item.horario_inicio, time_end: item.horario_fin}" > Horario: {{item.horario_inicio}} </option>
                            </select>
                        </div>
                        <button class="btn btn-primary btn-block text-white" type="submit">Solicitar</button></form>
                </div>
            </div>
</template>

<script>

const axios = require('axios');

export default {
  name: "Reservation",
  data() {
    return{
          email:"",
          telephone: "",
          date_request: new Date().toISOString().substring(0, 10),
          selected: '',
          turns: [],
          alert: false
    };
  },
  created(){
        this.fetchTurns();
  },
  methods: {
    fetchTurns(){
        axios.get(`http://127.0.0.1:5000/centros/${this.$route.params.center_id}/turnos_disponibles/?fecha=${this.changeFormat()}`).then((response) => {
            let index = 0
            response.data.turnos.forEach(
                (item)=>{ 
                        item.index = index;                 
                        this.turns.push(item);
                        index++
                }
            );
        }).catch((e) => {
            console.log("Error")
            console.log(e)
        })            
    },
    postTurn(){

        let send_data = {
            centro_id: Number(this.$route.params.center_id),
            email_donante: this.email,
            hora_inicio: this.selected.time_init,
            hora_fin: this.selected.time_end,
            fecha: this.date_request
        }

        if (this.telephone != "")
            send_data["telefono_donante"] = this.telephone;

        axios.post(`http://127.0.0.1:5000/centros/${this.$route.params.center_id}/reserva`, send_data, {
        headers: {
            'Content-Type': 'application/json',
        }})
        .then((response)=>{
            console.log(response);
        })
        .catch((error)=>{
            this.alert = true;
            console.log(error);
            this.error.push(error);
        });
            
    },
    changeFormat(){
        let fields = this.date_request.split('-');
        return `${fields[2]}-${fields[1]}-${fields[0]}`
    }
  },
  watch: {
    date_request: function () {
        this.turns = []
      this.fetchTurns();
    }
  },
};
</script>