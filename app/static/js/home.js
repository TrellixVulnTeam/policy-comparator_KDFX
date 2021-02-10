function new_option(option) {
    return '<option value="' + option + '">' + option + '</option>';
}
function change_target(policy_select,target_select) {
    policy = policy_select.value.toLowerCase();
    fetch('/target/' + policy).then(function (response) {
        response.json().then(function (data) {
            let optionHTML = '';
            
            for (let target of data.targets) {
                optionHTML += new_option(target);
            }
            
            target_select.innerHTML = optionHTML;
        })
    })
}

function titleCase(str) {
  str = str.toLowerCase().split(' ');
  for (var i = 0; i < str.length; i++) {
    str[i] = str[i].charAt(0).toUpperCase() + str[i].slice(1); 
  }
  return str.join(' ');
}

window.onload = function () {
     
    let policy_select = document.getElementById('policy');
    let target_select = document.getElementById('target');

    if (window.location.pathname.includes('factsheet')) {
        var id_sheet = document.getElementsByClassName('container')[0].id;
        var sheet_policy = id_sheet.split('-')[0];
        var sheet_target = id_sheet.split('-')[1];

        fetch('/target/' + sheet_policy).then(function (response) {
            response.json().then(function (data) {
                var optionHTML = ''; // Defining the options list
                optionHTML += new_option(titleCase(sheet_target)); // Define first option
                for (var target of data.targets) {
                    if (!(target === titleCase(sheet_target))) {
                        optionHTML += new_option(target);
                    }
                }
                target_select.innerHTML = optionHTML;
            })
        })
        policy_select.onchange = function(){
            change_target(policy_select,target_select);
        }; 
    } else {
        policy_select.onchange = function () {
        change_target(policy_select,target_select);
        }; 
    }
 };

// policy_select.onchange = function(){
//     change_target();
// };    