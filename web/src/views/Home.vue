<template>
  <div class="home">
    <div class="container py-4">
        <div class="text-center py-2">
            <h2 class="text-dark mb-4">Donaciones Covid-19</h2>
            <div class="d-flex justify-content-center">
                <p class="text-secondary" style="max-width: 480px;">Esta página esta destinada a ayudar brindando información sobre los distintos centros de ayuda distribuidos en la ciudad de la Plata</p>
            </div>
        </div>
        <div class="row">
            <div class="col-md-4 d-flex justify-content-center mb-3">
                <simple-card
                    title="Buscar Centro"
                    description="Buscar en un mapa los centros de ayuda disponibles"
                    icon="fas fa-map-marked-alt"
                    link="#"
                />
            </div>
            <div class="col-md-4 d-flex justify-content-center mb-3">
                <simple-card
                    title="Solicitar Turno"
                    description="Solicitar un turno de atención para uno de los centros de ayuda disponibles"
                    icon="far fa-address-card"
                    link="#"
                />
            </div>
            <div class="col-md-4 d-flex justify-content-center mb-3">
                <simple-card
                    title="Solicitar Centro"
                    description="Solicitar la creación de un nuevo centro de ayuda"
                    icon="fas fa-plus-circle"
                    link="#"
                />
            </div>
        </div>
    </div>
  </div>
</template>

<script>
import SimpleCard from '@/components/SimpleCard.vue'

export default {
    name: 'Home',
    components: {
        SimpleCard
    }
}
</script>
