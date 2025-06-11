<template>
    <footer :class="{'footer':true,'light':this.$store.getters.getTheme}">
      <div class="container">
        <div class="footer-wrapper">
            <div class="footer-logo">
              <h5 :class="{'footer-name':true,'light':this.$store.getters.getTheme}">ZooHelper</h5>
              <p :class="{'footer-name-text':true,'light':this.$store.getters.getTheme}">
                © 2025 ZooHelper
              </p>
            </div>
            <div class="footer-main">

              <p :class="{'footer-main-el':true,'light':this.$store.getters.getTheme}" @click ="scrollToElement('about')">About us</p>
              <p :class="{'footer-main-el':true,'light':this.$store.getters.getTheme}"  @click ="scrollToElement('faq')">
                  FAQ
              </p>
            </div>
            <div class="footer-social-b">
              <div class="footer-social">
                <div :class="{'footer-social-block':true,'stroke1':this.$store.getters.getTheme}">
                  <svg :class="{'svg':true}" width="24px" height="24px" stroke-width="1.5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" color="#000000"><path :class="{'stroke':this.$store.getters.getTheme}" d="M21 5L2 12.5L9 13.5M21 5L18.5 20L9 13.5M21 5L9 13.5M9 13.5V19L12.2488 15.7229" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg>
                </div>
              </div>
            </div>
        </div>
      </div>
    </footer>
  </template>
  
    <script>
    export default {
    name: "FooterC",
    methods: {
      scrollToElement(el) {
        setTimeout(()=>{
          console.log("aaaa")
          const element = document.getElementById(el);
          if (element) {
            element.scrollIntoView({ behavior: "smooth" });
          }
        },1)
        this.$router.push({name:'main'})
      }
    },
    };
    </script>
  
  <style>
  .footer {
    padding: 10px 0;
    flex-grow: 0;
    background-color: #000;
    z-index: 9999;
  }
  .footer-wrapper{
    display: flex;
    align-items: center;
    justify-content: space-between;
    color: #fff;
    font-size: 18px;
  }
  .footer-logo{
    display: flex;
    align-items: center;
    gap: 30px;
  }
  .footer-name{
    font-size: 20px;
    padding: 10px;
    cursor: pointer;
  }
  .footer-name-text{
    padding: 10px;
    cursor: pointer;
  }
  .footer-main{
    display: flex;
    align-items: center;
    gap: 30px;
  }
  .footer-main-el{
    padding: 10px;
    cursor: pointer;
  }
  .hover:hover{
    color: #e4b42f;
  }
  .footer-social-block{
    cursor: pointer;
    padding: 1px 4px 1px 3px;
    border: 1px solid #fff;
    border-radius: 100%;
    width: 35px;
  }
  .footer-social{
    padding: 10px;
    display: flex;
    justify-content: center;
  }

  @media (max-width: 1296px) {
    .footer-logo, .footer-main{
      width: 33%;
    }
  }
  @media (max-width: 768px) {
    .footer-social-b{
      width: 33%;
    }
    .footer-logo, .footer-main{
      flex-direction: column;
      gap: 5px;
      text-align: center;
      width: 33%;
    }
    .about-wrapper{
      padding: 0 !important;
    }
  }
  @media (max-width: 480px) {

  }
  </style>
  