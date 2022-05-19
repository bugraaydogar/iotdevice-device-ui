<template>
  <div id="app">
    <app-header/>
    <div class="wrapper">
      <form class="tesla-battery">
        <h1>{{ title }}</h1>
        <app-car :wheelsize="wheels" :speed="speed" />
        <div>
          <table>
            <tr>
              <td> <h3> Battery </h3> </td>
            </tr>
            <tr>
              <td><ve-progress :progress="50" text-align="center"/></td>
            </tr>
          </table>
        </div>
      </form>
      
    </div>
  </div>
</template>

<script>
import AppHeader from "./components/AppHeader.vue"
import AppCar from './components/AppCar.vue';



export default {
  name: 'App',
  components: {
    AppHeader,
    AppCar,
  },
  data() {
    return {
      title: "Ubuntu Core Over the Air Update",
      wheels: 19,
      speed: 55
    }
  }
}
</script>


<style lang="scss">
@import 'tesla-style.scss';
</style>
