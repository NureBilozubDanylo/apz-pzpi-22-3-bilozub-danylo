<template>
  <div class="login">
    <PreLoader :loading = "load"></PreLoader>
    <div class="container">
      <div :class="{'login-wrapper':true,'light':this.$store.getters.getTheme}">
        <h2 :class="{'login-head':true,'light1':this.$store.getters.getTheme}">Account Log in</h2>
        <input
          type="text"
          :class="{'login-input':true,'input-light':this.$store.getters.getTheme}"
          v-model="username"
          placeholder="Username"
        />
        <div class="password-block">
          <input
            :type="showPassword ? 'text' : 'password'" 
            class="login-input"
            :class="{'login-input':true,'input-light':this.$store.getters.getTheme}"
            v-model="password"
            placeholder="Password"
          />
          <label class="password-check" :class="{'black-color':this.$store.getters.getTheme}">
            <input type="checkbox" class = "check" v-model="showPassword" />
            Show password
          </label>
        </div>
        
        <div class="login-btn">
          <button class="login-btn-button" :class="{'light-btn':this.$store.getters.getTheme}" @click="tryLogin">Log in</button>
        </div>
      
        <div class="login-other">
          <p :class="{'login-other-f':true,'black-color':this.$store.getters.getTheme}">Forgot passwod?</p>
          <router-link :to="{ name: 'register' }">
            <p class="login-other-f" :class="{'black-color':this.$store.getters.getTheme}">Register Now</p>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import PreLoader from "./PreLoader.vue";

export default {
  name: "LoginC",
  components: {
    PreLoader
  },
  data() {
    return {
      username: "",
      password: "",
      showPassword: false
    };
  },
  methods: {
    async tryLogin() {
      this.$store.dispatch('login',{
        username:this.username,
        password:this.password
      }) 
    },
  },
  computed:{
    load(){
      return this.$store.getters.getLoad;
    }
  }
};
</script>

<style>
  .login{
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  .login-wrapper{
    display: flex;
    flex-direction: column;
    gap: 25px;
    width: 75vh;
    margin: 0 auto;
    border-radius: 20px;
    border: 2px solid rgb(166, 154, 167);
    padding: 35px 25px;
    background-color: #000 ;
  }
  .login-head{
    text-align: center;
    color: #fff;
    font-size: 30px;
    border-bottom: 1px solid rgb(166, 154, 167);
  }
  .login-input{
    border: none;
    padding: 5px 15px;
    border-radius: 15px;
    color: #000;
    font-size: 20px;
  }
  .login-btn{
    display: flex;
    justify-content: center;
    width: 100%;
  }
  .login-btn-button{
    padding: 10px 15px;
    border-radius: 15px;
    border: none;
    cursor: pointer;
    margin: 0 auto;
    width: 40%;
    background-color: #fff;
  }
  .login-btn-button:hover {
    box-shadow: 0px 5px 10px rgba(211, 176, 22, 0.5);
    color: #967418;
    animation: shadow-pulse 1s infinite;
  }
  .login-other{
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: #fff;
  }
  .login-other-f{
    cursor: pointer;
    padding: 5px 10px;
    color: #fff;
  }
  .login-other-f:hover{
    color: #e4b42f;
  }
  .password-block{
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  .password-check{
    cursor: pointer;
    color: #fff;
    user-select: none;
  }
  @media (max-width: 1296px) {
    .login{
      padding-top: 90px;
      padding-bottom: 30px;
    }
  }
  @media (max-width: 768px) {
    .password-block, .login-other{
      text-align: center;
    }
    .login-btn-button {
      width: 75%;
    }
  }
  @media (max-width: 480px) {
    .login-wrapper{
      width: 50vh;
    }
    .login-btn-button {
      width: 90%;
    }

  }
  .check{
    display: block !important;
    cursor: pointer;
    margin-right: 5px;
  }
  .google-login-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    background-color: #ffffff;
    color: white;
  }
  .google-icon {
    width: 35px;
    height: 35px;
  }
  .google{
    display: flex;
    align-items: center;
    gap: 10px;
    border: 1px solid #000;
    background-color: #fff;
}
</style>