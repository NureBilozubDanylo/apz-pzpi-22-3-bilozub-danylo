<template>
  <div class="shop-prof">
    <!-- modal форма створення тварини -->
    <div v-if="showForm" class="modal" @click.self="showForm = false">
      <form class="modal-body" @submit.prevent="createAnimal">
        <h3>Create new animal</h3>

        <!-- BASIC INFO -->
        <label>Name</label>
        <input v-model="form.name" required />

        <label>Species</label>
        <input v-model="form.species" required />

        <label>Breed</label>
        <input v-model="form.breed" />

        <div class="grid-2">
          <div>
            <label>Age</label>
            <input type="number" v-model.number="form.age" min="0" />
          </div>
          <div>
            <label>Sex</label>
            <select v-model="form.sex">
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
          </div>
        </div>

        <label>Weight (kg)</label>
        <input type="number" step="0.1" v-model.number="form.weight" />

        <!-- HEALTH -->
        <label>Health info</label>
        <textarea v-model="form.health_info" rows="2" />

        <div class="grid-3">
          <div>
            <label>Temperature</label>
            <input type="number" step="0.1" v-model.number="form.temperature" />
          </div>
          <div>
            <label>Humidity</label>
            <input type="number" step="0.1" v-model.number="form.humidity" />
          </div>
          <div>
            <label>Light</label>
            <input type="number" step="0.1" v-model.number="form.light_intensity" />
          </div>
        </div>

        <!-- FEEDING -->
        <label>Feeding time</label>
        <input v-model="form.feeding_time" placeholder="e.g. 09:00, 18:00" />

        <div class="grid-2">
          <div>
            <label>Food (name)</label>
            <input v-model="form.food_name" />
          </div>
          <div>
            <label>Food weight (g)</label>
            <input type="number" v-model.number="form.food_weight" />
          </div>
        </div>

        <div class="actions">
          <button type="submit" class="btn">Save</button>
          <button type="button" class="btn cancel" @click="showForm = false">
            Cancel
          </button>
        </div>
      </form>
    </div>

    <div class="container">
      <button class="btn back-btn" @click="goBack">Back to shop</button>

      <!-- додати тварину -->
      <div class="add-animal">
        <button class="btn add-btn" @click="showForm = true">Add animal</button>
      </div>

      <!-- CLIMATE SETTINGS -->
      <div v-if="climate" class="climate-box">
        <h3>Climate settings</h3>
        <p>🌡 Temperature: <strong>{{ climate.temperature }} °C</strong></p>
        <p>💧 Humidity: <strong>{{ climate.humidity }} %</strong></p>
        <p>💡 Light: <strong>{{ climate.light_intensity }} lx</strong></p>
      </div>

      <!-- список тварин -->
      <h3 v-if="animals.length" class="title">Animals ({{ animals.length }})</h3>

      <div v-if="animals.length" class="animals-grid">
        <div class="animal-card" v-for="a in animals" :key="a.animal_id">
          <img :src="getImg(a.species)" class="animal-img" :alt="a.species" />
          <div class="info">
            <h4 class="name">{{ a.name }}</h4>
            <p class="spec">{{ capitalize(a.species) }} — {{ a.breed || '—' }}</p>
            <p class="basic">
              Age: {{ a.age ?? 'n/a' }} &nbsp;|&nbsp;
              Sex: {{ a.sex }} &nbsp;|&nbsp;
              Weight: {{ a.weight ?? 'n/a' }} kg
            </p>
            <p class="env">
              🌡 {{ a.temperature ?? '—' }} °C &nbsp;
              💧 {{ a.humidity ?? '—' }} % &nbsp;
              💡 {{ a.light_intensity ?? '—' }} lx
            </p>
            <p class="feed">
              Feeding: {{ a.feeding_time || '—' }}
              <span v-if="a.food_name">
                — {{ a.food_name }} ({{ a.food_weight }} g)
              </span>
            </p>
            <p class="health">{{ a.health_info }}</p>
          </div>
        </div>
      </div>

      <p v-else>No animals yet.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
axios.defaults.baseURL = "http://127.0.0.1:8000";
axios.interceptors.request.use((c) => {
  const t = localStorage.getItem("token");
  if (t) c.headers.Authorization = `Bearer ${t}`;
  return c;
});

