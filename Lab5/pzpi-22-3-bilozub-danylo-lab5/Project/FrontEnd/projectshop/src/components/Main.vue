<template>
  <div class="page">
    <!-- Hero Section -->
    <section class="hero">
      <div class="overlay"></div>
      <div class="hero-content">
        <h2>
          Керуйте зоомагазином <br class="desktop-break" /> легко та зручно
        </h2>
        <p>
          Продажі, залишки, заробітна плата та бронювання улюбленців —
          ваш бізнес під контролем за кілька кліків.
        </p>
        <div class="hero-buttons">
          <a href="#features" class="btn btn-primary">Дізнатись більше</a>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features">
      <div class="container">
        <h3 class="section-title">Можливості для кожного</h3>
        <div class="cards">
          <div class="card">
            <h4 class="card-title">Адміністратору</h4>
            <ul>
              <li>Управління магазинами та працівниками</li>
              <li>Облік продажів і товарних залишків</li>
              <li>Автоматичні звіти та аналітика</li>
            </ul>
          </div>
          <div class="card">
            <h4 class="card-title">Працівнику</h4>
            <ul>
              <li>Швидке проведення продажів</li>
              <li>Доступ до графіка та зарплати</li>
              <li>Оновлення залишків у реальному часі</li>
            </ul>
          </div>
          <div class="card">
            <h4 class="card-title">Користувачу</h4>
            <ul>
              <li>Каталог тварин та товарів онлайн</li>
              <li>Бронювання улюбленців</li>
              <li>Актуальна інформація про наявність</li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>

export default {
  name:'MainC',
  data() {
      return {
      };
    },
  methods: {
      
    },
};
</script>
<style scoped>
:root {
  --primary: #ffb300;
  --bg-dark: #000;
  --text-light: #fff;
}

/* Global reset & helpers */
.page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  margin: 0;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

a {
  color: inherit;
  text-decoration: none;
  transition: color 0.2s ease;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* Navbar */
.navbar {
  background: var(--bg-dark);
  color: var(--text-light);
}

.nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
}

.logo {
  font-size: 1.5rem;
  font-weight: 700;
}

.nav-links {
  display: none;
  gap: 2rem;
}

.nav-links a:hover {
  color: var(--primary);
}

.menu-toggle {
  background: none;
  border: none;
  color: var(--text-light);
  display: block;
}

.menu-toggle .icon {
  width: 1.5rem;
  height: 1.5rem;
}

/* Show nav links on medium screens */
@media (min-width: 768px) {
  .nav-links {
    display: flex;
  }
  .menu-toggle {
    display: none;
  }
}

/* Hero */
.hero {
  position: relative;
  background-image: url('https://images.unsplash.com/photo-1558944351-d5f76c6b8cd7?auto=format&fit=crop&w=1740&q=80');
  background-size: cover;
  background-position: center;
  flex: 1;
}

.overlay {
  position: absolute;
  inset: 0;
  background: rgba(212, 212, 212, 0.5);
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: var(--text-light);
  padding: 8rem 1.5rem;
  max-width: 800px;
  margin: 0 auto;
}

.hero-content h2 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.desktop-break {
  display: none;
}

@media (min-width: 768px) {
  .hero-content h2 {
    font-size: 3.5rem;
  }
  .desktop-break {
    display: inline;
  }
}

.hero-content p {
  font-size: 1.125rem;
  margin-bottom: 2rem;
}

.hero-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
}

@media (min-width: 768px) {
  .hero-buttons {
    flex-direction: row;
    justify-content: center;
  }
}

/* Buttons */
.btn {
  padding: 0.75rem 2rem;
  border-radius: 9999px;
  font-weight: 600;
  cursor: pointer;
  display: inline-block;
}

.btn-primary {
  background: var(--primary);
  color: #000 !important;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.btn-primary:hover {
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.4);
}

.btn-outline {
  background: transparent;
  border: 2px solid var(--text-light);
  color: var(--text-light);
}

.btn-outline:hover {
  background: var(--text-light);
  color: #000;
}

/* Features */
.features {
  background: #fff;
  padding: 5rem 1.5rem;
}

.section-title {
  text-align: center;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 3rem;
}

.cards {
  display: grid;
  gap: 2rem;
}

@media (min-width: 768px) {
  .cards {
    grid-template-columns: repeat(3, 1fr);
  }
}

