<template>
  <div class="admin-page">
    <div class="container">
      <h2>Admin panel</h2>

      <!-- ░░░░░ 1. BACKUP ░░░░░ -->
      <section class="backup-block">
        <h3>Backup</h3>
        <button class="btn backup" :disabled="backupLoading" @click="createBackup">
          {{ backupLoading ? 'Creating…' : 'Create backup' }}
        </button>
        <input type="file" @change="restoreDb" accept=".sql,.dump,.gz" />
        <span v-if="lastBackup" class="time">
          Last backup: {{ format(lastBackup) }}
        </span>
      </section>

      <!-- ░░░░░ 2. SERVER STATS ░░░░░ -->
      <section class="stats-block" v-if="stats">
        <h3>Server stats</h3>
        <p>Uptime: {{ prettyUptime(stats.uptime_sec) }}</p>
        <p>CPU: {{ stats.cpu_percent }} %</p>
        <p>RAM: {{ stats.ram_used_mb }} / {{ stats.ram_total_mb }} MB</p>
        <p>Disk: {{ stats.disk_used_gb }} / {{ stats.disk_total_gb }} GB</p>
      </section>

      <!-- ░░░░░ 3. SYSTEM CONFIG ░░░░░ -->
      <section class="config-block" v-if="sysStatus">
        <h3>System config</h3>
        <div class="cfg-row" v-for="(val, key) in sysStatus.config" :key="key">
          <label>{{ key }}</label>
          <input
            v-model="configForm[key]"
            :type="typeof val === 'boolean' ? 'checkbox' : 'text'"
            :checked="typeof val === 'boolean' ? configForm[key] : null"
            @change="typeof val === 'boolean' ? configForm[key] = !configForm[key] : null"
          />
        </div>
        <button class="btn save" @click="saveConfig">Save config</button>
      </section>

      <!-- ░░░░░ 4. LOGS ░░░░░ -->
      <section class="logs-block">
        <h3>System logs</h3>
        <div class="logs-controls">
          <button class="btn" @click="fetchLogs">Load last 200 lines</button>
          <button class="btn cancel" @click="clearLogs">Clear logs</button>
        </div>
        <pre class="log-view" v-if="logs">{{ logs }}</pre>
      </section>

      <!-- ░░░░░ 5. DB STATUS ░░░░░ -->
      <section class="db-block">
        <h3>Database status</h3>
        <button class="btn" @click="fetchDbStatus">Refresh</button>
        <button class="btn save" @click="optimizeDb">Optimize (VACUUM)</button>

        <table v-if="dbStatus.length" class="db-table">
          <thead><tr><th>Table</th><th>Size, MB</th></tr></thead>
          <tbody>
            <tr v-for="t in dbStatus" :key="t.name">
              <td>{{ t.name }}</td>
              <td>{{ (t.size_bytes / 1024 / 1024).toFixed(2) }}</td>
            </tr>
          </tbody>
        </table>
      </section>

      <hr />

      <!-- ░░░░░ 6. SHOPS & WORKERS ░░░░░ -->
      <div v-if="loading" class="loader">Loading…</div>
      <div v-for="shop in shops" :key="shop.shop_id" class="shop-block">
        <h3>{{ shop.name }} (id: {{ shop.shop_id }})</h3>

        <div v-if="workers[shop.shop_id]?.length">
          <table class="worker-table">
            <thead><tr>
              <th>Name</th><th>Role</th><th>Email</th>
              <th>Phone</th><th>Age</th><th>Actions</th>
            </tr></thead>
            <tbody>
              <tr v-for="w in workers[shop.shop_id]" :key="w.user_id">
                <!-- edit -->
                <template v-if="editingId === w.user_id">
                  <td><input v-model="form.name" /></td>
                  <td>
                    <select v-model="form.role">
                      <option value="worker">worker</option>
                      <option value="director">director</option>
                      <option value="admin">admin</option>
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
                <!-- view -->
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
import { ref, reactive, onMounted, onBeforeUnmount } from "vue"
import axios from "axios"

axios.defaults.baseURL = "http://127.0.0.1:8000"
axios.defaults.withCredentials = true
axios.interceptors.request.use(cfg => {
  const t = localStorage.getItem("token")
  if (t) cfg.headers.Authorization = `Bearer ${t}`
  return cfg
})

/* ───────── state ───────── */
const loading = ref(true)
const shops   = ref([])
const workers = reactive({})
const stats        = ref(null)
const sysStatus    = ref(null)
const dbStatus     = ref([])
const logs         = ref("")

const editingId = ref(null)
const form = reactive({ name:"", role:"", email:"", mobile_number:"", age:0 })
const configForm = reactive({})