export default {
  name: "AnimalsC",
  data() {
    return {
      animals: [],
      climate: null, // ← climate settings
      showForm: false,
      form: {
        name: "",
        species: "",
        breed: "",
        age: null,
        sex: "male",
        weight: null,
        health_info: "",
        temperature: null,
        humidity: null,
        light_intensity: null,
        feeding_time: "",
        food_weight: null,
        food_name: "",
      },
      imgMap: {
        default: require("@/assets/defaultAnimal.jpg"),
      },
    };
  },
  created() {
    this.shop_id = this.$route.params.id;
    this.fetchAnimals();
    this.fetchClimateSettings(); // ← initial fetch
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    capitalize(t) {
      return t ? t.charAt(0).toUpperCase() + t.slice(1) : "";
    },
    getImg(species) {
      const key = species?.toLowerCase();
      return this.imgMap[key] || this.imgMap.default;
    },
    async fetchAnimals() {
      try {
        const { data } = await axios.get(
          `/animals/shop/${this.shop_id}/animals`
        );
        this.animals = data;
      } catch (e) {
        console.error(e);
      }
    },
    async fetchClimateSettings() {
      try {
        const { data } = await axios.get(`/climate_settings/shop/${this.shop_id}`);
        this.climate = data;
      } catch (e) {
        console.error("Climate settings fetch error:", e);
        this.climate = null;
      }
    },
    async createAnimal() {
      try {
        const payload = { ...this.form, shop_id: Number(this.shop_id) };
        await axios.post("/animals/", payload);
        this.showForm = false;
        this.resetForm();
        this.fetchAnimals();
        this.fetchClimateSettings(); // ← refresh after creation
      } catch (e) {
        console.error(e);
        alert("Failed to create animal");
      }
    },
    resetForm() {
      Object.assign(this.form, {
        name: "",
        species: "",
        breed: "",
        age: null,
        sex: "male",
        weight: null,
        health_info: "",
        temperature: null,
        humidity: null,
        light_intensity: null,
        feeding_time: "",
        food_weight: null,
        food_name: "",
      });
    },
  },
};
</script>

<style scoped>
/* layout */
.shop-prof .container {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}
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
  filter: brightness(1.08);
}
.back-btn {
  background: #6c757d;
  margin-bottom: 15px;
}
.add-btn {
  background: #2e7d32;
}
.cancel {
  background: #c62828;
}

/* climate block */
.climate-box {
  margin: 20px 0;
  padding: 16px;
  background: #f3f6fb;
  border-radius: 12px;
  border-left: 4px solid #1976d2;
}
.climate-box h3 {
  margin-top: 0;
  margin-bottom: 6px;
}

.animals-grid {
  height: 400px;
  overflow-y: scroll;
  margin-top: 28px;
  display: grid;
  gap: 24px;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}
.animal-card {
  background: #fff;
  padding: 18px;
  border-radius: 16px;
  display: flex;
  gap: 16px;
  box-shadow: 0 4px 10px rgb(0 0 0 / 0.07);
  transition: transform 0.15s;
}
.animal-card:hover {
  transform: translateY(-4px);
}
.animal-img {
  width: 60px;
  height: 60px;
  object-fit: contain;
}
.info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.name {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
}
.spec {
  font-style: italic;
}
.basic,
.env,
.feed {
  font-size: 0.9rem;
}
.health {
  font-size: 0.88rem;
  color: #555;
}

/* modal */
.modal {
  position: absolute;
  background: rgba(0 0 0 / 0.45);
  display: grid;
  place-items: center;
  z-index: 10;
  width: 100%;
  height: 100%;
  padding: 50px 0;
}
.modal-body {
  background: #fff;
  width: min(90%, 480px);
  max-height: 90vh;
  overflow-y: auto;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 100px 32px;
}
.modal-body h3 {
  margin: 0 0 8px;
  text-align: center;
}
.modal-body input,
.modal-body textarea,
.modal-body select {
  width: 100%;
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
}
.grid-2,
.grid-3 {
  display: grid;
  gap: 12px;
}
.grid-2 {
  grid-template-columns: repeat(2, 1fr);
}
.grid-3 {
  grid-template-columns: repeat(3, 1fr);
}
.actions {
  margin-top: 6px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
