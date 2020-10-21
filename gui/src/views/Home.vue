<template>
<div class="home">
  <MainButton :click="testClick" text="Welcome to Your Vue.js App" />
</div>
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
