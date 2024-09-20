var nam = document.querySelector("#name");
var price = document.querySelector("#price");
var bill = document.querySelector("#total");
var rm = document.querySelector("#rm");

function shoppingCart() {
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;

    // Add a delivery fee of 10 to the total
    var deliveryFee = 15;
    total = parseFloat(total);
    totaldisplay = total + deliveryFee;
    // Create a table structure
    var table = '<table class="table">';
    table += '<thead><tr><th>Name</th><th>Price</th><th>Action</th></tr></thead>';
    table += '<tbody>';

    for (let i = 0; i < cartSize; i++) {
        table += '<tr>';
        table += '<td>' + orders[i][0] + '</td>';
        table += '<td>' + orders[i][1] + '</td>';
        table += '<td><button class="btn btn-danger rounded" onclick="removeItem(' + i + ')">X</button></td>';
        table += '</tr>';
    }

    table += '</tbody>';
    table += '</table>';

    // Set the innerHTML of the container to the table
    document.getElementById('cartContainer').innerHTML = table;

    // Display total with delivery fee
    bill.innerHTML = '<h3 class="pt-3" style="text-align: center;">Total: ' + totaldisplay.toFixed(2) + ' TL </h3>';
    var submitButton = document.getElementById('submitBtn');
    if (totaldisplay == deliveryFee) {
        submitButton.disabled = true;
    }
}


shoppingCart();


function removeItem(n){
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    total = Number(total) - Number(orders[n][1]);
    orders.splice(n, 1);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;

    localStorage.setItem('orders', JSON.stringify(orders));
    localStorage.setItem('total', total);
    shoppingCart();
}

var note = document.querySelector('#message');
var dorm = document.querySelector('#address')

function order() {
    var submitButton = document.getElementById('submitBtn');

    var msg = note.value;
    var orders = localStorage.getItem('orders');
    var total = localStorage.getItem('total');
    var address = dorm.value;

    if (address.trim() === '') {
        alert("Address is required.");
        return;
    }

    // Check the current time
    var currentTime = new Date();

    var currentDay = currentTime.getDay();
    var currentHour = currentTime.getHours();

    // Check if it's not Sunday, Tuesday, or Thursday (0, 2, 4)

    if (currentHour < 9 || currentHour >= 17) {
        //alert("Orders can only be placed between 9 am and 5 pm.");
        //return;
    }

    // Make an AJAX call to check the wallet balance
    if (submitButton) {
        submitButton.disabled = true;
    }

    $.ajax({
        url: '/food/check_wallet_balance/',
        type: 'GET',
        success: function(data) {
            var walletString = data.walletAmount;
            var walletAmount = parseFloat(walletString);

            // Check if the wallet has enough balance
            if (walletAmount >= 0) {
                // Wallet has enough balance, proceed with the order
                var ur = '/food/order';

                var orderData = {
                    'orders': orders,
                    'note': msg,
                    'total': total,
                    'address': address,
                };

                console.log(orderData);

                $.ajax({
                    url: ur,
                    type: 'POST',
                    data: orderData,
                    success: function(data) {
                        // Check the status in the response
                        if (data.status === 'Order placed successfully') {
                            window.location.replace('/food/success');
                            localStorage.setItem('orders', JSON.stringify([]));
                            localStorage.setItem('total', 0);
                        } else if (data.status === 'Invalid campus for the current day') {
                            alert("Invalid campus for the current day");
                        } else {
                            alert("Invalid campus for the current day. Orders to Ozygein are only available on Monday, Wednesday, and Friday. Orders to Sabanci are only available on Tuesday and Thursday and Saturday.");
                        }
                    },
                    error: function(error) {
                        console.error("Error:", error);
                        alert("An error occurred. Please try again later.");
                    }
                });
            } else {
                alert("Insufficient wallet balance. Please add funds to your wallet.");
            }
        },
        error: function(error) {
            console.error("Error:", error);
            alert("An error occurred. Please try again later.");
        }
    });
}
