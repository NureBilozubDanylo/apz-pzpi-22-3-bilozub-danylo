<template>
  <div class="shop-prof">
  <div class="container">
    <div class="shop-one">
      <h1 class="shop-name">Shop: {{ shop.name }}</h1>
      <div class="shop-head">
        <h2 class="shop-address">Address: {{ shop.location }}</h2>
        <h3 class="work-schedule">Work schedule: {{ shop.work_schedule }}</h3>
      </div>
      <div class="start-work-block">
        <router-link :to="{ name: 'work',params: { id: this.$route.params.id } }">
          <button class="btn">Start work</button>
          </router-link> 
      </div>
      <div class="workers-block">
        <h2 class="shop-address">Workers:</h2>
        <div class="workers scrollable">
          <div class="worker" v-for="worker in shopWorkers" :key="worker.user_id">
            <h4 class="worker-name">Username: {{ worker.username }}</h4>
            <p class="worker-role">Role: {{ worker.role }}</p>
            <p class="worker-email">Email: {{ worker.email }}</p>
            <p class="worker-mobile">Mobile: {{ worker.mobile_number }}</p>
            <p class="worker-age">Age: {{ worker.age }}</p>
            <p class="worker-position">Position: {{ worker.position }}</p>
            <p class="worker-salary" v-if="worker.position !== 'Owner'">Salary: {{ worker.salary_without_percent }}</p>
            <button class="delete-button" v-if="worker.position !== 'Owner'" @click="confirmFire(worker.user_id)">Fire</button>
          </div>
        </div>
      </div>
      <div class="products-wrapper">
        <h2 class="products-h">Products</h2>
        <div class="btnCreate">
          <button class="btn" @click="showCreateModal">Create new product</button>
          <button class="btn" @click="showSelectModal = true">Add already created product</button>
          <router-link :to="{ name: 'shopStats', params: { id: this.$route.params.id } }">
            <button class="btn">Shop stats</button>
          </router-link>
          <router-link :to="{ name: 'sensors', params: { id: this.$route.params.id } }">
            <button class="btn">Sensors</button>
          </router-link>
          <router-link :to="{ name: 'animals', params: { id: this.$route.params.id } }">
            <button class="btn">Animals</button>
          </router-link>
          <router-link :to="{ name: 'climateHistory', params: { id: this.$route.params.id } }">
            <button class="btn">Climate history</button>
          </router-link>
          <button class="btn" @click="showWorkerModal = true">Add new worker</button>
        </div>
        <div class="search-pannel">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Search by name..." 
            class="search-input"
          />

          <div class="category-block">
            <div class="categories-history">
              <div class="category-history" @click="selectCategory(cat.id)" v-for="cat in categoriesHistory" :key="cat.id" >
                {{cat.name}} /
              </div>
            </div>
            <h3>Categories</h3>
            <div class="categories">
              <div class="category-btn-block" v-for="cat in categories" :key="cat.id" >
                <button class="category" @click="selectCategory(cat.id)">{{cat.name}}</button>
              </div>
            </div>
          </div>
        </div>
        <div class="products">
          <div class="product" v-for="product in paginatedProducts" :key="product.id">
            <img :src="product.image_url" alt="Product Image" class="product-image" />
            <h4 class="product-name">Name: {{ product.name }}</h4>
            <p class="product-description">Sale price: {{ product.sale_price }}</p>
            <p class="product-price">Purchase price: {{ product.purchase_price }}</p>
            <p class="product-quantity">Size weight: {{ product.size_weight }}</p>
            <p class="product-category">Producer: {{ product.producer }}</p>
            <p class="product-category">Quantity: {{ product.quantity }}</p>
            <button class="delete-button" @click="confirmDelete(product.supply_id)">Delete</button>
          </div>
        </div>
        <div class="pagination">
          <button 
            :disabled="currentPage === 1" 
            @click="currentPage--" 
            class="pagination-button btn"
          >
            Previous
          </button>
          <span>Page {{ currentPage }} of {{ totalPages }}</span>
          <button 
            :disabled="currentPage === totalPages || totalPages === 0" 
            @click="currentPage++" 
            class="pagination-button btn"
          >
            Next
          </button>
        </div>
      </div>

      <!-- Modal for creating a new product -->
      <div v-if="showModal" class="modal-overlay">
        <div class="modal">
          <h3>Create New Product</h3>
          <form @submit.prevent="createProduct">
            <label>
              Name:
              <input type="text" v-model="newProduct.name" required />
            </label>
            <label>
              Sale Price:
              <input type="number" v-model="newProduct.sale_price" required />
            </label>
            <label>
              Purchase Price:
              <input type="number" v-model="newProduct.purchase_price" required />
            </label>
            <label>
              Size/Weight:
              <input type="text" v-model="newProduct.size_weight" required />
            </label>
            <label>
              Producer:
              <input type="text" v-model="newProduct.producer" required />
            </label>
            <label>
              Photo URL:
              <input type="text" v-model="newProduct.image_url"/>
            </label>
            <label class="category-dropdown">
              Selected category: {{ selectedCategoryName }}
              <div class="category-block category-dropdown">
                <div class="categories-history">
                  <div class="category-history" @click="selectCategory(cat.id)" v-for="cat in categoriesHistory" :key="cat.id" >
                    {{cat.name}} /
                  </div>
                </div>
                <div class="categories">
                  <div class="category-btn-block" v-for="cat in categories" :key="cat.id" >
                    <button class="category" @click="selectCategory(cat.id)">{{cat.name}}</button>
                  </div>
                </div>
              </div>
            </label>
            <label>
              Quantity:
              <input type="number" v-model="newProduct.quantity" required />
            </label>
            <button class="btn" type="submit">Submit</button>
            <button class="btn" type="button" @click="showModal = false">Cancel</button>
          </form>
        </div>
      </div>

      <!-- Modal for selecting an existing product -->
      <div v-if="showSelectModal" class="modal-overlay">
        <div class="modal1 modalselect modal2">
          <h3>Select Product to Add</h3>
          <div class="search-pannel">
            <input 
              type="text" 
              v-model="searchQueryAdd" 
              placeholder="Search by name..." 
              class="search-input"
            />
            <div class="category-block">
              <div class="categories-history">
                <div class="category-history" @click="selectCategory(cat.id)" v-for="cat in categoriesHistory" :key="cat.id" >
                  {{cat.name}} /
                </div>
              </div>
              <h3>Categories</h3>
              <div class="categories">
                <div class="category-btn-block" v-for="cat in categories" :key="cat.id" >
                  <button class="category" @click="selectCategory(cat.id)">{{cat.name}}</button>
                </div>
              </div>
            </div>
          </div>
          <div class="products">
            <div class="product" v-for="product in filteredProducts" :key="product.id">
              <img :src="product.image_url" alt="Product Image" class="product-image" />
              <h4 class="product-name">Product name: {{ product.name }}</h4>
              <p class="product-description">Product sale price: {{ product.sale_price }}</p>
              <p class="product-price">Product purchase price: {{ product.purchase_price }}</p>
              <p class="product-quantity">Product size weight: {{ product.size_weight }}</p>
              <button @click="addProductToShop(product.supply_id)">Add to Shop</button>
            </div>
          </div>
          <div class="pagination">
            <button 
              :disabled="currentPageAdd === 1" 
              @click="currentPageAdd--" 
              class="pagination-button btn"
            >
              Previous
            </button>
            <span>Page {{ currentPageAdd }} of {{ totalPagesAdd }}</span>
            <button 
              :disabled="currentPageAdd === totalPagesAdd || totalPagesAdd === 0" 
              @click="currentPageAdd++" 
              class="pagination-button btn"
            >
              Next
            </button>
          </div>
          <button class="btn" @click="closeModal">Close</button>
        </div>
      </div>

      <!-- Modal for adding a new worker -->
      <div v-if="showWorkerModal" class="modal-overlay">
        <div class="modal1">
          <h3>Add New Worker</h3>
          <div class="search-pannel">
            <input 
              type="text" 
              v-model="searchWorkerQuery" 
              placeholder="Search by username..." 
              class="search-input"
            />
          </div>
          <div class="users scrollable">
            <div class="user" v-for="user in filteredAnotherWorkers" :key="user.user_id">
              <h4 class="user-name">Username: {{ user.username }}</h4>
              <p class="user-role">Role: {{ user.role }}</p>
              <p class="user-email">Email: {{ user.email }}</p>
              <p class="user-mobile">Mobile: {{ user.mobile_number }}</p>
              <p class="user-age">Age: {{ user.age }}</p>
              <button class="btn" @click="openInviteModal(user.user_id)">Invite</button>
            </div>
          </div>
          <div class="pagination">
            <button 
              :disabled="currentWorkerPage === 1" 
              @click="currentWorkerPage--" 
              class="pagination-button btn"
            >
              Previous
            </button>
            <span>Page {{ currentWorkerPage }} of {{ totalWorkerPages }}</span>
            <button 
              :disabled="currentWorkerPage === totalWorkerPages || totalWorkerPages === 0" 
              @click="currentWorkerPage++" 
              class="pagination-button btn"
            >
              Next
            </button>
          </div>
          <button class="btn" @click="showWorkerModal = false">Close</button>
        </div>
      </div>

      <!-- Modal for sending an invitation -->
      <div v-if="showInviteModal" class="modal-overlay">
        <div class="modal">
          <h3 style="text-align: center;">Send Invitation</h3>
          <form @submit.prevent="sendInvitation">
            <label>
              Message:
              <textarea v-model="inviteMessage" rows="4" placeholder="Write your message here..." required></textarea>
            </label>
            <div class="confirm-btns">
              <button class="btn" type="submit">Send</button>
              <button class="btn" type="button" @click="showInviteModal = false">Cancel</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Confirmation Modal -->
      <div v-if="showDeleteModal" class="modal-overlay">
        <div class="modal">
          <h3 style="text-align: center;">Confirm Deletion</h3>
          <p>Are you sure you want to delete this product?</p>
          <div class="confirm-btns">
            <button class="btn" @click="deleteProduct(confirmedProductId)">Yes</button>
            <button class="btn" @click="showDeleteModal = false">No</button>
          </div>
        </div>
      </div>

      <!-- Confirmation Modal for firing a worker -->
      <div v-if="showFireModal" class="modal-overlay">
        <div class="modal">
          <h3 style="text-align: center;">Confirm Firing</h3>
          <p>Are you sure you want to fire this worker?</p>
          <div class="confirm-btns">
            <button class="btn" @click="fireWorker(confirmedWorkerId)">Yes</button>
            <button class="btn" @click="showFireModal = false">No</button>
          </div>
        </div>
      </div>
    </div>
  </div>    
