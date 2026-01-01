$(document).ready(function() {
    
    setTimeout(function() {
        
        $('.alert').each(function(index, alert) {
            
            setTimeout(function() {
                $(alert).fadeOut(500, function() {
                    $(this).remove(); 
                });
            }, 3000); 
        });
        
        
        $('.alert .btn-close').click(function() {
            $(this).closest('.alert').fadeOut(300);
        });
    }, 100);
});
