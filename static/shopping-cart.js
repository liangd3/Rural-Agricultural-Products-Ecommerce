const cardInputCardHTML = `
<h2>Payment Detail</h2>
<div class="card row card p-4 mt-4 mb-4">
    <div class="col-lg-9 col-md-9 col-12">
        <div class="form-group">
            <label>Card Number</label>
            <input type="tel" name="card_number" id="card-number" 
            inputmode="numeric" pattern="[0-9\s]{15,19}" 
            autocomplete="cc-number" maxlength="19" 
            placeholder="xxxx xxxx xxxx xxxx" required>
        </div>
    </div>
    <div class="col-lg-3 col-md-3 col-12">
        <div class="form-group">
            <label>CVV Number</label>
            <input type="number" name="card_cvv" id="card-cvv" 
            type="tel" inputmode="numeric" pattern="[0-9\s]{15,19}"
            maxlength="4" placeholder="xxx" required>
        </div>
    </div>
    <div class="col-lg-2 col-md-2 col-12">
        <div class="form-group">
            <label>Expiry Date</label>
            <input type="number" name="card_month" id="card-month" 
            type="tel" inputmode="numeric" pattern="[0-9\s]{2}"
            maxlength="2" min="0" max="12" maplaceholder="MM" required>
            <span>/</span>
            <input type="number" name="card_year" id="card-year" 
            type="tel" inputmode="numeric" pattern="[0-9\s]{2}"
            maxlength="2" min=24" max="99" maplaceholder="YY" required>
        </div>
    </div>
    <div class="col-lg-2 col-md-2 col-12">
        <div class="form-group">
            <label>Name</label>
            <input type="text" name="card_name" id="card-name" required>
        </div>
    </div>
</div>
`
function messagePrompter(category, message) {
    var toastContainer = document.getElementById('toastContainerFlash');
  
      var category = category, content = message;
      // Define background classes based on message category
      var bgClass = category === 'success' ? 'bg-success text-white' : 
                    category === 'danger' ? 'bg-danger text-white' : 
                    category === 'warning' ? 'bg-warning' : 
                    'bg-primary text-white'; // Default case
  
      var toastHtml = `
        <div class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-bs-autohide="true" data-bs-delay="5000">
          <div class="toast-header">
            <strong class="me-auto">Notification</strong>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
          </div>
          <div class="toast-body ${bgClass}">
            ${content}
          </div>
        </div>
      `;
      console.log(content)

      toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    
    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    var toastList = toastElList.map(function(toastEl) {
      return new bootstrap.Toast(toastEl).show();
    });
  };


async function getTotalQty() {
    const response = await fetch('/customer/shopping_cart/totalQty', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    });

    if (response.ok) {
        const totalQty = await response.json();
            const targetElement = document.getElementById('total-count');
            const countInCart = document.getElementById('total-count-in-cart');

            if (totalQty == null){ 
                document.getElementById('total-count').hidden = true;
                targetElement.innerHTML = "0";
                countInCart.innerHTML = `0 Items`;
            } else {
                document.getElementById('total-count').hidden = false;
                targetElement.innerHTML = totalQty;
                countInCart.innerHTML = `${totalQty} Items`;
            }
    } else {
        alert('Failed to update total quantity.');
    }
}

async function addToCart(name, id, qty) {
    const productID = id;
    const quantity = qty;
    const cartQty = document.getElementById("product-"+productID+"-cart");
    const minusBtn = document.getElementById("product-"+productID+"-minus");

    const response = await fetch('/customer/product/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_id: productID, qty: quantity }),
    });
    getTotalQty();
    cartCalculation();

    if (response.ok) {
        const updatedQty = await response.json();
        if (updatedQty == "Item out of stock.") {
            alert(updatedQty);
        } else {
            if (cartQty){
                const qtyInput = cartQty;
                qtyInput.value = updatedQty;
            };
            if (quantity > 0) {
                messagePrompter('success', `${name} x ${quantity} added to cart.`);
            } else {
                messagePrompter('warning', `${name} x ${quantity} deleted from cart.`);
            }
            if (cartQty.value == 1){
                minusBtn.setAttribute("disabled", "disabled");
            }
            else {
                minusBtn.removeAttribute("disabled");
            }
        
        }
    } else {
        alert('Failed to update quantity.');
    }
}

