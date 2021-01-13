// Sidebar Menu Toggle
$("#menu-toggle").click(function (e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
    window.dispatchEvent(new Event('resize'));    
});

function SelectAllCheckboxes(source) {
    checkboxes = document.getElementsByName('network_checkbox');    
    for(var i=0, n=checkboxes.length;i<n;i++) {
        checkboxes[i].checked = true;
    }
}

function ToggleLoadingAnimation() {
    $("#loading-animation").removeClass("d-none"); 
    $("#loading-animation-text").removeClass("d-none");                         
}

//Add Organization name and logo at the top right in the navbar
$.get({
    url: "/api/orgInfo", success: function (data, status) {
        if (status === "success") {                        
            let templateHTML = `
                ${data[0]}
                <img src="${data[1]}" width="30" height="30" alt=""
                loading="lazy">
            `;

            $("#brand-info").html(templateHTML);
        }
    }
});