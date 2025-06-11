<template>
  <div class="shop-prof">
  <div class="container">
    <button class="btn back-btn" @click="goBack">Back to shop</button>
    <div class="shop-one">
      <h1 class="shop-name">Shop: {{ shop.name }}</h1>
      <div class="shop-head">
        <h2 class="shop-address">Address: {{ shop.location }}</h2>
        <h3 class="work-schedule">Work schedule: {{ shop.work_schedule }}</h3>
      </div>
      <div class="work-info">
        <button class="btn" @click="showPreviousSalesModal = true">Previous sales</button>
      </div>
      <div v-if="showPreviousSalesModal" class="modal-overlay">
        <div class="modal">
          <h3 class="modal-title">Sales for {{ todayDate }}</h3>
          <p class="total-sales"><strong>Total Sales Amount:</strong> {{ totalSalesAmount }} uah</p>
          <div class="receipt-list scrollable receipt-lista">
            <div v-for="receipt in salesReceipts" :key="receipt.id" class="receipt-item receipt-itema">
              <p class="receipt-id"><strong>Receipt ID:</strong> {{ receipt.id }}</p>
              <ul class="receipt-items">
                <li v-for="item in receipt.items" :key="item.product_id" class="receipt-item-detail">
                  <span class="item-name">{{ item.name }}</span> - 
                  <span class="item-quantity">Quantity: {{ item.quantity }}</span>, 
                  <span class="item-price">Price: {{ item.price }}</span>, 
                  <span class="item-total">Total: {{ item.total }}</span>
                </li>
              </ul>
              <p class="receipt-total"><strong>Receipt Total:</strong> {{ receipt.total }}</p>
            </div>
          </div>
          <button class="btn close-btn" @click="closePreviousSalesModal">Close</button>
        </div>
      </div>
      <div class="products-wrapper">
        <div class="products-inner">
          <h2 class="products-h">Products in checkbox</h2>
          <div class="btnCreate">
            <button class="btn" @click="showSelectModal = true">Add product to checkbox</button>
          </div>
          <div class="products">
          <div class="product" v-for="product in filteredProducts" :key="product.id">
            <img :src="product.image_url" alt="Product Image" class="product-image" />
            <h4 class="product-name">Name: {{ product.name }}</h4>
            <p class="product-description">Sale price: {{ product.sale_price }}</p>
            <p class="product-price">Purchase price: {{ product.purchase_price }}</p>
            <p class="product-quantity">Size weight: {{ product.size_weight }}</p>
            <p class="product-category">Producer: {{ product.producer }}</p>
            <p class="product-category">Quantity in stock: {{ product.quantity }}</p>
            <input 
              type="number" 
              v-model="product.count" 
              :min="1" 
              placeholder="Enter count" 
            />
            <button class="btn remove-btn" @click="removeFromCheckbox(product.supply_id)">Remove from checkbox</button>
          </div>
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
      </div>
      <div class="btnCreate">
        <button class="btn" style="margin: 20px 0px;" @click="showConfirmSaleModal = true">Confirm sale</button>
      </div>
      <div v-if="showConfirmSaleModal" class="modal-overlay">
        <div class="modal">
          <h3>Confirm Sale</h3>
          <div class="receipt">
            <div v-for="item in checkbox" :key="item.id" class="receipt-item width receipt-element receipt-item1">
              <p>{{ item.name }}</p>
              <p> {{ item.count }} x {{ item.sale_price }} </p>
              <p>total: {{ item.count * item.sale_price }}</p>
            </div>
            <hr />
            <p><strong>Total Amount: {{ totalAmount }}</strong></p>
          </div>
          <div class="payment-method">
            <label>
              <input type="radio" value="cash" v-model="paymentType" /> Cash
            </label>
            <label>
              <input type="radio" value="card" v-model="paymentType" /> Card
            </label>
          </div>
          <div>
            <button class="btn" @click="confirmSale">Confirm</button>
            <button class="btn" @click="closeConfirmSaleModal">Cancel</button>
          </div>
        </div>
      </div>
      <div v-if="showSelectModal" class="modal-overlay">
        <div class="modal1">
          <h3>Select Product to add to checkbox</h3>
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
            <div class="product" v-for="product in paginatedProducts" :key="product.id">
              <img :src="product.image_url" alt="Product Image" class="product-image" />
              <h4 class="product-name">Product name: {{ product.name }}</h4>
              <p class="product-description">Product sale price: {{ product.sale_price }}</p>
              <p class="product-price">Product purchase price: {{ product.purchase_price }}</p>
              <p class="product-quantity">Product size weight: {{ product.size_weight }}</p>
              <button @click="openQuantityModal(product)">Add to checkbox</button>
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
          <button class="btn" @click="closeModal">Close</button>
        </div>
      </div>

      <div v-if="showQuantityModal" class="modal-overlay">
        <div class="modal">
          <h3>Enter Quantity</h3>
          <input 
            type="number" 
            v-model="quantityInput" 
            min="1" 
            placeholder="Enter quantity" 
          />
          <div>
            <button class="btn" @click="confirmAddProduct">Confirm</button>
            <button class="btn" @click="closeQuantityModal">Cancel</button>
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
        this.$store.dispatch('fetchCategoriesByParent', 1);
        this.$store.dispatch('fetchReceipts', {shop_id});

    },
    data() {
        return {
            showModal: false,
            showSelectModal: false,
            showDeleteModal: false,
            showQuantityModal: false,
            showConfirmSaleModal: false,
            showPreviousSalesModal: false,
            confirmedProductId: null,
            quantityInput: 1,
            selectedProduct: null,
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
            selectedCategory: '',
            currentPage: 1,
            currentPageAdd: 1,
            itemsPerPage: 3,
            categoriesHistory: [{id: 1, name: 'All Products'}],
            checkbox: [],
            paymentType: 'cash',
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
        closeQuantityModal() {
          this.showQuantityModal = false;
          this.selectedProduct = null;
        },
        closeConfirmSaleModal() {
          this.showConfirmSaleModal = false;
        },
        closePreviousSalesModal() {
          this.showPreviousSalesModal = false;
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
        addProductToShop(product,count) {
            let p = {...product}
            p.count = count
            this.checkbox.push(p);
            this.showSelectModal = false;
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
        openQuantityModal(product) {
          this.selectedProduct = product;
          this.quantityInput = 1;
          this.showQuantityModal = true;
        },
        confirmAddProduct() {
          if (this.quantityInput > 0) {
            this.addProductToShop(this.selectedProduct, this.quantityInput);
            this.closeQuantityModal();
          }
        },
        confirmSale() {
          const shop_id = this.$route.params.id;
          const saleDetails = {
            products: this.checkbox,
            paymentType: this.paymentType,
            shop_id: shop_id,
          };
          this.$store.dispatch('confirmSale', saleDetails).then(() => {
            this.checkbox = []; // Clear the checkbox after confirming the sale
            this.closeConfirmSaleModal();
          });
        },
        goBack() {
          this.$router.go(-1); // Navigate to the previous page
        },
        removeFromCheckbox(productId) {
          this.checkbox = this.checkbox.filter(product => product.supply_id !== productId);
        },
    },
    computed: {
        selectedCategoryName() {
          return this.categoriesHistory[this.categoriesHistory.length - 1].name || 'All Products';
        },
        categories() {
            return this.$store.getters.getCategories;
        },
        salesReceipts() {
            return this.$store.getters.getReceipts;
        },
        shop() {
            return this.$store.getters.getShop;
        },
        products() {
            return this.$store.getters.getProducts || []; // Ensure it defaults to an empty array
        },
        paginatedProducts() {
            const filteredProducts = this.products.filter(product => {
                const isInCheckbox = this.checkbox.some(checkboxProduct => checkboxProduct.supply_id === product.supply_id);
                return !isInCheckbox && (this.searchQuery
                    ? product.name.toLowerCase().includes(this.searchQuery.toLowerCase())
                    : true);
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
            const filteredProducts = this.checkbox; // Ensure it defaults to an empty array
            return Math.ceil(filteredProducts.filter(product => {
                return this.searchQueryAdd
                    ? product.name.toLowerCase().includes(this.searchQueryAdd.toLowerCase())
                    : true;
            }).length / this.itemsPerPage)
        },
        filteredProducts() {
            let filteredProducts = this.checkbox; // Ensure it defaults to an empty array
            const start = (this.currentPageAdd - 1) * this.itemsPerPage;
            const end = start + this.itemsPerPage;
            return filteredProducts.slice(start, end);
        },
        totalAmount() {
          return this.checkbox.reduce((sum, item) => sum + item.count * item.sale_price, 0);
        },
        todayDate() {
          const today = new Date();
          return today.toLocaleDateString();
        },
        totalSalesAmount() {
          return this.salesReceipts.reduce((sum, receipt) => {
            return sum + receipt.items.reduce((itemSum, item) => itemSum + item.total, 0);
          }, 0);
        },
    },
    watch:{
      searchQuery() {
        this.currentPage = 1
      },
      searchQueryAdd() {
        this.currentPageAdd = 1
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
  padding: 30px;
  border-radius: 10px;
  width: 400px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.modal1{
  background: white;
  padding: 20px;
  border-radius: 5px;
  width: 60%;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
.modal h3 {
  font-size: 1.8em;
  margin-bottom: 20px;
  color: #333;
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
.modal input {
  margin: 10px 0;
  width: 80%;
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

.receipt {
  width: 100%;
  margin-bottom: 20px;
  text-align: left;
}
.width{
  width: 100% !important;
}
.receipt-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 1em;
  color: #555;
}
.receipt-item p {
  margin: 0;
}
hr {
  border: none;
  border-top: 1px solid #ddd;
  margin: 15px 0;
}
.payment-method {
  display: flex;
  justify-content: space-around;
  width: 100%;
  margin-bottom: 20px;
}
.payment-method label {
  font-size: 1em;
  color: #333;
  cursor: pointer;
}
.payment-method input {
  margin-right: 5px;
}
.modal button {
  width: 120px;
  padding: 10px;
  margin: 5px;
  background-color: #000000;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1em;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.modal button:hover {
  background-color: #c7a229;
}
.modal button:focus {
  outline: none;
  box-shadow: 0 0 5px #c7a229;
}
.scrollable {
  max-height: 300px;
  overflow-y: auto;
  padding-right: 10px;
}
.scrollable::-webkit-scrollbar {
  width: 8px;
}
.scrollable::-webkit-scrollbar-thumb {
  background-color: #c7a229;
  border-radius: 4px;
}
.scrollable::-webkit-scrollbar-thumb:hover {
  background-color: #a67c1a;
}
.modal-title {
  font-size: 1.5em;
  margin-bottom: 20px;
  text-align: center;
  color: #333;
}

.receipt-list {
  max-height: 300px;
  overflow-y: auto;
  padding: 10px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.receipt-item {
  margin-bottom: 20px;
  padding: 10px;
  background-color: #fff;
}

.receipt-id {
  font-weight: bold;
  margin-bottom: 10px;
}

.receipt-items {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.receipt-item-detail {
  margin-bottom: 5px;
  font-size: 0.9em;
  color: #555;
}

.item-name {
  font-weight: bold;
}

.item-quantity, .item-price, .item-total {
  margin-left: 5px;
}

.receipt-total {
  font-weight: bold;
  margin-top: 10px;
  text-align: right;
}

.receipt-divider {
  border: none;
  border-top: 1px solid #ddd;
  margin: 10px 0;
}

.close-btn {
  display: block;
  margin: 20px auto 0;
  padding: 10px 20px;
  background-color: #c7a229;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
}

.close-btn:hover {
  background-color: #a67c1a;
}
.total-sales {
  font-size: 1.2em;
  margin-bottom: 15px;
  text-align: center;
  color: #444;
}
.back-btn {
  margin-top: 10px;
}

.back-btn:hover {
  background-color: #a67c1a;
}
.receipt-element{
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.receipt-item1{
  width: 100% !important;
}
.remove-btn {
  margin-top: 10px;
  padding: 5px 10px;
  background-color: #ff4d4d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.remove-btn:hover {
  background-color: #e60000;
}
</style>