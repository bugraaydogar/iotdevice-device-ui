<template>
  <header class="header">
    <img :src="logo" />
  </header>
</template>

<script>
import logo from './../assets/logo.png';

export default {
  name: 'AppHeader',
  data() {
    return {
      logo,
    };
  },
};
</script>

<style lang="scss">
.header {
  padding: 12px 0;
  text-align: center;
  background: #222;
  img {
    width: 200px;
    height: 50px;
  }
}
</style>
