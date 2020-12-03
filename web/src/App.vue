<template>
  <div>
    <div style="height: 100%;">
      <navbar />
      <div
        class="container clear-top"
        style="overflow: auto; padding-bottom: 150px"
      >
        <router-view />
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";

export default {
  name: "App",
  components: {
    Navbar,
    Footer,
  },
};
</script>
