let deliveryButton = document.getElementById('payment-on-delivery');
if (deliveryButton !== null) {
    deliveryButton.addEventListener('click', () => {
        let elements = document.getElementsByClassName('credit-card-details');
        if (deliveryButton.checked) {
            for (let index in elements)
                elements[index].disabled = true;
        } else {
            for (let index in elements)
                elements[index].disabled = false;
        }
    });
}

let creditCardButton = document.getElementById('credit-card-payment');
if (creditCardButton !== null) {
    creditCardButton.addEventListener('click', () => {
        let elements = document.getElementsByClassName('credit-card-details');
        if (creditCardButton.checked) {
            for (let index in elements)
                elements[index].disabled = false;
        } else {
            for (let index in elements)
                elements[index].disabled = true;
        }
    });
}

$.ajax({
    type: 'GET',
    url: '/shopping-cart/order-items-count',
    success: function (data) {
        $('.order-items-count').text(data['count']);
    }
});
