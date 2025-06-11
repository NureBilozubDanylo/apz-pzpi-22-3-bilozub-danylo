<template>
    <!-- напівпрозоре тло -->
    <div class="overlay" @click.self="$emit('close')">
      <!-- модальне вікно -->
      <div class="modal">
        <h3>Notifications</h3>
  
        <!-- скролюваний список -->
        <div class="list-wrapper">
          <div
            class="notify"
            v-for="n in notifications"
            :key="n.notification_id"
          >
            <span class="time">{{ format(n.timestamp) }}</span>
            <p class="msg">{{ n.message }}</p>
          </div>
        </div>
  
        <button class="btn close" @click="$emit('close')">Close</button>
      </div>
  
      <!-- toast про нові повідомлення -->
      <transition name="fade">
        <div v-if="showToast" class="toast" @click="showToast = false">
          📬&nbsp; New notifications!
        </div>
      </transition>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onBeforeUnmount } from "vue";
  import axios from "axios";
  
  /* ───────── axios ───────── */
  axios.defaults.baseURL = "http://127.0.0.1:8000";
  axios.interceptors.request.use((cfg) => {
    const t = localStorage.getItem("token");
    if (t) cfg.headers.Authorization = `Bearer ${t}`;
    return cfg;
  });
  
  /* ───────── змінні ───────── */
  
  const notifications = ref([]);
  const showToast = ref(false);
  
  let prevCount = 0;
  let poller;
  let toastTimer;
  
  /* ───────── запит даних ───────── */
  async function fetchNotifications() {
    if (!localStorage.getItem("user_id")) return;
    try {
        const { data } = await axios.get(`/notifications/user/${localStorage.getItem("user_id")}`);
      // нові спочатку
      data.sort(
        (a, b) => new Date(b.timestamp) - new Date(a.timestamp)
      );
      /* якщо кількість виросла → показати toast */
      if (data.length > prevCount) {
        showToast.value = true;
        clearTimeout(toastTimer);
        toastTimer = setTimeout(() => (showToast.value = false), 4000);
      }
      prevCount = data.length;
      notifications.value = data;
    } catch (err) {
      console.error(err);
    }
  }
  
  /* ───────── життєвий цикл ───────── */
  onMounted(() => {
    fetchNotifications();
    poller = setInterval(fetchNotifications, 5000);
  });
  onBeforeUnmount(() => clearInterval(poller));
  
  /* ───────── utils ───────── */
  function format(ts) {
    return new Date(ts).toLocaleString();
  }
  </script>
  
  <style scoped>
  /* overlay */
  .overlay {
    position: fixed;
    inset: 0;
    background: rgba(0 0 0 / 0.45);
    display: grid;
    place-items: center;
    z-index: 30;
  }
  
  /* modal */
  .modal {
    background: #fff;
    width: min(90%, 480px);
    max-height: 80vh;
    overflow: hidden;
    padding: 24px 28px;
    border-radius: 14px;
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  h3 {
    margin: 0 0 4px;
  }
  
  /* список */
  .list-wrapper {
    flex: 1;
    overflow-y: auto;
    border: 1px solid #ddd;
    padding: 8px;
    border-radius: 8px;
  }
  .notify {
    border-bottom: 1px dashed #ccc;
    padding: 6px 0 8px;
  }
  .notify:last-child {
    border-bottom: none;
  }
  .time {
    font-size: 0.8rem;
    color: #666;
  }
  .msg {
    margin: 2px 0 0;
  }
  
  /* кнопка */
  .btn.close {
    align-self: flex-end;
    background: #1976d2;
    color: #fff;
    border: none;
    padding: 6px 14px;
    border-radius: 6px;
    cursor: pointer;
  }
  .btn.close:hover {
    filter: brightness(1.08);
  }
  
  /* toast */
  .toast {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    max-width: 400px;
    width: calc(100% - 40px);
    background: #1976d2;
    color: #fff;
    padding: 16px 24px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgb(0 0 0 / 0.2);
    text-align: center;
    font-size: 1.05rem;
  }
  
  /* плавна поява/зникнення toast */
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.25s;
  }
  .fade-enter-from,
  .fade-leave-to {
    opacity: 0;
  }
  </style>
  