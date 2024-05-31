
function handleSelect() {
    document.querySelectorAll('tr[data-href]').forEach(function (row) {
        row.removeEventListener('click', handleClick);
    });
}

function handleDoubleClick(e) {
    // Check if the double-click occurred on a table row
    var row = e.target.closest('tr[data-href]');
    if (row) {
        // Navigate to the next page
        window.location.href = row.getAttribute('data-href');
    }
}

document.addEventListener("DOMContentLoaded", function () {
    var delay = 450; // Adjust the delay time as needed
    var clicks = 1;
    var timer = null;

    function handleClick() {
        clicks++; // Increment the click counter
        if (clicks === 1) {
            timer = setTimeout(function () {
                // If no second click within the delay, treat it as a single-click and redirect
                window.location.href = row.getAttribute('data-href');
                clicks = 0; // Reset the click counter
            }, delay);
        } else {
            // If a second click occurs within the delay, cancel the single-click action
            clearTimeout(timer);
            clicks = 0; // Reset the click counter
        }
    }
    
    document.addEventListener('select', handleSelect);

    document.querySelectorAll('tr[data-href]').forEach(function (row) {
        row.addEventListener('click', handleClick);
        row.addEventListener('dblclick', handleDoubleClick); // Add double-click event listener
        // Prevent the default behavior for double-clicking
        row.addEventListener('dblclick', function (e) {
            e.preventDefault();
        });
    });
});

setTimeout(function () {
    var flashMessages = document.getElementById('flash-messages');
    flashMessages.style.display = 'none';
}, 3000);
