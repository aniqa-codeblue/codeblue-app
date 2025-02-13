const username = document.getElementById('uname');
const useremail = document.getElementById('uemail');
const usernum = document.getElementById('unum');
const userdetail = document.getElementById('customdetail');

const n_error = document.getElementById('name_error');
const email_error = document.getElementById('email_error');
const num_error = document.getElementById('num_error');
const detail_error = document.getElementById('detail_error');

const detail_form = document.getElementById('sign_submit_form')

detail_form.addEventListener('submit', (e)=>{

    var email_chk =  /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    var phoneno = /^\d{10}$/;
    
    if(username.value === '' || username.value == null){
        e.preventDefault();
        n_error.innerHTML = "Name is required";
    }
    else{
        n_error.innerHTML = "";
    }

    if(!useremail.value.match(email_chk)){
        e.preventDefault();
        email_error.innerHTML = "Email is required";
    }
    else{
        email_error.innerHTML = "";
    }

    if(!usernum.value.match(phoneno)){
        e.preventDefault();
        num_error.innerHTML = "Enter valid phone number without spaces";
    }
    else{
        num_error.innerHTML = "";
    }

    if(userdetail.value === '' || userdetail.value == null){
        e.preventDefault();
        detail_error.innerHTML = "Detail is required";
    }
    else{
        detail_error.innerHTML = "";
    }

})