const backupLoading = ref(false)
const lastBackup    = ref(null)
let statsPoller

/* ───────── helpers ───────── */
async function fetchShops() {
  const username = localStorage.getItem("username")
  const { data } = await axios.get(`/shops/user/${username}/shops`)
  shops.value = data
}
async function fetchWorkers(id) {
  const { data } = await axios.get(`/shops/${id}/workers`)
  workers[id] = data
}
async function fetchStats() {
  stats.value = (await axios.get("/admin/stats")).data
}
async function fetchSysStatus() {
  const { data } = await axios.get("/admin/system/status")
  sysStatus.value = data
  Object.assign(configForm, data.config)
}
async function fetchLogs() {
  logs.value = (await axios.get("/admin/system/logs")).data.log
}
async function clearLogs() {
  await axios.delete("/admin/system/logs")
  logs.value = ""
}
async function fetchDbStatus() {
  dbStatus.value = (await axios.get("/admin/db/status")).data.tables
}
async function optimizeDb() {
  await axios.post("/admin/db/optimize")
  alert("DB optimized (vacuum)")
  fetchDbStatus()
}

/* ─── BACKUP ─── */
async function createBackup() {
  backupLoading.value = true
  try{
    const { data } = await axios.post("/admin/backup")
    lastBackup.value = data.timestamp
    alert("Backup OK")
  }catch(e){ alert("Backup failed"); console.error(e)}
  finally{ backupLoading.value = false }
}
async function restoreDb(e){
  if(!e.target.files.length) return
  const f = e.target.files[0]
  const fd = new FormData()
  fd.append("file", f)
  try{
    await axios.post("/admin/db/restore", fd)
    alert("Restore OK")
  }catch(err){ alert("Restore failed"); console.error(err)}
}

/* ─── CONFIG ─── */
async function saveConfig(){
  await axios.put("/admin/system/config", configForm)
  alert("Config updated")
}

/* ─── USERS ─── */
function startEdit(u){
  editingId.value = u.user_id
  Object.assign(form, {
    name:u.username, role:u.role, email:u.email,
    mobile_number:u.mobile_number, age:u.age
  })
}
async function saveUser(id){
  await axios.put(`/users/${id}`, {
    username: form.name, role: form.role, email: form.email,
    mobile_number: form.mobile_number, age: form.age,
  })
  const sid = Object.keys(workers).find(sid=>workers[sid].some(u=>u.user_id===id))
  if(sid) await fetchWorkers(sid)
  editingId.value=null
}

/* ─── life-cycle ─── */
onMounted(async ()=>{
  await fetchShops()
  await Promise.all(shops.value.map(s=>fetchWorkers(s.shop_id)))
  loading.value=false

  await fetchStats()
  await fetchSysStatus()
  await fetchDbStatus()
  statsPoller=setInterval(fetchStats,5000)
})
onBeforeUnmount(()=>clearInterval(statsPoller))

/* ─── utils ─── */
function format(ts){ return new Date(ts).toLocaleString() }
function prettyUptime(sec){
  const h=Math.floor(sec/3600), m=Math.floor(sec%3600/60)
  return `${h}h ${m}m`
}
</script>

<style scoped>
.container{max-width:1100px;margin:0 auto;padding:20px;}
h3{margin-top:0}

/* blocks */
.backup-block,.stats-block,.config-block,.logs-block,.db-block{margin-bottom:32px}

/* buttons */
.btn{padding:4px 10px;border:none;border-radius:6px;cursor:pointer;font-size:.85rem;}
.edit{background:#1976d2;color:#fff;} .save{background:#2e7d32;color:#fff;}
.cancel{background:#c62828;color:#fff;margin-left:6px;}
.backup{background:#795548;color:#fff;}

.logs-controls{display:flex;gap:8px;margin-bottom:6px;}
.log-view{background:#1e1e1e;color:#d6d6d6;padding:10px;border-radius:6px;max-height:300px;overflow:auto;font-size:12px;}

.db-table{width:100%;border-collapse:collapse;margin-top:8px;}
.db-table th,.db-table td{border:1px solid #ccc;padding:4px 8px;}

.cfg-row{display:flex;align-items:center;gap:12px;margin:6px 0;}
.cfg-row label{width:180px;font-weight:600}

.shop-block{margin-bottom:40px;}
.worker-table{width:100%;border-collapse:collapse;}
.worker-table th,.worker-table td{border:1px solid #ccc;padding:6px 8px;}

.loader{margin:40px 0;text-align:center;font-size:1.1rem;}
</style>
