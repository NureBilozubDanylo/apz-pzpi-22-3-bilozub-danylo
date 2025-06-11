// orderSubject.js
class OrderSubject {
    constructor() {
        this.observers = [];
        this.orders = {};
    }

    addObserver(observer) {
        this.observers.push(observer);
    }

    removeObserver(observer) {
        this.observers = this.observers.filter(obs => obs !== observer);
    }

    notify(data) {
        this.observers.forEach(observer => observer.update(data));
    }

    updateOrderStatus(orderId, status) {
        this.orders[orderId] = status;
        this.notify({ orderId, status });
    }
}

// observers.js
class CustomerOrderObserver {
    constructor(customerName) {
        this.customerName = customerName;
    }

    update(data) {
        console.log(`${this.customerName}: Статус замовлення ${data.orderId} змінено на "${data.status}"`);
    }
}

class LogisticsObserver {
    update(data) {
        console.log(`Логістика: Оновлено статус замовлення ${data.orderId} - ${data.status}`);
    }
}

// main.js
const orderSubject = new OrderSubject();

const customer = new CustomerOrderObserver("Андрій");
const logistics = new LogisticsObserver();

orderSubject.addObserver(customer);
orderSubject.addObserver(logistics);

orderSubject.updateOrderStatus("order001", "Відправлено");