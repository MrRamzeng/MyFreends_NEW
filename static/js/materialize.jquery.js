$(document).ready(function () {
    $('.sidenav').sidenav();
});

// dropdown
document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.dropdown-trigger');
    var instances = M.Dropdown.init(elems);
});

// select
$(document).ready(function(){
    $('select').formSelect();
});