async function updateQty(name, id, qty) {
    const productID = id;
    const quantity = qty;
    const cartID = "product-"+productID+"-cart";
    const minusBtn = document.getElementById("product-"+productID+"-minus");

    const response = await fetch('/customer/cart/product/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_id: productID, qty: quantity }),
    });
    getTotalQty();
    cartCalculation();

    if (response.ok) {
        const updatedQty = await response.json();
        const qtyInput = document.getElementById(cartID);
        if (qtyInput){   
            qtyInput.value = updatedQty;
            var message = `Quantity of ${name} updated to ${quantity}.`;
            messagePrompter('success', message);
            if (quantity > 0) {
                messagePrompter('success', `${name} x ${quantity} added to cart.`);
            } else {
                messagePrompter('warning', `${name} x ${quantity} deleted from cart.`);
            };
            if (qtyInput.value == 1){
                minusBtn.setAttribute("disabled", "disabled");
            }
            else {
                minusBtn.removeAttribute("disabled");
            }
        };
    } else {
        alert('Failed to update quantity.');
    }
}

async function updateCartOverview() {
    const response = await fetch('/customer/cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    });
    let nf = new Intl.NumberFormat('en-US');


    if (response.ok) {
        const products = await response.json();
        const list = document.getElementById('shopping-list');
        var totalCost = 0;
        list.innerHTML = '';

        getTotalQty();

        products.forEach(product => {
            const listElement = document.createElement('li');

            if (product['discounted_price'] > 0) {
                listElement.innerHTML = `
                <a class="cart-img" href="/product/${product['product_id']}"><img src="/blueprints/static/product_image/${product['product_image']}" alt="https://via.placeholder.com/70x70"></a>
                <h4><a href="/product/${product['product_id']}">${product['product_name']}</a></h4>
                <p class="quantity">${product['qty']} x - <span class="amount text-decoration-line-through">$${product['product_price']}</span><span class="amount text-danger">$${product['discounted_price']}</span></p>
                `;
                totalCost += product['discounted_price'] * product['qty'];

            } else if (['bogof_price'] in product ){
                listElement.innerHTML = `
                <a class="cart-img" href="/product/${product['product_id']}"><img src="/blueprints/static/product_image/${product['product_image']}" alt="https://via.placeholder.com/70x70"></a>
                <h4><a href="/product/${product['product_id']}">${product['product_name']}</a></h4>
                <p class="quantity">${product['qty']} x - <span class="amount text-decoration-line-through">$${product['product_price']}</span><span class="amount text-danger">Buy one get one FREE</span></p>
                `;
                totalCost += parseFloat(product['bogof_price']);

                
            } else {
                listElement.innerHTML = `
                <a class="cart-img" href="/product/${product['product_id']}"><img src="/blueprints/static/product_image/${product['product_image']}" alt="https://via.placeholder.com/70x70"></a>
                <h4><a href="/product/${product['product_id']}">${product['product_name']}</a></h4>
                <p class="quantity">${product['qty']} x - <span class="amount">$${product['product_price']}</span></p>
                `;
                totalCost += product['product_price'] * product['qty'];

            }
            list.appendChild(listElement);
        });
        document.getElementById('total-amount').innerHTML = `$${nf.format(totalCost.toFixed(2))}`;
        
    } else {
        alert('Failed to update quantity.');
    }
}

async function cartCalculation() {
    const response = await fetch('/customer/cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (response.ok) {
        const products = await response.json();
        var totalCost = 0;
        let nf = new Intl.NumberFormat('en-US');


        products.forEach(product => {
            const subtotal = document.getElementById(product['product_id']+'-subtotal');
            const discountedPrice = document.getElementById(product['product_id']+'-discounted-price');
            
            if (['discounted_price'] in product && product['discounted_price']!='Buy One Get One Free') {
                var subtotalAmount = parseFloat(product['discounted_price']) * parseInt(product['qty']);
                discountedPrice.innerHTML = `$${nf.format(parseFloat(product['discounted_price']).toFixed(2))}`;
            } else if (['bogof_price'] in product ){
                var subtotalAmount = parseFloat(product['bogof_price']);
                discountedPrice.innerHTML = `<br>Buy One Get One Free`;
            } else {
                var subtotalAmount = parseFloat(product['product_price']) * parseInt(product['qty']);
            }
            
            subtotal.innerHTML = `$${nf.format(subtotalAmount.toFixed(2))}`;
            totalCost += subtotalAmount;
        });

        const gst = document.getElementById('gst');
        const totalExGst = document.getElementById('total-ex-gst');
        const total = document.getElementById('total');        
        var totalExGstCost = (totalCost / 1.15).toFixed(2);

        total.innerHTML = `$${nf.format(totalCost)}`;
        totalExGst.innerHTML = `$${nf.format(totalExGstCost)}`;
        gst.innerHTML = `$${nf.format((totalCost - totalExGstCost).toFixed(2))}`;

    } else {
        alert('Failed to update costs.');
    }
}

function changePickup() {
    const pickup = document.getElementById('pickup');
    const shipping = document.getElementById('shipping');
    if (pickup.checked) {
        shipping.innerHTML = "Free";
    } else {
        shipping.innerHTML = "Calculated during checkout";
    }
}

async function savedAddress() {
    const response = await fetch('/get_address', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ address_id: document.getElementById('saved-address').value}),
    });

    if (response.ok) {
        const address = await response.json();
        const regionSaved = address['region'];
        const unit = document.getElementById('unit');
        const address1 = document.getElementById('address1');
        const address2 = document.getElementById('address2');
        const city = document.getElementById('city');
        const postcode = document.getElementById('postcode');
        const saveThisAddress = document.getElementById('saveThisAddress');

        console.log(regionSaved);

        $('#region').val(regionSaved);
        $('#region + .nice-select .current').html(regionSaved);
        //$('#region option[value="'+regionSaved+'"').prop('selected',true);
        unit.value = address['unit_number'];
        address1.value = address['address_line1'];
        address2.value = address['address_line2'];
        city.value = address['city'];
        postcode.value = address['postcode'];
        saveThisAddress.disabled = "disabled";
        $('#saveThisAddress').removeAttr("checked");

    } else {
        alert('Failed to get saved address.');
    }
}

