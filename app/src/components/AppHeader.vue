<template>
  <header class="header">
    <img :src="logo">
  </header>
</template>


<script>
import logo from './../assets/logo.png';

export default {
  name: 'AppHeader',
  data() {
    return {
      logo
    }
  }
}
</script>

<style>

</style>