.card {
  background: #f3f3f3;
  border-radius: 1.5rem;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.card ul {
  list-style: disc;
  padding-left: 1rem;
  margin: 0;
  color: #4a4a4a;
}

/* Footer */
.footer {
  background: var(--bg-dark);
  color: var(--text-light);
}

.footer-inner {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 0;
}

@media (min-width: 768px) {
  .footer-inner {
    flex-direction: row;
  }
}

.footer nav {
  display: flex;
  gap: 1.5rem;
}

.footer nav a:hover {
  color: var(--primary);
}

.play-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--text-light);
  border-radius: 9999px;
  padding: 0.5rem;
  transition: background 0.2s, color 0.2s;
}

.play-btn:hover {
  background: var(--text-light);
  color: #000;
}

.icon {
  width: 1.25rem;
  height: 1.25rem;
}







.question-block{
    position: relative;
  }
  .faq-container {
    width: 100%;
    padding: 30px 100px 50px 100px !important;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 30px;
    align-items: center;
    justify-content: center;
  }
  
  .faq-title {
    width: 100%;
    text-align: center;
    margin-bottom: 20px;
    font-size: 2em;
    color: rgb(0, 0, 0);
  }
  
  .faq-item {
    width: 100%;
  }
  
  .faq-question {
    width: 100%;
    padding: 15px;
    text-align: left;
    background-color: #000000;
    color: white;
    font-size: 1.1em;
    border: none;
    cursor: pointer;
    border-radius: 5px;
    transition: background-color 0.3s;
  }
  
  .question-block:hover .svgstr{
    color: #000000;
  }
  .question-block:hover .faq-question{
    background-color: #ffc965;
    color: #000000;
  }
  
  .faq-answer {
    padding: 10px;
    width: 100%;
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    border-top: none;
    border-radius: 0 0 5px 5px;
  }
  
  .faq-answer p {
    margin: 0;
  }
  .svgstr{
    position: absolute;
    top: 40%;
    right: 10px;
    color: #fff;
    cursor: pointer;
  }
  .head{
    display: flex;
    justify-content: center;
    padding: 40px 0;
    
  }
  .head-wrapper{
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 30px 30px;
    border-radius: 30px;
    background-color: #000;
    color: #fff;
  }
  .head-logo{
    font-size: 50px;
    text-align: center;
    margin-bottom: 5px;
  }
  .head-sloggan{
    text-align: center;
    font-weight: 300;
    font-style: italic;
    margin-bottom: 25px;
  }
  .head-btn-wrapper{
    display: flex;
    justify-content: center;
  }
  .head-btn{
    padding: 10px 15px;
    border-radius: 15px;
    border: none;
    cursor: pointer;
    width: 40%;
  }
  .head-btn:hover {
    box-shadow: 0px 5px 10px rgba(211, 176, 22, 0.5);
    color: #967418;
    animation: shadow-pulse 1s infinite;
  }
  .about{
    background-color: #000;
    padding: 40px 0;
  }
  .about-wrapper{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 30px;
  }
  .about-text{
    width: 48%;
    color: #fff;
    padding: 0px 15px;
  }
  .about-img-wrapper{
    width: 48%;
  }
  .about-img{
    width: 100%;
    border: 1px solid black;
    border-radius: 10px;
  }
  .about-text-head{
    font-size: 40px;
    margin-bottom: 15px;
  }

  .feature-slider {
    max-width: 800px;
    margin: auto;
  }
  .feature-content {
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .mySwiper {
    padding: 20px;
  }
  .features-wrapper{
    padding: 50px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .features-head{
    text-align: center;
    font-size: 30px;
    padding-bottom: 10px;
    border-bottom: 1px solid #000;
    width: 30%;
    margin-bottom: 20px;
  }
  .features-img-block{
    width: 300px;
    height: 300px;
    overflow: hidden;
    border-radius: 100%;
    border: 1px solid black;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .features-img-block img{
    object-position: center;
    width: 80%;
    height: 80%;
    overflow: hidden;
    border-radius: 100%;
  }
  .feature-content h3{
    padding: 15px;
  }

  .head{
    z-index: 9999;
    background-color: #fff;
  }
  @media (max-width: 1296px) {
    .about-wrapper{
      flex-direction: column;
      text-align: center;
      gap: 30px
    }
    .about-text{
      width: 100%;
    }
    .about-img-wrapper{
      width: 90%;
    }
    .feature-slider{
      width: 90%;
    }
    .features-img-block{
      width: 200px;
      height: 200px;
    }
  }
  @media (max-width: 768px) {
    .lending-page{
      padding-top: 50px;
    }
    .faq-container{
      padding: 15px !important;
    }
    .faq-answer{
      text-align: center;
    }
    .features-img-block{
      width: 200px;
      height: 200px;
    }
  }
  @media (max-width: 480px) {
    .features-head{
      width: 50%;
    }
  }
</style>