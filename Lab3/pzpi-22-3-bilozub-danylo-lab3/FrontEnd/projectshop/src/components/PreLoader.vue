<template>
    <div v-if="loading" class="preloader">
      <div class="preloader-overlay"></div> <!-- Прозорий фон -->
      <div class="preloader-text">ZooHelper</div> <!-- Текст без прозорості -->
    </div>
  </template>
  
  <script>
  export default {
    props: {
      loading: {
        type: Boolean,
        required: true
      }
    }
  };
  </script>
  
  <style scoped>
.preloader {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

/* Прозорий фон */
.preloader-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(163, 163, 163, 0.7); /* Білий фон з 80% прозорістю */
  z-index: 1;
}

/* Текст без прозорості */
.preloader-text {
  font-size: 6rem;
  font-weight: bold;
  color: rgb(2, 0, 0);
  z-index: 2;
  animation: pulse 1s infinite ease-in-out;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.1);
  }
}
</style>