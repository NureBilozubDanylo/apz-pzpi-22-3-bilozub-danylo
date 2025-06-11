<template>
    <div class="login">
      <PreLoader :loading = "load"></PreLoader>
      <div class="container">
        <div :class="{'login-wrapper':true,'light':this.$store.getters.getTheme}">
          <h2 :class="{'login-head':true,'light':this.$store.getters.getTheme}">Register</h2>
          <input
            type="text"
            :class="{'login-input':true,'input-light':this.$store.getters.getTheme}"
            v-model="username"
            placeholder="Username"
          />
          <input
            type="text"
            :class="{'login-input':true,'input-light':this.$store.getters.getTheme}"
            v-model="email"
            placeholder="Email"
          />
          <input
            type="text"
            :class="{'login-input':true,'input-light':this.$store.getters.getTheme}"
            v-model="number"
            placeholder="Mobile number"
          />
          <input
            type="number"
            :class="{'login-input':true,'input-light':this.$store.getters.getTheme}"
            v-model="age"
            placeholder="Age"
          />
          <select
            :class="{'login-input':true,'input-light':this.$store.getters.getTheme}"
            v-model="role"
          >
            <option value="" disabled>Select Role</option>
            <option value="worker">Worker</option>
            <option value="director">Director</option>
          </select>
          <input
            :type="showPassword ? 'text' : 'password'" 
            :class="{'login-input':true,'input-light':this.$store.getters.getTheme}"
            v-model="password"
            placeholder="Password"
          />
          <div class="password-block">
            <input
              :type="showPassword ? 'text' : 'password'" 
              :class="{'login-input':true,'input-light':this.$store.getters.getTheme}"
              v-model="password1"
              placeholder="Password"
            />
            <label class="password-check" :class="{'black-color':this.$store.getters.getTheme}">
              <input type="checkbox" class = "check" v-model="showPassword" />
              Show password
            </label>
          </div>
          <div class="login-btn">
            <button class="login-btn-button" :class="{'light-btn':this.$store.getters.getTheme}" @click="tryRegister">Register</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import PreLoader from "./PreLoader.vue";
  export default {
    name: "RegisterC",
    components: {
      PreLoader
    },
    data() {
      return {
        username: "",
        password: "",
        password1: "",
        number: "",
        email: "",
        age: null,
        role: "",
        showPassword: false
      };
    },
    methods: {
      async tryRegister(){
        this.$store.dispatch('register',{
        username:this.username,
        password:this.password,
        mobile_number:this.number,
        email:this.email,
        age: this.age,
        role: this.role
      }) 
      }
    },
    computed:{
    load(){
      return this.$store.getters.getLoad;
    }
  }
  };
  </script>
