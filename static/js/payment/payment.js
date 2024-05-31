function showPaymentButton() {
    const formElements = document.querySelectorAll('input[type="text"]');
    const subscriptionOptions = document.querySelectorAll('input[name="subscription"]');
    let allFilled = true;
    formElements.forEach((input) => {
        if (input.value === '') {
            allFilled = false;
        }
    });
    let subscriptionSelected = false;
    subscriptionOptions.forEach((option) => {
        if (option.checked) {
            subscriptionSelected = true;
        }
    });
    if (allFilled && subscriptionSelected) {
        document.getElementById('paymentButton').style.display = 'block';
    }
}