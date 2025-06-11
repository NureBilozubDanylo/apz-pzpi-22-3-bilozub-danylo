<template>
    <div class="hist-page">
      <div class="container">
  
        <!-- Навігація -->
        <button class="btn" @click="router.go(-1)">⬅ Back to shop</button>
  
        <h2 class="title">Climate history</h2>
  
        <!-- Фільтри -->
        <div class="filters">
          <label>Type</label>
          <select v-model="type">
            <option value="temperature">Temperature</option>
            <option value="humidity">Humidity</option>
            <option value="light_intensity">Light</option>
          </select>
  
          <label>Mode</label>
          <select v-model="mode">
            <option value="day">Day</option>
            <option value="month">Month</option>
          </select>
  
          <div v-if="mode === 'day'">
            <label>Date</label>
            <input type="date" v-model="dateStr" />
          </div>
  
          <div v-else>
            <label>Month</label>
            <select v-model.number="month">
              <option v-for="m in 12" :key="m" :value="m">{{ m }}</option>
            </select>
  
            <label>Year</label>
            <input type="number" v-model.number="year" min="2000" style="width: 5rem" />
          </div>
  
          <button class="btn" @click="fetchHistory">Load</button>
        </div>
  
        <!-- Графік -->
        <div v-if="chartData.labels.length" class="chart-wrapper">
          <Line :data="chartData" :options="chartOpts" />
        </div>
        <p v-else>No data for selected period</p>
  
        <!-- Таблиця -->
        <div v-if="history.length" class="table-wrapper">
            <table class="history-table">
                <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>{{ typeLabel }}</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="h in history" :key="h.record_date">
                    <td>{{ formatDateTime(h.record_date) }}</td>
                    <td>{{ h[type] }}</td>
                </tr>
                </tbody>
            </table>
        </div>
  
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, watch, onMounted } from "vue";
  import axios from "axios";
  import { Line } from "vue-chartjs";
  axios.defaults.baseURL = "http://127.0.0.1:8000";
axios.interceptors.request.use((c) => {
  const t = localStorage.getItem("token");
  if (t) c.headers.Authorization = `Bearer ${t}`;
  return c;
});
  import {
    Chart,
    LineElement,
    PointElement,
    CategoryScale,
    LinearScale,
    Tooltip,
    Legend,
  } from "chart.js";
  import { useRoute, useRouter } from "vue-router";
  Chart.register(
    LineElement,
    PointElement,
    CategoryScale,
    LinearScale,
    Tooltip,
    Legend
  );
  
  // ---- державні змінні ----
  const route  = useRoute();
  const router = useRouter();
  const shop_id = Number(route.params.id);
  const type = ref("temperature");
  const mode = ref("day");
  
  const today = new Date().toISOString().slice(0, 10);
  const dateStr = ref(today);
  
  const month = ref(new Date().getMonth() + 1);
  const year = ref(new Date().getFullYear());
  
  const history = ref([]);
  
  // ---- запит даних ----
  async function fetchHistory() {
    try {
      let url = "";
      if (mode.value === "day") {
        url = `/climate_history/shop/${shop_id}/daily?date=${dateStr.value}`;
      } else {
        url = `/climate_history/shop/${shop_id}/monthly?month=${month.value}&year=${year.value}`;
      }
      const { data } = await axios.get(url);
      history.value = data;
    } catch (e) {
      console.error(e);
      history.value = [];
    }
  }
  
  // ---- реактивні побічні ефекти ----
  watch([type, mode], fetchHistory);
  onMounted(fetchHistory);
  
  // ---- дані для графіка ----
  const chartData = computed(() => {
    const labels = history.value.map((h) =>
      mode.value === "day"
        ? new Date(h.record_date).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
        : new Date(h.record_date).getDate()
    );
    const values = history.value.map((h) => h[type.value]);
  
    return {
      labels,
      datasets: [
        {
          label: typeLabel.value,
          data: values,
          tension: 0.3,
          fill: false,
          borderWidth: 2,
        },
      ],
    };
  });
  
  const typeLabel = computed(() =>
    type.value === "temperature"
      ? "Temperature (°C)"
      : type.value === "humidity"
      ? "Humidity (%)"
      : "Light (lx)"
  );
  
  const chartOpts = {
    responsive: true,
    plugins: { legend: { display: false } },
  };
  
  // ---- утиліти ----
  function formatDateTime(dt) {
    return new Date(dt).toLocaleString();
  }
  </script>
  
  <style scoped>
  .table-wrapper {
  max-height: 400px;   /* підберіть потрібну висоту */
  overflow-y: auto;
  border: 1px solid #ccc;  /* аби було видно рамку */
}
  .container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
  }
  .btn {
    background: #1976d2;
    color: #fff;
    border: none;
    border-radius: 6px;
    padding: 6px 14px;
    cursor: pointer;
  }
  .btn:hover {
    filter: brightness(1.08);
  }
  .title {
    margin: 10px 0 20px;
  }
  .filters {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    align-items: center;
    margin-bottom: 20px;
  }
  .filters label {
    margin-right: 4px;
  }
  .chart-wrapper {
    max-width: 100%;
    margin-bottom: 24px;
  }
  .history-table {
    width: 100%;
    border-collapse: collapse;
  }
  .history-table th,
  .history-table td {
    padding: 6px 10px;
    border: 1px solid #ccc;
    text-align: left;
  }
  </style>
  