 document.addEventListener("DOMContentLoaded", function() {
        document.querySelectorAll('tr[data-href]').forEach(function(row) {
            row.addEventListener('click', function() {
                window.location.href = this.getAttribute('data-href');
            });
        });
    });

setTimeout(function() {
    var flashMessages = document.getElementById('flash-messages');
    flashMessages.style.display = 'none';
}, 3000);