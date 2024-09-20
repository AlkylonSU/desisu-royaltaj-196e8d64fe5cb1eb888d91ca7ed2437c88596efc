var rcart = document.querySelector('#rcart');
var rtotal = document.querySelector('#rtotal');

//ADD RICE

function addRice(rid) {
    rtId = '#rt' + rid;
    var name = document.querySelector(rtId).innerHTML;
    var foodSpice = document.querySelector('input[name="riceSpice' + rid + '"]:checked').value;
    name += '(' + foodSpice + ' spice)';
    rpId = '#rp' + rid;
    var price = document.querySelector(rpId).innerHTML;
    console.log(Number(price));
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;

    orders[cartSize] = [name, price];
    localStorage.setItem('orders', JSON.stringify(orders));

    total = Number(total) + Number(price);
    localStorage.setItem('total', total);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;
    console.log(total);

    // Display the notification
    var notification = document.getElementById('notification');
    notification.innerText = name + ' has been added to your cart.';
    notification.style.display = 'block';

    // Hide the notification after a few seconds (e.g., 3 seconds)
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}

function addChicken(cmid) {
    cmtId = '#cmt' + cmid;
    var name = document.querySelector(cmtId).innerHTML;

    // Get the selected food option (roti or rice)
    var foodOption = document.querySelector('input[name="chickenOption' + cmid + '"]:checked').value;
    var foodSpice = document.querySelector('input[name="chickenSpice' + cmid + '"]:checked').value;
    // Concatenate the selected option to the name
    name += ' with ' + foodOption + ' (' + foodSpice + ' spice)';

    cmpId = '#cmp' + cmid;

    var price = document.querySelector(cmpId).innerHTML;
    console.log(Number(price));
    var orders = JSON.parse(localStorage.getItem('orders')) || [];
    var total = localStorage.getItem('total') || 0;
    var cartSize = orders.length;

    orders[cartSize] = [name, price];
    localStorage.setItem('orders', JSON.stringify(orders));

    total = Number(total) + Number(price);
    localStorage.setItem('total', total);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;
    console.log(total);

    // Display the notification
    var notification = document.getElementById('notification');
    notification.innerText = name + ' has been added to your cart.';
    notification.style.display = 'block';

    // Hide the notification after a few seconds (e.g., 3 seconds)
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}


function addMuttonBeef(mbid) {
    mbtId = '#mbt' + mbid;
    var name = document.querySelector(mbtId).innerHTML;

    mbpId = '#mbp' + mbid;
    console.log("mbtId:", mbtId);
    console.log("mbpId:", mbpId);

    var price = document.querySelector(mbpId).innerHTML;
    console.log(Number(price));
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;

    orders[cartSize] = [name, price];
    localStorage.setItem('orders', JSON.stringify(orders));

    total = Number(total) + Number(price);
    localStorage.setItem('total', total);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;
    console.log(total);

    // Display the notification
    var notification = document.getElementById('notification');
    notification.innerText = name + ' has been added to your cart.';
    notification.style.display = 'block';

    // Hide the notification after a few seconds (e.g., 3 seconds)
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}

function addBBQ(bbqid) {
    bbqtId = '#bbqt' + bbqid;
    var name = document.querySelector(bbqtId).innerHTML;

    bbqpId = '#bbqp' + bbqid;
    console.log("bbqtId:", bbqtId);
    console.log("bbqpId:", bbqpId);

    var price = document.querySelector(bbqpId).innerHTML;
    console.log(Number(price));
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;

    orders[cartSize] = [name, price];
    localStorage.setItem('orders', JSON.stringify(orders));

    total = Number(total) + Number(price);
    localStorage.setItem('total', total);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;
    console.log(total);

    // Display the notification
    var notification = document.getElementById('notification');
    notification.innerText = name + ' has been added to your cart.';
    notification.style.display = 'block';

    // Hide the notification after a few seconds (e.g., 3 seconds)
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}

