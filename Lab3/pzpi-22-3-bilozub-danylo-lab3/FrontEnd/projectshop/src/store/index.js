import { createStore } from 'vuex'
import router from '../router/index.js'; 

export default createStore({
  state: {
    user:[],
    load:false,
    theme: false,
    adminInfo:[],
    adminInfoPagination:[],
    adminPagination:{
      skip:0,
      count:3,
      page:1
    },
    userShops: [],
    shop: {},
    products: [],
    allProducts: [],
    categories: [],
    receipts: [],
    shopStats: null,
    shopWorkers: [],
    anotherWorkers: [],
    invites: [], // New state for invites
  },
  getters: {
    getUser(state){
      return state.user
    },
    getLoad(state){
      return state.load
    },
    getTheme(state){
      return state.theme
    },
    getAdminInfo(state){
      return state.adminInfo
    },
    getAdminPagination(state){
      return state.adminPagination
    },
    getUserShops(state) {
      return state.userShops;
    },
    getShop(state) {
      return state.shop;
    },
    getProducts(state) {
      return state.products;
    },
    getAllProducts(state) {
      return state.allProducts;
    },
    getCategories(state) {
      return state.categories;
    },
    getCategoriesHistory(state) {
      return state.categoriesHistory;
    },
    getReceipts(state) {
      return state.receipts;
    },
    getShopStats(state) {
      return state.shopStats;
    },
    getShopWorkers(state) {
      return state.shopWorkers;
    },
    getAnotherWorkers(state) {
      return state.anotherWorkers;
    },
    getInvites(state) {
      return state.invites;
    },
  },
  mutations: {
    setUser(state,payload){
      state.user = payload
    },
    logout(state,payload){
      state.user = payload
    },
    setLoad(state,payload){
      state.load = payload
    },
    setTheme(state){
      state.theme = !state.theme
    },
    setAdminInfo(state,payload){
      state.adminInfo = payload
    },
    setAdminPagination(state,payload){
      state.adminPagination = payload
    },
    setUserShops(state, payload) {
      state.userShops = payload;
    },
    setShop(state, payload) {
      state.shop = payload;
    },
    setProducts(state, payload) {
      state.products = payload;
    },
    setAllProducts(state, payload) {
      state.allProducts = payload;
    },
    setCategories(state, payload) {
      state.categories = payload;
    },
    setCategoriesHistory(state, payload) {
      state.categoriesHistory = payload;
    },
    setReceipts(state, payload) {
      state.receipts = payload;
    },
    setShopStats(state, stats) {
      state.shopStats = stats;
    },
    setShopWorkers(state, payload) {
      state.shopWorkers = payload;
    },
    setAnotherWorkers(state, payload) {
      state.anotherWorkers = payload;
    },
    setInvites(state, payload) {
      state.invites = payload;
    },
  },
  actions: {
    async login({ commit }, payload) {
      commit('setLoad', true);
      const response = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          username: payload.username,
          password: payload.password,
        }),
      });
      let res = await response.json();
      if (res.access_token) {
        console.log(res);
        localStorage.setItem('token', res.access_token);
        localStorage.setItem('username', payload.username);
        localStorage.setItem('user_id', res.user_id);
        localStorage.setItem('role', res.role);
        router.push('/');
      }
      commit('setUser', res);
      commit('setLoad', false);
    },
    async register({ commit },payload) {
      try {
        commit('setLoad',true)
        await fetch("http://localhost:8000/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: payload.username,
            password: payload.password,
            email: payload.email,
            mobile_number: payload.mobile_number,
            role: payload.role,
            age: payload.age,
          }),
        });
        router.push('/login');
      } catch (error) {
        console.log(error);
      }
      commit('setLoad',false)
    },
    async logout({ commit }) {
      commit('logout',[])
    },
    async googleLogin({ commit },payload) {
      commit('setUser',payload)
    },
    setTheme({commit}){
      commit('setTheme')
    },
    async getAdminInfo({ commit }){
        commit('setLoad',true)
        const token = localStorage.getItem('token1');
        let response = await fetch(`https://api.pinq.yooud.org/admin/user`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
          }
        })
        let res = await response.json();
        res.data.forEach((el) => {
          const date = new Date(el.created_at * 1000);
          el.created_at = date.toDateString();
          el.username = el.profile.username;
          el.profile_image = el.profile.profile_picture_url
          delete el.profile
        });
        commit('setAdminInfo', res);
        commit('setLoad',false)
      },
      async modifyRole({ commit },payload){
        const token = localStorage.getItem('token1');
        commit('setLoad',true)
        await fetch(`https://api.pinq.yooud.org/admin/user/${payload.id}`, {
          method: "PATCH", // Метод запиту
          headers: {
            "Content-Type": "application/json", // Формат даних
            "Authorization": `Bearer ${token}` // Додаємо токен авторизації
          },
          body: JSON.stringify({role:payload.role}) // Дані які ми відправляємо на сервер
        })
  
        commit('setLoad',false)
      },
      setAdminPagination({commit},payload){
        commit('setAdminPagination',payload)
      },
      async fetchUserShops({ commit }) {
        commit('setLoad', true);
        const token = localStorage.getItem('token');
        const username = localStorage.getItem('username'); // Используем username из localStorage
        try {
          const response = await fetch(`http://127.0.0.1:8000/shops/user/${username}/shops`, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
            },
          });
          const shops = await response.json();
          if(shops.length > 0){
            commit('setUserShops', shops);
          }
        } catch (error) {
          console.error("Failed to fetch user shops:", error);
        }
        commit('setLoad', false);
      },
      async createShop({ commit }, payload) {
        commit('setLoad', true);
        const token = localStorage.getItem('token');
        try {
          const response = await fetch("http://127.0.0.1:8000/shops/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify({
              name: payload.name,
              work_schedule: payload.work_schedule,
              location: payload.location,
              user_id: +localStorage.getItem('user_id')
            }),
          });
          const shop = await response.json();
          console.log("Shop created:", shop);
          this.dispatch('fetchUserShops');
        } catch (error) {
          console.error("Failed to create shop:", error);
        }
        commit('setLoad', false);
      },
      async fetchShopById({ commit }, shopId) {
        commit('setLoad', true);
        const token = localStorage.getItem('token');
        try {
          const response = await fetch(`http://127.0.0.1:8000/shops/${shopId}`, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
            },
          });
          const shop = await response.json();
          commit('setShop', shop);
        } catch (error) {
          console.error("Failed to fetch shop details:", error);
          throw error; // Re-throw the error for further handling
        } finally {
          commit('setLoad', false);
        }
      },
      async getProducts({ commit }, payload) {
        commit('setLoad', true);
        const token = localStorage.getItem('token');
        try {
          const response = await fetch(`http://127.0.0.1:8000/supplies/shop/${payload.shop_id}/${payload.category_id}`, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
            },
          });
          const products = await response.json();
          console.log("Fetched products:", products);
          if (products.length == 0) {
            commit('setProducts', []);
          }
          commit('setProducts', products);
        } catch (error) {
          console.error("Failed to fetch shop Products:", error);
          throw error;
        } finally {
          commit('setLoad', false);
        }
      },
      async createProduct({ commit }, payload) {
        commit('setLoad', true);
        const token = localStorage.getItem('token');
        try {
          const response = await fetch("http://127.0.0.1:8000/supplies/createAndAdd", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify({
              name: payload.name,
              sale_price: payload.sale_price,
              purchase_price: payload.purchase_price,
              size_weight: payload.size_weight,
              producer: payload.producer,
              category_id: payload.category_id,
              quantity: payload.quantity,
              shop_id: payload.shop_id,
              image_url: payload.image_url,
            }),
          });
          const product = await response.json();
          console.log("Product created:", product);
          this.dispatch('getProducts', {shop_id:payload.shop_id,category_id:1});
        } catch (error) {
          console.error("Failed to create product:", error);
        } finally {
          commit('setLoad', false);
        }
      },
      async fetchAllProducts({ commit }, payload) {
        commit('setLoad', true);
        const token = localStorage.getItem('token');
        try {
          const response = await fetch(`http://127.0.0.1:8000/supplies/notInShop/${payload.shop_id}/${payload.category_id}`, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
            },
          });
          const products = await response.json();
          commit('setAllProducts', products);
        } catch (error) {
          console.error("Failed to fetch all products:", error);
        } finally {
          commit('setLoad', false);
        }
      },
      async addProductToShop({ commit }, payload) {
        commit('setLoad', true);
        const token = localStorage.getItem('token');
        try {
          await fetch("http://127.0.0.1:8000/shop_supplies/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify({
              supply_id: payload.supply_id,
              shop_id: payload.shop_id,
              quantity: 0,
              sale_price: 1,
            }),
          });
          this.dispatch('getProducts', {shop_id:payload.shop_id,category_id:1});
          this.dispatch('fetchAllProducts', { shop_id: payload.shop_id,category_id:1 });
        } catch (error) {
          console.error("Failed to add product to shop:", error);
        } finally {
          commit('setLoad', false);
        }
      },
      async fetchCategoriesByParent({ commit }, parentId) {
        commit('setLoad', true);
        const token = localStorage.getItem('token');
        try {
          const response = await fetch(`http://127.0.0.1:8000/categories/children/${parentId}`, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
            },
          });
          const categories = await response.json();
          if(categories.detail){
            commit('setCategories', []);
            return;
          }
          commit('setCategories', categories);
        } catch (error) {
          console.error("Failed to fetch categories by parent:", error);
        } finally {
          commit('setLoad', false);
        }
      },
      async deleteProduct({ commit, state }, payload) {
        commit('setLoad', true);
        const token = localStorage.getItem('token');
        try {
          await fetch(`http://127.0.0.1:8000/shop_supplies/${payload.shop_id}/${payload.productId}`, {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
            },
          });
          const updatedProducts = state.products.filter(product => product.supply_id !== payload.productId);
          commit('setProducts', updatedProducts);
          this.dispatch('fetchAllProducts', { shop_id: payload.shop_id,category_id:1 });
        } catch (error) {
          console.error("Failed to delete product:", error);
        } finally {
          commit('setLoad', false);
        }
      },
      async confirmSale({ commit }, payload) {
        commit('setLoad', true);
        const token = localStorage.getItem('token');
        try {
          const response = await fetch("http://127.0.0.1:8000/sales/confirm", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify({
              shop_id: payload.shop_id,
              products: payload.products,
              paymentType: payload.paymentType,
            }),
          });
          const result = await response.json();
          console.log("Sale confirmed:", result);
        } catch (error) {
          console.error("Failed to confirm sale:", error);
        } finally {
          commit('setLoad', false);
        }
      },
      async fetchReceipts({ commit }, payload) {
        commit('setLoad', true);
        const token = localStorage.getItem('token');
        try {
          const response = await fetch(`http://127.0.0.1:8000/sales/shop/${payload.shop_id}`, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
            },
          });
          const receipts = await response.json();
          commit('setReceipts', receipts);
        } catch (error) {
          console.error("Failed to fetch receipts:", error);
        } finally {
          commit('setLoad', false);
        }
      },
      async fetchShopStats({ commit }, payload) {
        const token = localStorage.getItem('token');
        const response = await fetch(`http://127.0.0.1:8000/shops/${payload.shop_id}/stats?sales_date=${payload.date}`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`,
          },
        });
        const stats = await response.json();
        commit('setShopStats', stats);
      },
      async fetchShopWorkers({ commit }, payload) {
        commit('setLoad', true);
        const token = localStorage.getItem('token');
        try {
          const response = await fetch(`http://127.0.0.1:8000/shops/${payload.shop_id}/workers`, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
            },
          });
          const workers = await response.json();
          commit('setShopWorkers', workers);
        } catch (error) {
          console.error("Failed to fetch shop workers:", error);
        } finally {
          commit('setLoad', false);
        }
      },
      async fireWorker({ commit }, payload) {
        commit('setLoad', true);
        const token = localStorage.getItem('token');
        try {
          await fetch(`http://127.0.0.1:8000/shops/workers/${payload.workerId}`, {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
            },
          });
          this.dispatch('fetchShopWorkers', { shop_id: payload.shop_id });
        } catch (error) {
          console.error("Failed to fire worker:", error);
        } finally {
          commit('setLoad', false);
        }
      },
      async fetchAnotherWorkers({ commit }, payload) {
        commit('setLoad', true);
        const token = localStorage.getItem('token');
        try {
          const response = await fetch(`http://127.0.0.1:8000/shops/${payload.shop_id}/another-workers`, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
            },
          });
          const workers = await response.json();
          commit('setAnotherWorkers', workers);
        } catch (error) {
          console.error("Failed to fetch another workers:", error);
        } finally {
          commit('setLoad', false);
        }
      },
      async sendInvitation({ commit }, payload) {
        commit('setLoad', true);
        const token = localStorage.getItem('token');
        try {
          await fetch(`http://127.0.0.1:8000/shops/${payload.shop_id}/invite`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
            },
            body: JSON.stringify({
              user_id: payload.user_id,
              message: payload.message,
              shop_id: payload.shop_id,
            }),
          });
          console.log("Invitation sent successfully!");
        } catch (error) {
          console.error("Failed to send invitation:", error);
        } finally {
          commit('setLoad', false);
        }
      },
      async fetchInvites({ commit }) {
        commit('setLoad', true);
        const token = localStorage.getItem('token');
        const user_id = localStorage.getItem('user_id');
        try {
          const response = await fetch(`http://127.0.0.1:8000/invites/${user_id}`, {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
            },
          });
          const data = await response.json();
          commit('setInvites', data);
        } catch (error) {
          console.error('Error fetching invites:', error);
        } finally {
          commit('setLoad', false);
        }
      },
      async acceptInvite({ commit }, payload) {
        commit('setLoad', true);
        const token = localStorage.getItem('token');
        try {
          await fetch(`http://127.0.0.1:8000/invites/accept/${payload.requestId}/${payload.status}`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`,
            },
          });
          console.log("Invite accepted successfully!");
          router.push('/shops'); // Redirect to /shops after success
        } catch (error) {
          console.error("Error accepting invite:", error);
        } finally {
          commit('setLoad', false);
        }
      },
    },
    modules: {
    }
  })
