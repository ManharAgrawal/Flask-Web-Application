function updateAmount() {
            const subscriptionType = document.getElementById('subscription_type').value;
            const amountElement = document.getElementById('subscription_amount');
            let amount = 0;
            if (subscriptionType === 'monthly') {
                amount = 10000; // INR 10000
            } else if (subscriptionType === 'quarterly') {
                amount = 25000; // INR 25000
            } else if (subscriptionType === 'annually') {
                amount = 100000; // INR 100000
            }
            amountElement.textContent = `Amount: INR ${amount}`;
        }