function addSaute(sid) {
    stId = '#st' + sid;
    var name = document.querySelector(stId).innerHTML;

    spId = '#sp' + sid;

    var price = document.querySelector(spId).innerHTML;
    console.log(Number(price));
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;

    orders[cartSize] = [name, price];
    localStorage.setItem('orders', JSON.stringify(orders));

    total = Number(total) + Number(price);
    localStorage.setItem('total', total);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;
    console.log(total);

    // Display the notification
    var notification = document.getElementById('notification');
    notification.innerText = name + ' has been added to your cart.';
    notification.style.display = 'block';

    // Hide the notification after a few seconds (e.g., 3 seconds)
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}

function addRoti(rotiid) {
    rotitId = '#rotit' + rotiid;
    var name = document.querySelector(rotitId).innerHTML;

    rotipId = '#rotip' + rotiid;
    console.log("rotitId:", rotitId);
    console.log("rotipId:", rotipId);

    var price = document.querySelector(rotipId).innerHTML;
    console.log(Number(price));
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;

    orders[cartSize] = [name, price];
    localStorage.setItem('orders', JSON.stringify(orders));

    total = Number(total) + Number(price);
    localStorage.setItem('total', total);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;
    console.log(total);

    // Display the notification
    var notification = document.getElementById('notification');
    notification.innerText = name + ' has been added to your cart.';
    notification.style.display = 'block';

    // Hide the notification after a few seconds (e.g., 3 seconds)
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}

function addBurger(bid) {
    btId = '#bt' + bid;
    var name = document.querySelector(btId).innerHTML;

    bpId = '#bp' + bid;

    var price = document.querySelector(bpId).innerHTML;
    console.log(Number(price));
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;

    orders[cartSize] = [name, price];
    localStorage.setItem('orders', JSON.stringify(orders));

    total = Number(total) + Number(price);
    localStorage.setItem('total', total);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;
    console.log(total);

    // Display the notification
    var notification = document.getElementById('notification');
    notification.innerText = name + ' has been added to your cart.';
    notification.style.display = 'block';

    // Hide the notification after a few seconds (e.g., 3 seconds)
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}

function addRoll(roid) {
    rotId = '#rot' + roid;
    var name = document.querySelector(rotId).innerHTML;

    ropId = '#rop' + roid;

    var price = document.querySelector(ropId).innerHTML;
    console.log(Number(price));
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;

    orders[cartSize] = [name, price];
    localStorage.setItem('orders', JSON.stringify(orders));

    total = Number(total) + Number(price);
    localStorage.setItem('total', total);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;
    console.log(total);

    // Display the notification
    var notification = document.getElementById('notification');
    notification.innerText = name + ' has been added to your cart.';
    notification.style.display = 'block';

    // Hide the notification after a few seconds (e.g., 3 seconds)
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}

function addChinese(chid) {
    chtId = '#cht' + chid;
    var name = document.querySelector(chtId).innerHTML;

    chpId = '#chp' + chid;

    var price = document.querySelector(chpId).innerHTML;
    console.log(Number(price));
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;

    orders[cartSize] = [name, price];
    localStorage.setItem('orders', JSON.stringify(orders));

    total = Number(total) + Number(price);
    localStorage.setItem('total', total);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;
    console.log(total);

    // Display the notification
    var notification = document.getElementById('notification');
    notification.innerText = name + ' has been added to your cart.';
    notification.style.display = 'block';

    // Hide the notification after a few seconds (e.g., 3 seconds)
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}

function addDurum(durumid) {
    durumtId = '#durumt' + durumid;
    var name = document.querySelector(durumtId).innerHTML;

    durumpId = '#durump' + durumid;

    var price = document.querySelector(durumpId).innerHTML;
    console.log(Number(price));
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;

    orders[cartSize] = [name, price];
    localStorage.setItem('orders', JSON.stringify(orders));

    total = Number(total) + Number(price);
    localStorage.setItem('total', total);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;
    console.log(total);

    // Display the notification
    var notification = document.getElementById('notification');
    notification.innerText = name + ' has been added to your cart.';
    notification.style.display = 'block';

    // Hide the notification after a few seconds (e.g., 3 seconds)
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}