</div>
</template>
<script>

export default {
    name: 'ShopC',
    created() {
        const shop_id = this.$route.params.id;
        this.$store.dispatch('fetchShopById', shop_id);
        this.$store.dispatch('fetchAllProducts',{shop_id,category_id: 1});
        this.$store.dispatch('getProducts', {shop_id,category_id: 1});
        this.$store.dispatch('fetchCategoriesByParent', 1)
        this.$store.dispatch('fetchShopWorkers', {shop_id})
        this.$store.dispatch('fetchAnotherWorkers', {shop_id})
    },
    data() {
        return {
            showModal: false,
            showSelectModal: false,
            showDeleteModal: false,
            showWorkerModal: false,
            showFireModal: false,
            showInviteModal: false,
            confirmedProductId: null,
            confirmedWorkerId: null,
            inviteMessage: '',
            selectedUserId: null,
            newProduct: {
                name: '',
                sale_price: null,
                purchase_price: null,
                size_weight: '',
                producer: '',
                category_id: null,
                quantity: null,
                shop_id: this.$route.params.id
            },
            searchQuery: '',
            searchQueryAdd: '',
            searchWorkerQuery: '',
            selectedCategory: '',
            currentPage: 1,
            currentPageAdd: 1,
            currentWorkerPage: 1,
            itemsPerPage: 3,
            workersPerPage: 5,
            categoriesHistory: [{id: 1, name: 'All Products'}],
        };
    },
    methods: {
        headCategory(){
          const shop_id = this.$route.params.id;
          if(!shop_id){
            this.categoriesHistory = [{id: 1, name: 'All Products'}];
            this.$store.dispatch('fetchAllProducts',{shop_id:1,category_id: 1});
            this.$store.dispatch('getProducts', {shop_id:1,category_id: 1});
            this.$store.dispatch('fetchCategoriesByParent', 1)
          }else{
            this.categoriesHistory = [{id: 1, name: 'All Products'}];
            this.$store.dispatch('fetchAllProducts',{shop_id,category_id: 1});
            this.$store.dispatch('getProducts', {shop_id,category_id: 1});
            this.$store.dispatch('fetchCategoriesByParent', 1)
          }
        },
        showCreateModal() {
            this.showModal = true;
            this.headCategory()
        },
        
        closeModal() {
          this.showSelectModal = false;
          this.headCategory()
        },
        createProduct() {
            let catId = this.categoriesHistory[this.categoriesHistory.length - 1].id
            this.newProduct.category_id = catId
            // Dispatch an action to create a new product
            this.$store.dispatch('createProduct', this.newProduct).then(() => {
                this.showModal = false;
                // Optionally, clear the form fields
                this.newProduct = {
                    name: '',
                    sale_price: null,
                    purchase_price: null,
                    size_weight: '',
                    producer: '',
                    category_id: null,
                    shop_id: this.$route.params.id
                };
            });
            this.headCategory()
        },
        addProductToShop(supply_id) {
            this.$store.dispatch('addProductToShop', { shop_id: this.$route.params.id, supply_id }).then(() => {
                this.showSelectModal = false;
            });
            this.headCategory()
        },
        confirmDelete(productId) {
          this.confirmedProductId = productId;
          this.showDeleteModal = true;
        },
        deleteProduct(productId) {
          const shop_id = this.$route.params.id;
          this.$store.dispatch('deleteProduct', { shop_id, productId });
          this.showDeleteModal = false;
        },
        selectCategory(categoryId) {
          const index = this.categoriesHistory.findIndex(cat => cat.id === categoryId);
          if (index !== -1) {
              this.categoriesHistory = this.categoriesHistory.slice(0, index + 1);
          } else {
              const category = this.categories.find(cat => cat.id === categoryId);
              if (category) {
                  this.categoriesHistory.push(category);
              }
          }
          this.$store.dispatch('fetchCategoriesByParent', categoryId);
          const shop_id = this.$route.params.id;
          this.$store.dispatch('getProducts', {shop_id,category_id: categoryId});
          this.$store.dispatch('fetchAllProducts',{shop_id,category_id: categoryId});
        },
        inviteWorker(userId) {
          const shop_id = this.$route.params.id;
          this.$store.dispatch('inviteWorkerToShop', { shop_id, userId }).then(() => {
            alert('Worker invited successfully!');
          });
        },
        confirmFire(workerId) {
          this.confirmedWorkerId = workerId;
          this.showFireModal = true;
        },
        fireWorker(workerId) {
          const shop_id = this.$route.params.id;
          this.$store.dispatch('fireWorker', { shop_id, workerId }).then(() => {
            this.showFireModal = false;
          });
        },
        openInviteModal(userId) {
          this.selectedUserId = userId;
          this.showInviteModal = true;
        },
        sendInvitation() {
          const shop_id = this.$route.params.id;
          const payload = {
            shop_id,
            user_id: this.selectedUserId,
            message: this.inviteMessage,
          };
          this.$store.dispatch('sendInvitation', payload).then(() => {
            alert('Invitation sent successfully!');
            this.showInviteModal = false;
            this.inviteMessage = '';
          });
        },
    },
    computed: {
        selectedCategoryName() {
          return this.categoriesHistory[this.categoriesHistory.length - 1].name || 'All Products';
        },
        categories() {
            return this.$store.getters.getCategories;
        },
        shop() {
            return this.$store.getters.getShop;
        },
        products() {
            return this.$store.getters.getProducts || []; // Ensure it defaults to an empty array
        },
        paginatedProducts() {
            const filteredProducts = this.products.filter(product => {
                return this.searchQuery
                    ? product.name.toLowerCase().includes(this.searchQuery.toLowerCase())
                    : true;
            });

            const start = (this.currentPage - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return filteredProducts.slice(start, end);
        },
        
        totalPages() {
            const filteredProducts = this.products.filter(product => {
                return this.searchQuery
                    ? product.name.toLowerCase().includes(this.searchQuery.toLowerCase())
                    : true;
            });
            return Math.ceil(filteredProducts.length / this.itemsPerPage);
        },
        totalPagesAdd() {
            const filteredProducts = this.$store.getters.getAllProducts || []; // Ensure it defaults to an empty array
            return Math.ceil(filteredProducts.filter(product => {
                return this.searchQueryAdd
                    ? product.name.toLowerCase().includes(this.searchQueryAdd.toLowerCase())
                    : true;
            }).length / this.itemsPerPage)
        },
        filteredProducts() {
            let filteredProducts = this.$store.getters.getAllProducts || []; // Ensure it defaults to an empty array
            filteredProducts = filteredProducts.filter(product => {
                return this.searchQueryAdd
                    ? product.name.toLowerCase().includes(this.searchQueryAdd.toLowerCase())
                    : true;
            });
            const start = (this.currentPageAdd - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return filteredProducts.slice(start, end);
        },
        filteredUsers() {
          const users = this.$store.getters.getUsers || []; // Ensure it defaults to an empty array
          const filtered = users.filter(user => {
            return this.searchWorkerQuery
              ? user.username.toLowerCase().includes(this.searchWorkerQuery.toLowerCase())
              : true;
          });
          const start = (this.currentWorkerPage - 1) * this.workersPerPage;
          const end = start + this.workersPerPage;
          return filtered.slice(start, end);
        },
        totalWorkerPages() {
          const users = this.$store.getters.getUsers || []; // Ensure it defaults to an empty array
          const filtered = users.filter(user => {
            return this.searchWorkerQuery
              ? user.username.toLowerCase().includes(this.searchWorkerQuery.toLowerCase())
              : true;
          });
          return Math.ceil(filtered.length / this.workersPerPage);
        },
        shopWorkers() {
          return this.$store.getters.getShopWorkers || [];
        },
        filteredAnotherWorkers() {
          const workers = this.$store.getters.getAnotherWorkers || [];
          const filtered = workers.filter(worker => {
            return this.searchWorkerQuery
              ? worker.username.toLowerCase().includes(this.searchWorkerQuery.toLowerCase())
              : true;
          });
          const start = (this.currentWorkerPage - 1) * this.workersPerPage;
          const end = start + this.workersPerPage;
          return filtered.slice(start, end);
        },
    },
    watch:{
      searchQuery() {
        this.currentPage = 1
      },
      searchQueryAdd() {
        this.currentPageAdd = 1
      },
      searchWorkerQuery() {
        this.currentWorkerPage = 1;
      },
    }
};
</script>
<style>
.btnCreate{
  display: flex;
  align-items: center;
  justify-content: center;
}
.shop-name, .shop-address, .work-schedule{
    text-align: center;
    margin-top: 10px;
  }
  .products-h{
    text-align: center;
  }
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal {
  background: white;
  padding: 20px;
  border-radius: 5px;
  width: 300px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
.modal1{
  background: white;
  padding: 20px;
  border-radius: 5px;
  width: 60%;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
.modal2{
  height: 80vh !important;
}
.modal h3 {
  margin-top: 0;
}
.modal p {
  margin: 10px 0;
  font-size: 16px;
  text-align: center;
}
.modal form label {
  display: block;
  margin-bottom: 10px;
}
.modal form input {
  width: 100%;
  padding: 5px;
  margin-top: 5px;
}
.modal form button {
  margin-right: 10px;
}
.search-pannel {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 20px 0;
}
.search-input {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 15px;
  padding: 10px 20px;
  width: 40%;
}
.category-dropdown {
  padding: 5px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.search-button {
  padding: 5px 10px;
  background-color: #000000;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.search-button:hover {
  background-color: #000000;
}
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}
.pagination-button {
  padding: 5px 10px;
  margin: 0 5px;
  background-color: #000000;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.pagination-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
.pagination-button:hover:not(:disabled) {
  background-color: #c7a229;
}
.products{
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 20px;
  gap: 20px;
}
.product{
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
  width: 30%;
  text-align: center;
  background-color: #f9f9f9;
}

.category-block {
  margin: 20px 0;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.categories-history {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 10px;
}

.category-history {
  margin-right: 5px;
  cursor: pointer;
  font-weight: bold;
}

.category-history:hover {
  text-decoration: underline;
}

.categories {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.category-btn-block {
  display: inline-block;
}

.category {
  padding: 8px 12px;
  background-color: #000000;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.category:hover {
  background-color: #be9d2f;
}

input {
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

input:focus {
  border-color: #c7a229;
  outline: none;
  box-shadow: 0 0 5px #c7a229;;
}

.delete-button {
  padding: 5px 10px;
  background-color: #ff4d4d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.delete-button:hover {
  background-color: #e60000;
}
.start-work-block{
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
.scrollable {
  max-height: 300px;
  overflow-y: auto;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
  display: flex;
  justify-content: space-evenly;
  flex-wrap: wrap;
  gap: 10px;
}
.worker {
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 5px;
  background-color: #ffffff;
  width: calc(33.33% - 10px);
  box-sizing: border-box;
}
.worker h4, .worker p {
  margin: 5px 0;
}
.user {
  border: 1px solid #ddd;
  padding: 10px;
  border-radius: 5px;
  background-color: #ffffff;
  width: calc(33.33% - 10px);
  box-sizing: border-box;
  text-align: center;
}
.user h4, .user p {
  margin: 5px 0;
}
textarea {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}
textarea:focus {
  border-color: #c7a229;
  outline: none;
  box-shadow: 0 0 5px #c7a229;
}
.modalselect{
  height: 65vh;
}
.product-image {
  width: 100%;
  height: auto;
  max-height: 150px;
  object-fit: cover;
  border-radius: 5px;
  margin-bottom: 10px;
}
</style>








