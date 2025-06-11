<template>
  <div class="wrapper">
    <Header></Header>
    <main class="main" :style = "main">
      <router-view></router-view>
    </main>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from "./components/Header.vue";
import Footer from "./components/Footer.vue";
export default {
  name: "App",
  components: {
    Header,
    Footer
  },
  data() {
    return {
      isAdmin: false,
      main: '',
    };
  },
};
</script>

<style>

.main{
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}
.wrapper{
    display: flex;
    height: 100vh;
    flex-direction: column;
}
body {
    margin: 0;
}
* {
    font-family: "Faculty Glyphic", sans-serif;
    font-weight: 400;
    font-style: normal;
  }
*,
*:before,
*:after {
  box-sizing: border-box;
}
input:focus{
    outline: none;
}
h1,h2,h3,h4,h5,h6,p{
    margin: 0;
    padding: 0;
}
.container{
    max-width: 1200px;
    margin: 0 auto;
}
.wrapper{
    display: flex;
    height: 100vh;
    flex-direction: column;
}
.main{
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}
a {
    text-decoration: none !important;
}
html, body {
    height: 100%;
    margin: 0;
    padding: 0;
  }
  #app {
    height: 100%;
  }

body {
    margin: 0;
}
</style>