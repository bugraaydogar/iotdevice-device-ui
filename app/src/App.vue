<template>
  <div id="app">
    <app-header/>
    <div class="wrapper">
      <form class="tesla-car-container">
        <h1>{{ title }}</h1>
        <app-car :wheelsize="wheels" :speed="speed" />
        <div>
          <table>
            <tr>
              <td> <h3> Speed </h3> </td>
            </tr>
            <tr>
              <td>
                <div id="gauge-demo">
                  <div id="gauge-container">
                    <div class="center-section">
                      <DxCircularGauge :value="car_speed">
                        <DxSize :width="260"/>
                        <DxValueIndicator
                          :second-fraction="0.24"
                          type="twoColorNeedle"
                          color="none"
                          second-color="#f05b41"/>
                        <DxGeometry :start-angle="225" :end-angle="315" />
                        <DxScale :start-value="0" :end-value="180" :tick-interval="20" :minor-tick-interval="10" />
                      </DxCircularGauge>
                      <div class="speed-value">
                        <span>{{ car_speed }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </td>
            </tr>
          </table>
        </div>
      </form>
    </div>
  <div>
    <vue-final-modal v-model="showModal" classes="modal-container" content-class="modal-content">
      <span class="modal__title">Internal System Error Detected</span>
      <div class="modal__content">
        <p>Speed can not be more 100 km/h! Please wait while the software reverts to the last known good state</p>
      </div>
    </vue-final-modal>
  </div>

</div>

</template>

<script>
import AppHeader from "./components/AppHeader.vue"
import AppCar from './components/AppCar.vue';
import axios from "axios"
import DxSlider from 'devextreme-vue/slider';
import DxCircularGauge, {
  DxSize,
  DxValueIndicator,
  DxGeometry,
  DxScale,
} from 'devextreme-vue/circular-gauge';
import DxLinearGauge, {
  DxSize as DxLinearSize,
  DxValueIndicator as DxLinearValueIndicator,
  DxScale as DxLinearScale,
  DxMinorTick,
  DxLabel,
} from 'devextreme-vue/linear-gauge';


export default {
  name: 'App',
  components: {
    AppHeader,
    AppCar,
    DxSlider,

    DxCircularGauge,
    DxSize,
    DxValueIndicator,
    DxGeometry,
    DxScale,

    DxLinearGauge,
    DxLinearSize,
    DxLinearValueIndicator,
    DxLinearScale,
    DxMinorTick,
    DxLabel,

  },
  data() {
    return {
      title: "Ubuntu Core Over the Air Update",
      wheels: 19,
      max_allowed_speed: 100,
      current_max_speed: 0,
      speed: 55,
      polling_speed: null,
      car_speed: 0,
      polling_refresh: null,
      showModal: false,
    }
  },
  created () {
    this.loadData()
    this.pollSpeed()
    this.pollUpdate()
  },
  methods: {
    pollSpeed () {
      this.polling_speed = setInterval(() => {
        this.loadData()
      }, 500)
    },
    pollUpdate() {
      this.polling_refresh = setInterval(() => {
        this.refresh()
      }, 50000)

    },
    async loadData() {
      // console.log("Load Data is called")
      const res = await axios.get("http://localhost:3000/speed-level")
      // Use the battery value for the speed as well
      this.car_speed = res.data.speed
      this.current_max_speed = res.data.maxSpeed

      if(this.current_max_speed > this.max_allowed_speed) {
        this.showModal = true
        await this.revert()
        const res = await axios.get("http://localhost:3000/speed-level")
        this.car_speed = res.data.speed
        this.current_max_speed = res.data.maxSpeed
      }

      if (this.current_max_speed <= this.max_allowed_speed) {
        this.showModal = false
      }

    },
    async refresh() {
      const res = await axios.post("http://localhost:5000/refresh")
      console.log(JSON. stringify(res))
    },
    async revert() {
      const res = await axios.post("http://localhost:5000/revert", {"name": "iotdevice-device-controller"})
      console.log(JSON. stringify(res))
    }
  },
  beforeDestroy () {
    clearInterval(this.polling_speed)
    clearInterval(this.polling_refresh)

  }
}
</script>


<style lang="scss">
@import 'tesla-style.scss';
</style>

<style scoped>
:deep(.modal-container) {
  display: flex;
  justify-content: center;
  align-items: center;
}
:deep(.modal-content) {
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
