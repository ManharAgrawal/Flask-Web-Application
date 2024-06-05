$(document).ready(function() {
    $('.subscribe-btn').click(function() {
        var planId = $(this).data('plan-id');
        $.ajax({
            type: 'POST',
            url: '/create_plans',
            data: { plan_id: planId },
            success: function(response) {
                window.location.href = response;
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
            }
        });
    });
});