function addStarter(starterid) {
    startertId = '#startert' + starterid;
    var name = document.querySelector(startertId).innerHTML;

    starterpId = '#starterp' + starterid;

    var price = document.querySelector(starterpId).innerHTML;
    console.log(Number(price));
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;

    orders[cartSize] = [name, price];
    localStorage.setItem('orders', JSON.stringify(orders));

    total = Number(total) + Number(price);
    localStorage.setItem('total', total);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;
    console.log(total);

    // Display the notification
    var notification = document.getElementById('notification');
    notification.innerText = name + ' has been added to your cart.';
    notification.style.display = 'block';

    // Hide the notification after a few seconds (e.g., 3 seconds)
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}

function addVeg(vegid) {
    vegtId = '#vegt' + vegid;
    var name = document.querySelector(vegtId).innerHTML;
    var foodOption = document.querySelector('input[name="vegOption' + vegid + '"]:checked').value;
    var foodSpice = document.querySelector('input[name="vegSpice' + vegid + '"]:checked').value;

    // Concatenate the selected option to the name
    name += ' with ' + foodOption + ' (' + foodSpice + ' spice)';

    vegpId = '#vegp' + vegid;

    var price = document.querySelector(vegpId).innerHTML;
    console.log(Number(price));
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;

    orders[cartSize] = [name, price];
    localStorage.setItem('orders', JSON.stringify(orders));

    total = Number(total) + Number(price);
    localStorage.setItem('total', total);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;
    console.log(total);

    // Display the notification
    var notification = document.getElementById('notification');
    notification.innerText = name + ' has been added to your cart.';
    notification.style.display = 'block';

    // Hide the notification after a few seconds (e.g., 3 seconds)
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}

function addSoup(soupid) {
    souptId = '#soupt' + soupid;
    var name = document.querySelector(souptId).innerHTML;

    souppId = '#soupp' + soupid;

    var price = document.querySelector(souppId).innerHTML;
    console.log(Number(price));
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;

    orders[cartSize] = [name, price];
    localStorage.setItem('orders', JSON.stringify(orders));

    total = Number(total) + Number(price);
    localStorage.setItem('total', total);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;
    console.log(total);

    // Display the notification
    var notification = document.getElementById('notification');
    notification.innerText = name + ' has been added to your cart.';
    notification.style.display = 'block';

    // Hide the notification after a few seconds (e.g., 3 seconds)
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}

function addSalads(saladid) {
    saladtId = '#saladt' + saladid;
    var name = document.querySelector(saladtId).innerHTML;

    saladpId = '#saladp' + saladid;

    var price = document.querySelector(saladpId).innerHTML;
    console.log(Number(price));
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;

    orders[cartSize] = [name, price];
    localStorage.setItem('orders', JSON.stringify(orders));

    total = Number(total) + Number(price);
    localStorage.setItem('total', total);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;
    console.log(total);

    // Display the notification
    var notification = document.getElementById('notification');
    notification.innerText = name + ' has been added to your cart.';
    notification.style.display = 'block';

    // Hide the notification after a few seconds (e.g., 3 seconds)
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}


function addDrink(drinkid) {
    drinktId = '#drinkt' + drinkid;
    var name = document.querySelector(drinktId).innerHTML;

    drinkpId = '#drinkp' + drinkid;

    var price = document.querySelector(drinkpId).innerHTML;
    console.log(Number(price));
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;

    orders[cartSize] = [name, price];
    localStorage.setItem('orders', JSON.stringify(orders));

    total = Number(total) + Number(price);
    localStorage.setItem('total', total);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;
    console.log(total);

    // Display the notification
    var notification = document.getElementById('notification');
    notification.innerText = name + ' has been added to your cart.';
    notification.style.display = 'block';

    // Hide the notification after a few seconds (e.g., 3 seconds)
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}

