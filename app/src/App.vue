<template>
  <div id="app">
    <app-header />
    <div>
      <progress-bar :options="options" :value="value" />
    </div>
    <div>
      <vue-final-modal
        v-model="showModal"
        classes="modal-container"
        content-class="modal-content"
      >
        <span class="modal__title">Internal System Error Detected</span>
        <div class="modal__content">
          <p>
            Speed can not be more 100 km/h! Please wait while the software
            reverts to the last known good state
          </p>
        </div>
      </vue-final-modal>
    </div>
    <div>
      <vue-final-modal
        v-model="showModal2"
        classes="modal-container"
        content-class="modal-content"
      >
        <span class="modal__title">Too fast!</span>
        <div class="modal__content">
          <p>
            Automated speed control tried to reach {{ car_speed }} which
            violates the limit of {{ current_max_speed }}. Reverting to
            {{ last_correct_speed }}
          </p>
        </div>
      </vue-final-modal>
    </div>
  </div>
</template>
i
<script>
import AppHeader from './components/AppHeader.vue';
import axios from 'axios';

export default {
  name: 'App',
  components: {
    AppHeader,
  },
  data() {
    return {
      title: 'Ubuntu Core Over the Air Update',
      wheels: 19,
      max_allowed_speed: 100,
      current_max_speed: 0,
      speed: 55,
      polling_speed: null,
      car_speed: 0,
      polling_refresh: null,
      showModal: false,
    };
  },
  created() {
    this.loadData();
    this.pollSpeed();
    this.pollUpdate();
  },
  methods: {
    pollSpeed() {
      this.polling_speed = setInterval(() => {
        this.loadData();
      }, 1000);
    },
    pollUpdate() {
      this.polling_refresh = setInterval(() => {
        this.refresh();
      }, 45000);
    },
    async loadData() {
      // console.log("Load Data is called")
      const res = await axios.get('http://localhost:4040/speed-level');
      // Use the battery value for the speed as well
      this.car_speed = res.data.speed;
      this.current_max_speed = res.data.maxSpeed;
      if (this.current_max_speed > this.max_allowed_speed) {
        this.showModal = true;
        await this.revert();
        const res = await axios.get('http://localhost:4040/speed-level');
        this.car_speed = res.data.speed;
        this.current_max_speed = res.data.maxSpeed;
      }

      if (this.car_speed > this.current_max_speed) {
        this.showModal2 = true;
        setTimeout(function () {
          this.showModal2 = false;
          this.car_speed = this.last_correct_speed;
        }, 1000);
      } else {
        this.last_correct_speed = this.car_speed;
        this.showModal2 = false;
      }

      if (this.current_max_speed <= this.max_allowed_speed) {
        this.showModal = false;
      }
    },
    async refresh() {
      const res = await axios.post('http://localhost:4500/refresh');
      console.log(JSON.stringify(res));
    },
    async revert() {
      const res = await axios.post('http://localhost:4500/revert', {
        name: 'iotdevice-device-controller',
      });
      console.log(JSON.stringify(res));
    },
  },
  beforeDestroy() {
    clearInterval(this.polling_speed);
    clearInterval(this.polling_refresh);
  },
};
</script>

<style lang="scss">
.header {
  padding: 12px 0;
  text-align: center;
  background: #222;
  img {
    width: 157px;
    height: 50px;
  }
}
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
