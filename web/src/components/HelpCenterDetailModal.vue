<template>
    <div :id="id" class="modal fade text-left" role="dialog" tabindex="-1">
        <div class="modal-dialog modal-dialog-scrollable" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h4 class="modal-title">Información</h4>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">×</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <h6 class="mb-0">Nombre</h6>
                        <small class="ml-2">{{ helpCenter.nombre }}</small>
                    </div>
                    <div class="mb-3">
                        <h6 class="mb-0">Dirección</h6>
                        <small class="ml-2">{{ helpCenter.direccion }}</small>
                    </div>
                    <div class="mb-3">
                        <h6 class="mb-0">Telefono</h6>
                        <small class="ml-2">{{ helpCenter.telefono }}</small>
                    </div>
                    <div class="mb-3">
                        <h6 class="mb-0">Hora de apertura</h6>
                        <small class="ml-2">{{ helpCenter.hora_apertura }}</small>
                    </div>
                    <div class="mb-3">
                        <h6 class="mb-0">Hora de cierre</h6>
                        <small class="ml-2">{{ helpCenter.hora_cierre }}</small>
                    </div>
                    <div class="mb-3">
                        <h6 class="mb-0">Tipo de centro</h6>
                        <small class="ml-2">{{ helpCenter.tipo }}</small>
                    </div>
                    <div class="mb-3">
                        <h6 class="mb-0">Municipio</h6>
                        <small class="ml-2">{{ helpCenter.municipio }}</small>
                    </div>
                    <div class="mb-3" v-if="helpCenter.web">
                        <h6 class="mb-0">Sitio web</h6>
                        <small class="ml-2">{{ helpCenter.web }}</small>
                    </div>
                    <div class="mb-3" v-if="helpCenter.email">
                        <h6 class="mb-0">Correo electronico</h6>
                        <small class="ml-2">{{ helpCenter.email }}</small>
                    </div>
                    <div class="mb-3" v-if="helpCenter.protocolo">
                        <h6 class="mb-0">Protocolo de vista</h6>
                        <small class="ml-2">
                            <a :href="`http://localhost:5000/${helpCenter.protocolo}`">Protocolo</a>
                        </small>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "HelpCenterDetailModal",
    props: ["id", "helpCenter"]
}
</script>

<style>

</style>