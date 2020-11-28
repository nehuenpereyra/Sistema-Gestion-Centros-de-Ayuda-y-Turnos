<template>
    <div class="container my-4" style="/*overflow: auto;*//*padding-bottom: 150px;*//*background: white;*/">
        <h5 class="mt-3">Solicitar Centro</h5>
        <div class="border rounded shadow-sm mt-3 p-3" style="background: white;">
            <form method="post" @submit.prevent="submit">
                <div class="form-row">
                    <div class="col">
                        <div class="form-group">
                            <label for="name_input">Nombre*</label>
                            <input class="form-control" type="text" id="name_input" name="name" v-model="name" required>
                        </div>
                    </div>
                </div>
                <div class="form-row">
                    <div class="col-12 col-sm-6">
                        <div class="form-group">
                            <label for="address_input">Dirección*</label>
                            <input class="form-control" type="text" id="address_input" name="address" v-model="address" required>
                        </div>
                    </div>
                    <div class="col-12 col-sm-6">
                        <div class="form-group">
                            <label for="phone_input">Teléfono*</label>
                            <input class="form-control" type="tel" id="phone_input" name="phone" v-model="phone" required>
                        </div>
                    </div>
                </div>
                <div class="form-row">
                    <div class="col-12 col-sm-6">
                        <div class="form-group">
                            <label for="opening_time_input">Hora de Apertura*</label>
                            <input class="form-control" id="opening_time_input" type="time" name="opening_time" v-model="opening_time" required>
                        </div>
                    </div>
                    <div class="col-12 col-sm-6">
                        <div class="form-group">
                            <label for="closing_time_input">Hora de Cierre*</label>
                            <input class="form-control" id="closing_time_input" type="time" name="closing_time" v-model="closing_time" required>
                        </div>
                    </div>
                </div>
                <div class="form-row">
                    <div class="col">
                        <div class="form-group">
                            <label for="type_input">Tipo de Centro*</label>
                            <select class="form-control" id="type_input" name="type" v-model="type" required>
                                <option value="" disabled="">Por favor, seleccione uno</option>
                                <option value="1">Centro de Alimentos</option>
                                <option value="2">Centro de Ropa</option>
                                <option value="3">Centro de Sangre</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div class="form-row">
                    <div class="col">
                        <div class="form-group">
                            <label for="town_input">Municipio*</label>
                            <select class="form-control" id="town_input" name="town" v-model="town" required>
                                <option value="" disabled="">Por favor, seleccione uno</option>
                                <option value="1">Almirante Brown</option>
                                <option value="2">Avellaneda</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div class="form-row">
                    <div class="col">
                        <div class="form-group">
                            <label for="web_input">Sitio Web</label>
                            <input class="form-control" type="url" id="web_input" name="web" v-model="web">
                        </div>
                    </div>
                </div>
                <div class="form-row">
                    <div class="col">
                        <div class="form-group">
                            <label for="email_input">Correo Electrónico</label>
                            <input class="form-control" type="email" id="email_input" name="email" v-model="email">
                        </div>
                    </div>
                </div>
                <div class="d-flex justify-content-center justify-content-sm-end">
                    <button class="btn btn-primary mt-3" type="submit">Enviar Solicitud</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
export default {
    name: "HelpCenterRequest",
    data() {
        return {
            name: "Centro la Galleta",
            address: "Av 60 e80 y 81",
            phone: "+54 2944 106080",
            opening_time: "09:00",
            closing_time: "16:00",
            type: "1",
            town: "2",
            web: "",
            email: ""
        }
    },
    methods: {
        submit() {
            console.log(this.$data);
        }
    }
}
</script>