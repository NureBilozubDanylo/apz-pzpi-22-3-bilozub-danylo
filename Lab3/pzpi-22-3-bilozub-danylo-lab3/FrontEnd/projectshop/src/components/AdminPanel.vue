<template>
  <div class="admin-page">
    <div class="container">
      <h2>Admin panel</h2>

      <!-- резервна копія -->
      <section class="backup-block">
        <h3>Backup</h3>
        <button class="btn backup" :disabled="backupLoading" @click="createBackup">
          {{ backupLoading ? 'Creating…' : 'Create backup' }}
        </button>
        <span v-if="lastBackup" class="time">
          Last backup: {{ format(lastBackup) }}
        </span>
      </section>

      <!-- статистика -->
      <section class="stats-block" v-if="stats">
        <h3>Server stats</h3>
        <p>Uptime: {{ prettyUptime(stats.uptime_sec) }}</p>
        <p>CPU: {{ stats.cpu_percent }} %</p>
        <p>RAM: {{ stats.ram_used_mb }} / {{ stats.ram_total_mb }} MB</p>
        <p>Disk: {{ stats.disk_used_gb }} / {{ stats.disk_total_gb }} GB</p>
      </section>

      <hr />

      <!-- Список магазинів та працівників -->
      <div v-if="loading" class="loader">Loading…</div>
      <div v-for="shop in shops" :key="shop.shop_id" class="shop-block">
        <h3>{{ shop.name }} (id: {{ shop.shop_id }})</h3>

        <div v-if="workers[shop.shop_id]?.length">
          <table class="worker-table">
            <thead>
              <tr>
                <th>Name</th><th>Role</th><th>Email</th>
                <th>Phone</th><th>Age</th><th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="w in workers[shop.shop_id]" :key="w.user_id">
                <!-- edit mode -->
                <template v-if="editingId === w.user_id">
                  <td><input v-model="form.name" /></td>
                  <td>
                    <select v-model="form.role">
                      <option value="worker">worker</option>
                      <option value="director">director</option>
                    </select>
                  </td>
                  <td><input v-model="form.email" /></td>
                  <td><input v-model="form.mobile_number" /></td>
                  <td><input type="number" v-model.number="form.age" /></td>
                  <td>
                    <button class="btn save" @click="saveUser(w.user_id)">Save</button>
                    <button class="btn cancel" @click="editingId = null">Cancel</button>
                  </td>
                </template>
                <!-- view mode -->
                <template v-else>
                  <td>{{ w.username }}</td><td>{{ w.role }}</td>
                  <td>{{ w.email }}</td><td>{{ w.mobile_number }}</td>
                  <td>{{ w.age }}</td>
                  <td><button class="btn edit" @click="startEdit(w)">Edit</button></td>
                </template>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else>No workers in this shop</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount } from "vue";
import axios from "axios";

axios.defaults.baseURL = "http://127.0.0.1:8000";
axios.defaults.withCredentials = true;
axios.interceptors.request.use((cfg) => {
  const t = localStorage.getItem("token");
  if (t) cfg.headers.Authorization = `Bearer ${t}`;
  return cfg;
});

/* ---------------- state ---------------- */
const loading = ref(true);
const shops   = ref([]);
const workers = reactive({});
const stats   = ref(null);

const editingId = ref(null);
const form = reactive({ name:"", role:"", email:"", mobile_number:"", age:0 });

const backupLoading = ref(false);
const lastBackup    = ref(null);

let statsPoller;

/* -------------- fetch helpers -------------- */
async function fetchShops() {
  const username = localStorage.getItem("username");
  const { data } = await axios.get(`/shops/user/${username}/shops`);
  shops.value = data;
}
async function fetchWorkers(shopId) {
  const { data } = await axios.get(`/shops/${shopId}/workers`);
  workers[shopId] = data;
}
async function fetchStats() {
  try {
    const { data } = await axios.get("/admin/stats");
    stats.value = data;
  } catch(e){ console.error(e); }
}

/* -------------- backup -------------- */
async function createBackup() {
  backupLoading.value = true;
  try {
    const { data } = await axios.post("/admin/backup");
    lastBackup.value = data.timestamp;
    alert("Backup created successfully!");
  } catch (e) {
    console.error(e);
    alert("Backup failed!");
  } finally {
    backupLoading.value = false;
  }
}

/* -------------- edit flow -------------- */
function startEdit(w) {
  editingId.value = w.user_id;
  Object.assign(form, {
    name: w.username, role: w.role, email: w.email,
    mobile_number: w.mobile_number, age: w.age
  });
}
async function saveUser(userId) {
  try {
    await axios.put(`/users/${userId}`, {
      username: form.name, role: form.role, email: form.email,
      mobile_number: form.mobile_number, age: form.age,
    });
    const shopId = Object.keys(workers)
      .find(id => workers[id].some(u => u.user_id === userId));
    if (shopId) await fetchWorkers(shopId);
    editingId.value = null;
  } catch(e){ console.error(e); alert("Save failed"); }
}

/* -------------- life-cycle -------------- */
onMounted(async () => {
  await fetchShops();
  await Promise.all(shops.value.map(s => fetchWorkers(s.shop_id)));
  loading.value = false;
  await fetchStats();
  statsPoller = setInterval(fetchStats, 5000);
});
onBeforeUnmount(() => clearInterval(statsPoller));

/* -------------- utils -------------- */
function format(ts){
  return new Date(ts).toLocaleString();
}
function prettyUptime(sec){
  const h = Math.floor(sec/3600), m = Math.floor(sec%3600/60);
  return `${h}h ${m}m`;
}
</script>

<style scoped>
.container { max-width:1100px; margin:0 auto; padding:20px; }
h3 { margin-top:0; }

.backup-block, .stats-block { margin-bottom:24px; }
.time { margin-left:12px; font-style:italic; }

.shop-block { margin-bottom:40px; }
.worker-table { width:100%; border-collapse:collapse; }
.worker-table th, .worker-table td { border:1px solid #ccc; padding:6px 8px; }

.btn { padding:4px 10px; border:none; border-radius:6px; cursor:pointer; font-size:.85rem; }
.edit{ background:#1976d2; color:#fff; } .save{ background:#2e7d32; color:#fff; }
.cancel{ background:#c62828; color:#fff; margin-left:6px; }
.backup{ background:#795548; color:#fff; }

.loader{ margin:40px 0; }
</style>
