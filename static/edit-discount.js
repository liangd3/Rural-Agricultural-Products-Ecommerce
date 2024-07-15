function messagePrompter(category, message) {
    var toastContainer = document.getElementById('toastContainer');
  
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
      console.log(content);

      toastContainer.innerHTML = toastHtml;
    
    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    var toastList = toastElList.map(function(toastEl) {
      return new bootstrap.Toast(toastEl).show();
    });
  };


async function changeDiscountStatus(pid, pname) {
    const productID = pid;
    const productName = pname;
    const product = document.getElementById(`box-${pid}`);

    var ul = document.getElementById("list");
    var li = document.createElement("li");

    const response = await fetch('/discounts/edit/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_id: productID, checked: product.checked }),
    });

    if (response.ok) {
        const status = await response.json();
        if (status == true) {
            product.checked = true;
            li.appendChild(document.createTextNode(`${productID} - ${productName}`));
            li.setAttribute("id", `list-${productID}`);
            ul.appendChild(li);        
            messagePrompter('success', `Discount added to product ${productID}.`);
        } else {
            product.checked = false;
            document.getElementById(`list-${productID}`).remove();
            messagePrompter('warning', `Product ${productID} returns to normal price.`);
        }

    } else {
        alert('Failed to update quantity.');
    }
}