<template>
  <div id="app" style="min-height: 100%">
    <div style="margin-bottom: 100px">
      <navbar />
      <router-view />
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
