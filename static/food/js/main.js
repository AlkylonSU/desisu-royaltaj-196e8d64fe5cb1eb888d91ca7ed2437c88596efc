var hours = 24;
var now = new Date().getTime();
var stepTime = localStorage.getItem('stepTime');

if (stepTime == null){
    localStorage.setItem('stepTime', now);
}
else{
    if(now - stepTime > hours*60*60*1000){
        localStorage.clear();
        localStorage.setItem('stepTime', now);
    }
}

var orders = JSON.parse(localStorage.getItem('orders'));
var total = localStorage.getItem('total');

if (orders === null || orders === undefined){
    localStorage.setItem('orders', JSON.stringify([]));
    orders = JSON.parse(localStorage.getItem('orders'));
}

if (total === null || total === undefined){
    localStorage.setItem('total', 0);
    total = JSON.parse(localStorage.getItem('total'));
}

var cart = document.querySelector('#cart');
cart.innerHTML = orders.length;

fetch('/food/api/get_orders_received_today/')
  .then(response => response.json())
  .then(data => {
    const ordersContainer = document.getElementById('todays-orders');
    const orders = JSON.parse(data);
    const totalOrders = orders.length;

    if (totalOrders === 0) {
      ordersContainer.innerHTML = '<h2 style="color: rgb(20, 23, 216);">No orders today</h2>';
    } else {
      let totalBill = 0; // Initialize total bill to 0
      const ordersHtml = orders.map(order => {
        const customer = order.fields.customer;
        const orderTotal = parseFloat(order.fields.total);
        totalBill += orderTotal; // Add order total to the total bill
        //return `<p>${customer} - ${orderTotal}</p>`;
      });
      console.log("ORDER OUT CALLED")
      if (totalBill >= 1000) {
        // Make an AJAX call to confirm_orders view
        console.log("ORDER CALLED")
        confirmOrders(totalBill, orders);
      }

      // Adjust text size based on screen width
      const screenWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
      let fontSize = '16px'; // Default font size

      if (screenWidth <= 768) {
        // Adjust font size for smaller screens
        fontSize = '10px';
      }

      ordersContainer.innerHTML = `<h2 style="color: rgb(20, 23, 216); font-size: ${fontSize};">Total orders today: ${totalOrders} </h2> <br> <h2 style="color: rgb(20, 23, 216); font-size: ${fontSize};"> Total bill today: ${totalBill.toFixed(2)} / 1000</h2>` + ordersHtml.join('');

    }
  });



  function confirmOrders(totalBill, orders) {
    // Prepare the data to send to the view
    const data = {
        totalBill: totalBill,
        orders: orders
    };

    // Make an AJAX request to confirm_orders view
    console.log("ORDER FUNCTION CALLED")
    fetch('/food/api/confirm_orders/')
    .then(response => response.json())
    .then(result => {
        // Handle the result as needed
        console.log(result);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


