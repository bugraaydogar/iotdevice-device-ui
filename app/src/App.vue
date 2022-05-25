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
              <td><ve-progress :progress="battery" text-align="center"/></td>
            </tr>
          </table>
        </div>
      </form>
      
    </div>
  <div>
    <vue-final-modal v-model="showModal" classes="modal-container" content-class="modal-content">
      <span class="modal__title">Internal System Error Detected</span>
      <div class="modal__content">
        <p>Battery Level can not be more %100, Please wait while reverting to the last known good state</p>
      </div>
    </vue-final-modal>
  </div>
  </div>
</template>

<script>
import AppHeader from "./components/AppHeader.vue"
import AppCar from './components/AppCar.vue';
import axios from "axios"

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
      speed: 55,
      polling_battery: null,
      polling_refresh: null,
      battery: 0,
      showModal: false
    }
  },
  created () {
    this.loadData()
    this.pollBattery()
    this.pollUpdate()
  },
  methods: {
    pollBattery () {
      this.polling_battery = setInterval(() => {
        this.loadData()
      }, 50000)
    },
    pollUpdate() {
      this.polling_refresh = setInterval(() => {
        this.refresh()
      }, 50000)

    },
    async loadData() {
      console.log("Load Data is called")
      const res = await axios.get("http://localhost:3000/battery-level")
      this.battery = res.data.battery
      
      if(this.battery > 100) {
        showModal = true
        await this.revert()
        showModal = false
        const res = await axios.get("http://localhost:3000/battery-level")
        this.battery = res.data.battery
      }

    },
    async refresh() {
      console.log("refresh is called")
      const res = await axios.post("http://localhost:5000/refresh")
      console.log(JSON. stringify(res))
    },
    async revert() {
      console.log("Revert is called...")
      const payload = ['iotdevice-device-controller']
      const res = await axios.post("http://localhost:5000/revert", payload)
      console.log(JSON. stringify(res))
    }
  },
  beforeDestroy () {
    clearInterval(this.polling_battery)
    clearInterval(this.polling_refresh)

  }
}
</script>


<style lang="scss">
@import 'tesla-style.scss';
</style>

<style scoped>
::v-deep .modal-container {
  display: flex;
  justify-content: center;
  align-items: center;
}
::v-deep .modal-content {
  display: flex;
  flex-direction: column;
  margin: 0 1rem;
  padding: 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
  background: #fff;
}
.modal__title {
  font-size: 1.5rem;
  font-weight: 700;
}
</style>
