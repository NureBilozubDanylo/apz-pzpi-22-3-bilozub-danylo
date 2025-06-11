<template>
    <div class="shops">
      <div class="container">
        <div v-if="userRole !== 'worker'" class="create-wrapper">
            <div class="create-shop">
                <h3 class="create-h">Create new shop</h3>
                <p class="shop-name">Shop name</p>
                <input type="text" v-model="shopName">
                <p class="shop-name">Shop address</p>
                <input type="text" v-model="shopAddress">
                <p class="shop-name">Shop work schedule</p>
                <input type="text" v-model="work_schedule">
                <button @click="createShop" class="create-btn">Create</button>
            </div>
        </div>
        
        <div class="your-shops">
            <h2 class="your-shops-h">Your shops</h2>
            <div class="shops-wrapper">
                <div class="shop" v-for="shop in userShops" :key="shop.id">
                    <h4 class="your-shop-name">Shop name: {{ shop.name }}</h4>
                    <p class="your-shop-address">Shop address: {{ shop.location }}</p>
                    <p class="your-shop-address">Shop work schedule: {{ shop.work_schedule }}</p>
                    <router-link :to="{ name: 'shop', params: { id: shop.shop_id } }">
                        <button>Get in Shop</button>
                    </router-link> 
                </div>
            </div>
        </div>
      </div>
    </div>
</template>
<script>
export default {
    name: 'MainC',
    created() {
        this.$store.dispatch('fetchUserShops');
    },
    data() {
        return {
            shopName: "",
            shopAddress: "",
            work_schedule: "",
        };
    },
    computed: {
        userShops() {
            if (this.$store.getters.getUserShops.length === 0) {
                return [];
            }
            return this.$store.getters.getUserShops;
        },
        userRole() {
            return localStorage.getItem('role');
        },
    },
    methods:{
        createShop() {
            const shopData = {
                name: this.shopName,
                location: this.shopAddress,
                work_schedule: this.work_schedule,
            };
            this.$store.dispatch('createShop', shopData).then(() => {
                this.shopName = "";
                this.shopAddress = "";
                this.work_schedule = "";
            });
        },
    }
};
</script>
<style>
   .create-shop{
    display: flex;
    margin: 0 auto;
    flex-direction: column;
    gap: 10px;
    padding: 15px;
    border: 1px solid black;
    border-radius: 30px;
    margin-top: 30px;
    justify-content: center;
    align-items: center;
    width: 50%;
   }
   .shops-wrapper{
    margin: 30px 0;
    display: flex;
    flex-wrap: wrap;
    gap: 30px;
    align-items: center;
    justify-content: space-around;
   }
   .shop{
    display: flex;
    flex-direction: column;
    padding: 15px;
    border: 1px solid black;
    border-radius: 30px;
    width: 30%;
    align-items: center;
    gap: 15px;
   }
   .your-shops-h{
    text-align: center;
    margin-top: 50px;
   }
</style>