document.addEventListener("DOMContentLoaded", function() {
    var keys = document.querySelectorAll("ul li b");
    var values = document.querySelectorAll("ul li i");

    // Find the longest key
    var maxKeyLength = 0;
    keys.forEach(function(key) {
        maxKeyLength = Math.max(maxKeyLength, key.textContent.length);
    });

    // Set the minimum width for the key elements
    keys.forEach(function(key) {
        key.style.minWidth = (maxKeyLength * 10) + "px"; // Adjust the multiplier as needed
    });

    // Set the flex basis for the value elements to fill the remaining space
    values.forEach(function(value) {
        value.style.flexBasis = "calc(100% - " + (maxKeyLength * 10 + 10) + "px)"; // Adjust the value if there's padding/margin
    });
});