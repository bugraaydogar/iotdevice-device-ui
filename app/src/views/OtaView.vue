<template>
  <app-header />
  <div style="display: flex">
    <!-- Left side table -->
    <div style="flex: 1">
      <table style="width: 100%; border-collapse: collapse; margin-top: 300px">
        <tr style="font-weight: bold; font-size: 24px">
          <td>Metadata</td>
        </tr>
        <tr style="font-weight: bold; font-size: 20px">
          <td>API Version: {{ api_version }}</td>
        </tr>
        <tr style="font-weight: bold; font-size: 20px">
          <td>iotdevice-device-controller: {{ controller }}</td>
        </tr>
        <tr style="font-weight: bold; font-size: 20px">
          <td>iotdevice-device-ui: {{ ui }}</td>
        </tr>
        <tr style="font-weight: bold; font-size: 24px; margin-top: 10px">
          <td>Validation Sets</td>
        </tr>

        <tr style="font-weight: bold; font-size: 24px; margin-top: 10px">
          <td>
            <button @click="enforce('1')">
              Enforce Validation Sequence: 1
            </button>
          </td>
        </tr>
        <tr style="font-weight: bold; font-size: 24px; margin-top: 10px">
          <td>
            <button @click="enforce('2')">
              Enforce Validation Sequence: 2
            </button>
          </td>
        </tr>

        <tr style="font-weight: bold; font-size: 24px; margin-top: 10px">
          <td>
            <button @click="forget()">Remove Validation Set</button>
          </td>
        </tr>
      </table>
    </div>

    <!-- Right side content -->
    <div style="flex: 2">
      <h1>Ubuntu Core Over the Air Update</h1>
      <div class="progress">
        <h1>Battery Level</h1>
        <ve-progress :progress="battery_level" />
      </div>
    </div>

    <!-- Modal -->
    <div style="flex: 1">
      <vue-final-modal
        v-model="showModal"
        classes="modal-container"
        content-class="modal-content"
      >
        <span class="modal__title">Internal System Error Detected</span>
        <div class="modal__content">
          <p>
            Battery Level cannot be more than 100%! Please wait while the
            software reverts to the last known good state.
          </p>
        </div>
      </vue-final-modal>
    </div>
  </div>
</template>

<script>
import AppHeader from '../components/AppHeader.vue';
import axios from 'axios';
import { VueEllipseProgress } from 'vue-ellipse-progress';

export default {
  name: 'Ota',
  components: {
    AppHeader,
    VueEllipseProgress,
  },
  data() {
    return {
      api_version: null,
      controller: null,
      ui: null,
      max_allowed_battery_level: 100,
      polling_battery_level: null,
      battery_level: 0,
      polling_refresh: null,
      showModal: false,
      baseURL : window.location.href.split(':')[0]
    };
  },
  created() {

    console.log(this.baseURL);
    this.loadData();
    this.pollBattery();
    this.pollUpdate();
  },
  methods: {
    enforce(seq) {
      var url = baseURL + ":4500/enforce";
      axios.post(url, { name: seq });
    },
    forget() {
      axios.post('http://localhost:4500/forget');
    },
    pollBattery() {
      this.polling_battery_level = setInterval(() => {
        this.loadData();
      }, 1000);
    },
    pollUpdate() {
      this.polling_refresh = setInterval(() => {
        this.refresh();
      }, 45000);
    },
    async loadData() {
      const res = await axios.get('http://localhost:4040/v1/batterylevel');
      this.battery_level = res.data.level;
      if (this.battery_level > this.max_allowed_battery_level) {
        this.showModal = true;
        await this.revert();
        const res = await axios.get('http://localhost:4040/batterylevel');
        this.battery_level = res.data.level;
      }

      if (this.battery_level <= this.max_allowed_battery_level) {
        this.showModal = false;
      }

      const api_version = await axios.get('http://localhost:4040/version');
      this.api_version = api_version.data.version;

      const snaps = await axios.get('http://localhost:4500/list');
      snaps.data.result.forEach((entry) => {
        if (entry.name === 'iotdevice-device-controller') {
          this.controller = entry.revision;
        }
      });

      snaps.data.result.forEach((entry) => {
        if (entry.name === 'iotdevice-device-ui') {
          this.ui = entry.revision;
        }
      });
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
h1 {
  font-family: 'RobotoNormal';
  font-weight: 100;
  font-size: 38px;
  text-align: center;
  letter-spacing: 3px;
  padding-top: 3px;
}

.progress {
  margin: auto;
  width: 50%;
  padding: 10px;
  text-align: center;
}

body {
  background: white;
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
