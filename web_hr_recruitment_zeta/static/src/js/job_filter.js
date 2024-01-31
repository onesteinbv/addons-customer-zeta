odoo.define("quatra_website.redirect", function (require) {
    "use strict";

//    Var ajax = require("web.ajax");
    require("web.dom_ready");

    console.log(window.location.hash)
    // Check on filter?
    var openval = null;
    if (window.location.hash !== '' ) {
        openval = window.location.hash.slice(1);
        $('#' + openval).addClass('show');
    }


    const checkboxes = document.querySelectorAll('.filter_label');
    if(window.location.pathname.includes("/jobs/label_ids/")){
        var label_ids= window.location.pathname.replace("/jobs/label_ids/","").split(",");
        for (var i = 0; i < label_ids.length; i++) {
            for (var j = 0; j < checkboxes.length;j++) {
                if(checkboxes[j].id===label_ids[i]){
                       checkboxes[j].checked = true
                }
            }
        }
    }

    for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].addEventListener('change', function() {
        var ids="/label_ids/"
        var anyChecked=false;
        for (var j = 0; j < checkboxes.length;j++) {
            if(checkboxes[j].checked){
                ids = ids + checkboxes[j].id+","
                anyChecked = true;
            }
        }
        if(anyChecked){
        window.location.replace('/jobs'+ids.replace(/,$/,"")+'#filter');
        } else{
        window.location.replace('/jobs'+'#filter');
        }

    })
    }



});
