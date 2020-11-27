<template>
    <router-link :to="link" style="color: inherit; text-decoration: inherit;">
        <div class="card shadow-sm text-center h-100" style="max-width: 280px;">
            <i :class="icon" class="my-4" style="font-size: 60px;color: #3a6ba6;"></i>
            <div class="card-body">
                <h5 class="card-title" style="font-weight: bold">{{ title }}</h5>
                <p class="card-text">{{ description }}</p>
            </div>
        </div>
    </router-link>
</template>

<script>
export default {
    name: "SimpleCard",
    props: ["title", "description", "icon", "link"]
}
</script>

<style>

</style>