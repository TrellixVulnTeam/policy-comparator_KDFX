// Function for search bar
let policy_select = document.getElementById('policy');
let target_select = document.getElementById('target');
let reset = document.getElementById('remove');

function change_target() {
    policy = policy_select.value;
    fetch('/target/' + policy).then(function (response) {
        response.json().then(function (data) {
            let optionHTML = '';
            for (let target of data.targets) {
                optionHTML += '<option value="' + target + '">' + target + '</option>';
            }

            target_select.innerHTML = optionHTML;
        })
    })
}

window.onload = function(){
    if (!(policy_select.value === "--policy--")){
        change_target();
    }
};

policy_select.onchange = function(){
    change_target();
};    
