//store.js
import { reactive } from 'vue';

// Суб’єкт — об’єкт стану зоомагазину
const petStore = reactive({
    products: [
        { id: "cat123", name: "Кіт Мурзик", inStock: 5 },
        { id: "dog456", name: "Собака Рекс", inStock: 3 }
    ],
    observers: [], // Спостерігачі для зовнішньої логіки (необов’язково у Vue, але для прикладу)

    addObserver(observer) {
        this.observers.push(observer);
    },

    removeObserver(observer) {
        this.observers = this.observers.filter(obs => obs !== observer);
    },

    notify(data) {
        this.observers.forEach(observer => observer.update(data));
    },

    updateStock(productId, newStock) {
        const product = this.products.find(p => p.id === productId);
        if (product) {
            product.inStock = newStock;
            this.notify({ productId, newStock }); // Додаткове сповіщення для не-Vue спостерігачів
        }
    }
});

export default petStore;

// observers.js
export class WarehouseObserver {
    update(data) {
        console.log(`Склад: Оновлено наявність товару ${data.productId} - ${data.newStock} одиниць`);
    }
}

// App.vue
<template>
  <div>
    <h1>Наявність товарів у зоомагазині</h1>
    <ul>
      <li v-for="product in petStore.products" :key="product.id">
        {{ product.name }} - Наявність: {{ product.inStock }}
      </li>
    </ul>
    <button @click="updateStock('cat123', 4)">Оновити наявність Мурзика</button>
  </div>
</template>

<script>
import petStore from './store';
import { WarehouseObserver } from './observers';

export default {
  name: 'App',
  setup() {
    const warehouse = new WarehouseObserver();
    petStore.addObserver(warehouse);

    const updateStock = (productId, newStock) => {
      petStore.updateStock(productId, newStock);
    };

    return {
      petStore,
      updateStock
    };
  }
};
</script>

// main.js
import { createApp } from 'vue';
import App from './App.vue';

const app = createApp(App);
app.mount('#app');