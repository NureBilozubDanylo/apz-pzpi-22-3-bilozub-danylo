<template>
    <div class="shop-stats">
      <div class="container">
          <button class="btn back-btn" @click="goBack">Back to shop</button>
          <h1 class="shop-name">Shop: {{ shop.name }}</h1>
          <div class="shop-head">
              <h2 class="shop-address">Address: {{ shop.location }}</h2>
              <h3 class="work-schedule">Work schedule: {{ shop.work_schedule }}</h3>
          </div>
          
          <div class="stats-block">
            <div class="dropdown">
              <label for="stats-select">Select Statistics:</label>
              <select id="stats-select" v-model="selectedStat" @change="updateDisplayedStat">
                <option value="day">Statistic per day</option>
                <option value="customers">Customers</option>
                <option value="ratings">Ratings</option>
              </select>
            </div>
            <div class="stats-content">
              <div v-if="selectedStat === 'day'">
                <h4>Daily Statistics</h4>
                <div class="date-picker">
                  <label for="date-select">Select Date:</label>
                  <input type="date" id="date-select" v-model="selectedDate" @change="fetchDailyStats" />
                </div>
                <div class="sales-summary">
                  <h3>Sales for {{ selectedDate }}</h3>
                  <div v-if="stats.length > 0">
                    <p class="total-sales"><strong>Total Sales Amount:</strong> {{ totalSales }}</p>
                    <p class="total-sales-count"><strong>Total Sales Count:</strong> {{ stats.length }}</p>
                    <p class="total-profit"><strong>Total Profit:</strong> {{ totalProfit }}</p>
                    <div class="receipt-list scrollable">
                      <div v-for="receipt in stats" :key="receipt.id" class="receipt-item receipt-itema">
                        <p class="receipt-id"><strong>Receipt ID:</strong> {{ receipt.id }}</p>
                        <ul class="receipt-items">
                          <li v-for="item in receipt.items" :key="item.product_id" class="receipt-item-detail">
                            <span class="item-name">{{ item.name }}</span> - 
                            <span class="item-quantity">Quantity: {{ item.quantity }}</span>, 
                            <span class="item-price">Price: {{ item.price }}</span>, 
                            <span class="item-purchase-price">Purchase Price: {{ item.purchase_price }}</span>, 
                            <span class="item-total">Total: {{ item.total }}</span>, 
                            <span class="item-profit">Profit: {{ item.quantity * (item.price - item.purchase_price) }}</span>
                          </li>
                        </ul>
                        <p class="receipt-total receipt-totala"><strong>Receipt Total:</strong> {{ receipt.total }}</p>
                        <p class="receipt-profit"><strong>Receipt Profit:</strong> {{ receipt.items.reduce((sum, item) => sum + item.quantity * (item.price - item.purchase_price), 0) }}</p>
                      </div>
                    </div>
                  </div>
                  <div v-else>
                    <p class="no-sales-message">No sales data available for the selected date.</p>
                  </div>
                </div>
              </div>
              <div v-if="selectedStat === 'customers'">
                <h4>Customer Statistics</h4>
                <!-- Add customer statistics content here -->
              </div>
              <div v-if="selectedStat === 'ratings'">
                <h4>Ratings Statistics</h4>
                <!-- Add ratings statistics content here -->
              </div>
            </div>
          </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ShopStats',
    data() {
      return {
        selectedStat: 'day',
        selectedDate: new Date().toISOString().split('T')[0], // Default to today's date
      };
    },
    created() {
      const shop_id = this.$route.params.id;
      this.$store.dispatch('fetchShopById', shop_id);
      this.fetchDailyStats(); // Fetch stats for the default date
    },
    computed: {
      shop() {
        return this.$store.getters.getShop;
      },
      stats() {
        return this.$store.getters.getShopStats || []; // Ensure stats is always an array
      },
      totalSales() {
        return this.stats.reduce((sum, receipt) => sum + receipt.total, 0); // Calculate total sales amount
      },
      totalProfit() {
        return this.stats.reduce((sum, receipt) => {
          return sum + receipt.items.reduce((itemSum, item) => itemSum + item.quantity * (item.price - item.purchase_price), 0);
        }, 0);
      },
    },
    methods: {
      goBack() {
        this.$router.push({ name: 'shop', params: { id: this.shop.id } });
      },
      updateDisplayedStat() {
        // Logic to update displayed statistics based on selectedStat
      },
      fetchDailyStats() {
        const shop_id = this.$route.params.id;
        this.$store.dispatch('fetchShopStats', { shop_id, date: this.selectedDate });
      },
    },
  };
  </script>
  
  <style>
  .shop-stats {
    padding: 20px;
    text-align: center;
  }
  .shop-name, .shop-address, .work-schedule {
    text-align: center;
    margin-bottom: 10px;
  }
  .stats-block {
    margin-top: 20px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
  }
  .dropdown {
    margin-bottom: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
  #stats-select {
    padding: 12px 25px;
    border-radius: 15px;
    border: 1px solid #ccc;
    width: 200px;
    margin-top: 10px;
  }
  .stats-content {
    text-align: center;
    margin-bottom: 10px;
  }
  .stats-content h4 {
    margin-bottom: 10px;
  }
  .date-picker {
    margin-bottom: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
  #date-select {
    padding: 10px;
    border-radius: 8px;
    border: 1px solid #ccc;
    margin-top: 10px;
  }
  .sales-summary {
    margin-top: 20px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
    text-align: center;
  }
  .sales-summary h3 {
    font-size: 1.5em;
    margin-bottom: 20px;
  }
  .total-sales, .total-sales-count {
    font-size: 1.2em;
    margin-bottom: 10px;
  }
  .receipt-list {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    gap: 15px;
    max-height: 300px;
    overflow-y: auto;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #fff;
  }
  .receipt-item {
    width: 30%;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 10px;
    background: #fff;
  }
  .receipt-item-detail {
    font-size: 0.9em;
    margin-bottom: 5px;
  }
  .receipt-total {
    font-weight: bold;
    margin-top: 10px;
  }
  .receipt-profit {
    font-weight: bold;
    margin-top: 10px;
  }
  .close-btn {
    margin-top: 20px;
    padding: 10px 20px;
    background: #007bff;
    color: #fff;
    border: none;
    border-radius: 8px;
    cursor: pointer;
  }
  .close-btn:hover {
    background: #0056b3;
  }
  .no-sales-message {
    font-size: 1.2em;
    color: #ff0000;
    margin-top: 20px;
  }
  </style>
