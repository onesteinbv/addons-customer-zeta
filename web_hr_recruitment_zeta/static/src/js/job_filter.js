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

//    Const checkboxes = document.querySelectorAll(".btn");

});
