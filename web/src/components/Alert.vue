<template>
    <div :class="alertTypeClass" class="alert alert-dismissible fade show mt-2" role="alert">
        {{ message }}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    </div>
</template>

<script>
export default {
    name: "Alert",
    props: ["type", "message"],
    computed: {
        alertTypeClass() {
            return `alert-${this.type}`
        }
    }
}
</script>

<style>

</style>