function addSweet(sweetid) {
    sweettId = '#sweett' + sweetid;
    var name = document.querySelector(sweettId).innerHTML;

    sweetpId = '#sweetp' + sweetid;

    var price = document.querySelector(sweetpId).innerHTML;
    console.log(Number(price));
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;

    orders[cartSize] = [name, price];
    localStorage.setItem('orders', JSON.stringify(orders));

    total = Number(total) + Number(price);
    localStorage.setItem('total', total);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;
    console.log(total);

    // Display the notification
    var notification = document.getElementById('notification');
    notification.innerText = name + ' has been added to your cart.';
    notification.style.display = 'block';

    // Hide the notification after a few seconds (e.g., 3 seconds)
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}

function addAddon(addonid) {
    addontId = '#addont' + addonid;
    var name = document.querySelector(addontId).innerHTML;

    addonpId = '#addonp' + addonid;

    var price = document.querySelector(addonpId).innerHTML;
    console.log(Number(price));
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;

    orders[cartSize] = [name, price];
    localStorage.setItem('orders', JSON.stringify(orders));

    total = Number(total) + Number(price);
    localStorage.setItem('total', total);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;
    console.log(total);

    // Display the notification
    var notification = document.getElementById('notification');
    notification.innerText = name + ' has been added to your cart.';
    notification.style.display = 'block';

    // Hide the notification after a few seconds (e.g., 3 seconds)
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}

function addRamadan(ramadanid) {
    ramadantId = '#ramadant' + ramadanid;
    var name = document.querySelector(ramadantId).innerHTML;
    var chatOption = document.querySelector('input[name="chatChoice' + ramadanid + '"]:checked').value;
    var drinkOption = document.querySelector('input[name="drinkChoice' + ramadanid + '"]:checked').value;

    // Concatenate the selected option to the name
    name += ' : ' + chatOption + ' and ' + drinkOption;

    ramadanpId = '#ramadanp' + ramadanid;

    var price = document.querySelector(ramadanpId).innerHTML;
    console.log(Number(price));
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;

    orders[cartSize] = [name, price];
    localStorage.setItem('orders', JSON.stringify(orders));

    total = Number(total) + Number(price);
    localStorage.setItem('total', total);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;
    console.log(total);

    // Display the notification
    var notification = document.getElementById('notification');
    notification.innerText = name + ' has been added to your cart.';
    notification.style.display = 'block';

    // Hide the notification after a few seconds (e.g., 3 seconds)
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}



function addPasta(pastaid) {
    pastatId = '#pastat' + pastaid;
    var name = document.querySelector(pastatId).innerHTML;

    pastapId = '#pastap' + pastaid;

    var price = document.querySelector(pastapId).innerHTML;
    console.log(Number(price));
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;

    orders[cartSize] = [name, price];
    localStorage.setItem('orders', JSON.stringify(orders));

    total = Number(total) + Number(price);
    localStorage.setItem('total', total);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;
    console.log(total);

    // Display the notification
    var notification = document.getElementById('notification');
    notification.innerText = name + ' has been added to your cart.';
    notification.style.display = 'block';

    // Hide the notification after a few seconds (e.g., 3 seconds)
    setTimeout(function() {
        notification.style.display = 'none';
    }, 3000);
}



function rshoppingCart() {
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    var cartSize = orders.length;
    rcart.innerHTML = '';
    for(let i = 0; i < cartSize; i++){
        btn = '<div class="del" onclick="removeRice(' + i + ')">x</div>';
        rcart.innerHTML += '<li>' + orders[i][0] + ' ' + orders[i][1] + btn + '</li>';
    }
    rtotal.innerHTML = 'Total: ' + total + ' TL';
}

rshoppingCart();

function removeRice(n){
    var orders = JSON.parse(localStorage.getItem('orders'));
    var total = localStorage.getItem('total');
    total = Number(total) - Number(orders[n][1]);
    orders.splice(n, 1);

    var cart = document.querySelector('#cart');
    cart.innerHTML = orders.length;

    localStorage.setItem('orders', JSON.stringify(orders));
    localStorage.setItem('total', total);
    rshoppingCart();
}