function addressEdited() {
    document.getElementById('saved-address').value = "default";
    $('#saveThisAddress').removeAttr("disabled");
}

function checkOuterIsland(originalShipping) {
    const region = document.getElementById('region').value;
    const shipping = document.getElementById('shipping');
    const totalCost = document.getElementById('total-cost');
    const costTbd = document.getElementById('total-cost-tbd');
    const submitBtn = document.getElementById('submit-button');
    const nextBtn = document.getElementById('next-button');

    if (region == "Outer-Islands") {
        shipping.innerHTML = 'TBD';
        totalCost.hidden = true;
        costTbd.hidden = false;
        $('#checkout-form').action = "{{url_for('customer.payment', action = request_quote)}}";
        submitBtn.innerHTML = 'Request a quote';
        submitBtn.hidden = false;
        nextBtn.hidden = true;

    } else {
        shipping.innerHTML = originalShipping;
        totalCost.hidden = false;
        costTbd.hidden = true;
        $('#checkout-form').action = "{{url_for('customer.payment', action = payment)}}";
        //submitBtn.innerHTML = 'Next: Payment Detail';
        submitBtn.hidden = true;
        nextBtn.hidden = false;

    }
}

function updateSliderValue(originalCost) {
    var totalCost = document.getElementById('total-cost');
    var points = document.getElementById('point-slider');

    document.getElementById('point-display').innerHTML = points.value + " pt.";
    var newCost = originalCost - (points.value / 100);
    totalCost.innerHTML = `$${newCost}`;
}


function showPaymentSection() {
    const first_name = document.getElementById('first_name');
    const last_name = document.getElementById('last_name');
    const email = document.getElementById('email');
    const phone = document.getElementById('phone');
    const region = document.getElementById('region');
    const unit = document.getElementById('unit');
    const address1 = document.getElementById('address1');
    const address2 = document.getElementById('address2');
    const city = document.getElementById('city');
    const postcode = document.getElementById('postcode');
    const payment = document.querySelector('input[name="payment-method"]:checked');


    document.getElementById('form-section').hidden = true;
    document.getElementById('payment-section').hidden = false;
    $('#checkout-form').action = "{{url_for('customer.payment', action = payment)}}";
    document.getElementById('submit-button').hidden = false;
    document.getElementById('next-button').hidden = true;

    var cardInputCardinnerHTML = ``
    if (noPaymentNeeded == true) {
        cardInputCardinnerHTML = ``;
    } else {
        cardInputCardinnerHTML = cardInputCardHTML;
    }

    document.getElementById('payment-section').innerHTML = `
    <h2 id="address-title">Delivery Address</h2>
    <div class="card p-4 mt-4 mb-4" id="address-card">
        <span>${first_name.value} ${last_name.value}</span>
        <span>Unit ${unit.value}</span>
        <span>${address1.value}</span>
        <span>${address2.value}</span>
        <span>${city.value}</span>
        <span>${region.value.replace(/-/g, '')} ${postcode.value}</span> 
    </div>
    <div id="payment-required-card">
        <h5>Please select a payment</h5>
    </div>
    <div id="card-card">
        ${cardInputCardinnerHTML}
    </div>
    `;
    if (document.getElementById('pickup-box').checked) {
        document.getElementById('address-card').innerHTML = ``;
        document.getElementById('address-input-card').innerHTML = ``;
        document.getElementById('address-title').innerHTML = ``;
        //document.getElementById('card-card').innerHTML = ``;
        document.querySelector('input').required = false;
    }
    if (payment.value != "card") {
        document.getElementById('card-card').innerHTML = ``;
    }
    if (payment.value) {
        document.getElementById('payment-required-card').hidden = true;
    }
}


