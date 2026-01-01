$(document).ready(function() {
    console.log("الموقع يعمل بنجاح!");
    
    
    setTimeout(function() {
        $('#loading-screen').fadeOut(1000);
        $('#main-content').fadeIn(1000);
    }, 1000);

    
    $('#classificationBtn').click(function(e) {
        e.preventDefault();
        e.stopPropagation();
        $('#filterDropdown').slideToggle(300);
    });

    $(document).click(function(e) {
        if (!$(e.target).closest('#classificationBtn, #filterDropdown').length) {
            $('#filterDropdown').slideUp(300);
        }
    });

    
    $('#viewProjectsBtn').click(function() {
        
        $('#prioritiesSection').slideUp(500);
        $('#implementationSection').slideUp(500);
        
        $('#projectsSection').slideToggle(500, function() {
            console.log("قسم المشاريع: " + ($(this).is(':visible') ? "مفتوح" : "مغلق"));
        });
    });

    
    $('#viewPrioritiesBtn').click(function() {
        
        $('#projectsSection').slideUp(500);
        $('#implementationSection').slideUp(500);
        
        $('#prioritiesSection').slideToggle(500, function() {
            console.log("قسم الأولويات: " + ($(this).is(':visible') ? "مفتوح" : "مغلق"));
        });
    });

    
    $('#viewImplementationBtn').click(function() {
        
        $('#projectsSection').slideUp(500);
        $('#prioritiesSection').slideUp(500);
        
        $('#implementationSection').slideToggle(500, function() {
            console.log("قسم التنفيذ: " + ($(this).is(':visible') ? "مفتوح" : "مغلق"));
        });
    });
});