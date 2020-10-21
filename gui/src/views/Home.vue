<template>
<main class="home">
  <MainButton :click="testClick" text="Check" />
  <MainButton :click="testClick" text="Action" />
  <MainButton :click="testClick" text="Stop" />
</main>
</template>

<script>
// @ is an alias to /src
import MainButton from '@/components/MainButton.vue'
//import http from "../axios";

export default {
  name: 'Home',
  components: {
    MainButton
  },
  methods: {
    testClick: () => {
      console.log("test");
    }
  }
}
</script>

<style scoped>
</style>
