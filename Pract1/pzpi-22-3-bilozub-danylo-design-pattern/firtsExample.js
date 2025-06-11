// store.js
import Vuex from 'vuex';
import Vue from 'vue';

Vue.use(Vuex);

// Стан і логіка (суб’єкт)
const store = new Vuex.Store({
    state: {
        notes: [
            { id: 1, text: "Купити молоко", done: false },
            { id: 2, text: "Подзвонити другу", done: false }
        ]
    },
    mutations: {
        toggleNote(state, noteId) {
            const note = state.notes.find(n => n.id === noteId);
            if (note) {
                note.done = !note.done;
            }
        }
    },
    actions: {
        toggleNote({ commit }, noteId) {
            commit('toggleNote', noteId);
        }
    },
    getters: {
        allNotes: state => state.notes
    }
});

export default store;

// Notes.vue
<template>
  <div>
    <h1>Список нотаток</h1>
    <ul>
      <li v-for="note in notes" :key="note.id">
        <input
          type="checkbox"
          :checked="note.done"
          @change="toggleNote(note.id)"
        />
        <span :style="{ textDecoration: note.done ? 'line-through' : 'none' }">
          {{ note.text }}
        </span>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
    name: 'Notes',
    computed: {
        // Спостерігач: підписка на стан через геттер
        ...mapGetters(['allNotes']),
        notes() {
            return this.allNotes;
        }
    },
    methods: {
        // Виклик дії для оновлення стану
        ...mapActions(['toggleNote'])
        
    updated() {
        console.log('Компонент Notes оновився');
    }
};
</script>

// main.js
import Vue from 'vue';
import App from './App.vue';
import store from './store';

Vue.config.productionTip = false;

new Vue({
    store,
    render: h => h(App)
}).$mount('#app');

// App.vue
<template>
  <div id="app">
    <Notes />
  </div>
</template>

<script>
import Notes from './components/Notes.vue';

export default {
    name: 'App',
    components: {
        Notes
    }
};
</script>