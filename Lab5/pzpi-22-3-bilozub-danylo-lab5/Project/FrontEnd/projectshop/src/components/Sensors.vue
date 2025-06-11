<template>
  <div class="shop-prof">
    <div class="container">

      <button class="btn back-btn" @click="goBack">Back to shop</button>

      <!-- add sensor -->
      <div class="add-sensor">
        <button class="btn add-btn" @click="showForm = true">Add sensor</button>
      </div>

      <!-- modal -->
      <div v-if="showForm" class="modal" @click.self="showForm = false">
        <form class="modal-body" @submit.prevent="createSensor">
          <h3>Create new sensor</h3>

          <label>Type</label>
          <select v-model="form.type">
            <option value="humidity">Humidity</option>
            <option value="light">Light</option>
            <option value="temperature">Temperature</option>
          </select>

          <label>Sensor link</label>
          <input type="text" v-model="form.sensor_link" required />

          <label>Location</label>
          <input type="text" v-model="form.location" required />

          <label>Initial value</label>
          <input type="number" v-model.number="form.current_value" required />

          <label>Last maintenance</label>
          <input type="date" v-model="form.last_maintenance" required />

          <div class="actions">
            <button type="submit" class="btn">Save</button>
            <button type="button" class="btn cancel" @click="showForm = false">
              Cancel
            </button>
          </div>
        </form>
      </div>

      <!-- sensors list -->
      <h3 v-if="sensors.length" class="title">
        Sensors ({{ sensors.length }})
      </h3>

      <div v-if="sensors.length" class="sensors-grid">
        <div
          class="sensor-card"
          v-for="sensor in sensors"
          :key="sensor.sensor_id"
        >
          <img
            :src="getIcon(sensor.type)"
            class="sensor-icon"
            :alt="sensor.type"
          />
          <div class="info">
            <h4 class="sensor-type">
              {{ capitalize(sensor.type) }}
            </h4>
            <p class="location">{{ sensor.location }}</p>
            <p class="value">Value: {{ sensor.current_value }}</p>
            <p class="date">
              Last maintenance: {{ formatDate(sensor.last_maintenance) }}
            </p>
            <a
              class="link"
              :href="sensor.sensor_link"
              target="_blank"
              rel="noopener noreferrer"
            >
              {{ sensor.sensor_link }}
            </a>
          </div>
        </div>
      </div>

      <p v-else>No sensors yet.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
axios.defaults.baseURL = "http://127.0.0.1:8000";
axios.defaults.withCredentials = true;
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default {
  name: "SensorsC",
  data() {
    return {
      sensors: [],
      showForm: false,
      form: {
        type: "temperature",
        sensor_link: "",
        location: "",
        current_value: 0,
        last_maintenance: "",
      },
      /** карта тип → asset-шлях */
      iconMap: {
        humidity: require("@/assets/humidity.png"),
        light: require("@/assets/light.png"),
        temperature: require("@/assets/temperature.jpg"),
      },
    };
  },
  created() {
    this.shop_id = this.$route.params.id;
    this.fetchSensors();
  },
  mounted() {
    // авто-обновление каждые 5 с
    this.poller = setInterval(this.fetchSensors, 5000);
  },
  beforeUnmount() {
    clearInterval(this.poller);
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    formatDate(d) {
      return new Date(d).toLocaleDateString();
    },
    capitalize(txt) {
      return txt.charAt(0).toUpperCase() + txt.slice(1);
    },
    getIcon(type) {
      return this.iconMap[type] || this.iconMap.temperature;
    },
    async fetchSensors() {
      try {
        const { data } = await axios.get(
          `/sensor/shop/${this.shop_id}/sensors`
        );
        this.sensors = data;
      } catch (e) {
        console.error(e);
      }
    },
    async createSensor() {
      try {
        const payload = { ...this.form, shop_id: Number(this.shop_id) };
        await axios.post(`/sensor/`, payload);
        this.showForm = false;
        this.resetForm();
        this.fetchSensors();
      } catch (e) {
        console.error(e);
        alert("Failed to create sensor");
      }
    },
    resetForm() {
      this.form = {
        type: "temperature",
        sensor_link: "",
        location: "",
        current_value: 0,
        last_maintenance: "",
      };
    },
  },
};
</script>

<style scoped>
/* layout */
.shop-prof .container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 20px;
}

/* buttons */
.btn {
  padding: 8px 16px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
  transition: 0.2s;
  background: #1976d2;
  color: #fff;
}
.btn:hover {
  filter: brightness(1.1);
}
.back-btn {
  background: #6c757d;
}
.add-btn {
  background: #2e7d32;
}
.cancel {
  background: #c62828;
}

/* grid of sensors */
.sensors-grid {
  margin-top: 30px;
  display: grid;
  gap: 24px;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
}
.back-btn {
  background: #6c757d;
  margin-bottom: 15px;
}

.sensor-card {
  background: #ffffff;
  padding: 18px;
  border-radius: 16px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  display: flex;
  gap: 14px;
  transition: transform 0.15s;
}
.sensor-card:hover {
  transform: translateY(-4px);
}

/* icon */
.sensor-icon {
  width: 48px;
  height: 48px;
}

/* inner info */
.info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.sensor-type {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}
.location {
  font-style: italic;
}
.value,
.date {
  font-size: 0.9rem;
}
.link {
  font-size: 0.88rem;
  color: #1976d2;
  word-break: break-all;
}

/* modal */
.modal {
  position: fixed;
  background: rgba(0 0 0 / 0.45);
  display: grid;
  place-items: center;
  z-index: 10;
  width: 100%;
  height: 100%;
}
.modal-body {
  background: #fff;
  width: min(90%, 420px);
  padding: 28px 32px;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.modal-body h3 {
  margin: 0 0 6px;
  text-align: center;
}
.modal-body input,
.modal-body select {
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
.actions {
  margin-top: 6px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
