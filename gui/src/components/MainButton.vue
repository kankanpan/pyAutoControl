<template>
<button type="button" @click="handleClick" class="mainButton">
  {{ text }}
</button>
</template>

<script>
export default {
  name: 'MainButton',
  props: {
    text: String,
    click: Function,
  },
  methods: {
    handleClick() {
      this.click()
    }
  }
}
</script>

<style scoped>
h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