function proceedToPayment() {
    const first_name = document.getElementById('first_name');
    const last_name = document.getElementById('last_name');
    const email = document.getElementById('email');
    const phone = document.getElementById('phone');
    const region = document.getElementById('region');
    const unit = document.getElementById('unit');
    const address1 = document.getElementById('address1');
    const address2 = document.getElementById('address2');
    const postcode = document.getElementById('postcode');
    const city =  document.getElementById('city');
    const payment = document.querySelectorAll('input[type="radio"]:checked');


    if (first_name.checkValidity() && last_name.checkValidity() && email.checkValidity() && phone.checkValidity() 
        && region.checkValidity() && address1.checkValidity() && postcode.checkValidity()
        && city.checkValidity() && payment.length > 0) {
        showPaymentSection();
         } else {
        messagePrompter('warning', "Please fill in all the required information.")
    }
    if (payment.length == 0) {
        messagePrompter('warning', "Please select a payment method.")
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const applyGiftcardButton = document.getElementById('apply-giftcard-button');
    const totalAmountElement = document.getElementById('total-cost');
    const cardCard = document.getElementById('card-card');
    const submit_button = document.getElementById('submit-button');
    const next_button = document.getElementById('next-button');
    const cash = document.getElementById('cash');
    const account = document.getElementById('account');
    const card = document.getElementById('card');
    const giftcardCheckboxes = document.querySelectorAll('.giftcard-checkbox');
    const payment_section  = document.getElementById('payment-section');
    const placeholder = document.getElementById('placeholder');
    const payment_details = document.getElementById('payment-details');
    
    cash.addEventListener('click', function() {
        payment_section.querySelectorAll('input').forEach(input => input.required = false);
        payment_section.style.display = 'none';
        placeholder.style.display = 'block';
    });
    account.addEventListener('click', function() {
        payment_section.querySelectorAll('input').forEach(input => input.required = false);
        payment_section.style.display = 'none';
        placeholder.style.display = 'block';

    });
    card.addEventListener('click', function() {
        payment_section.querySelectorAll('input').forEach(input => input.required = true);
        payment_section.style.display = 'block';
        document.getElementById('payment-required-card').style.display = 'none';
        payment_details.style.display = 'block';
        placeholder.style.display = 'none';
    });

    
    
    let initialTotalAmount = parseFloat(totalAmountElement.innerHTML.replace(/[\$,]/g, '')); // Initialize from the displayed total amount

    let nf = new Intl.NumberFormat('en-US'); // Define the number formatter

    applyGiftcardButton.addEventListener('click', function() {
        let totalGiftCardAmount = 0;
        giftcardCheckboxes.forEach(function(checkbox) {
            if (checkbox.checked) {
                totalGiftCardAmount += parseFloat(checkbox.value);
                cash.disabled = true;
                account.disabled = true;
            }else {
                cash.disabled = false;
                account.disabled = false;


            }
        });

        let newTotalAmount = initialTotalAmount - totalGiftCardAmount;
        newTotalAmount = newTotalAmount < 0 ? 0 : newTotalAmount;
        totalAmountElement.innerHTML = `$${nf.format(newTotalAmount)}`;

        if (newTotalAmount === 0) {
       
            cardCard.style.display = 'none';
            cardCard.querySelectorAll('input').forEach(input => input.required = false);
         
            payment_section.style.display = 'none';
            payment_section.querySelectorAll('input').forEach(input => input.required = false);
            submit_button.hidden = false;
            next_button.hidden = true;
        
           

        } else {
            cardCard.style.display = 'block';
            cardCard.querySelectorAll('input').forEach(input => input.required = true);
          
            payment_section.style.display = 'block';
            payment_section.querySelectorAll('input').forEach(input => input.required = false);
            submit_button.hidden = true;
            next_button.hidden = false;
       
        }
    });

   

    document.getElementById('checkout-form').addEventListener('submit', function(event) {
        giftcardCheckboxes.forEach(function(checkbox) {
            if (checkbox.checked) {
                const hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'selected_giftcards';
                hiddenInput.value = checkbox.id.replace('giftcard', '');
                event.target.appendChild(hiddenInput);
            }
        });
    });
});
