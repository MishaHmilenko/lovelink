const createUserBtn = document.getElementById('createUserBtn');
if (createUserBtn) {
    createUserBtn.addEventListener('click', createUser);
}

const loginBtn = document.getElementById('loginBtn');
if (loginBtn) {
    loginBtn.addEventListener('click', login);
}

function displayErrors(errorsObj) {
    const errorContainer = document.getElementById('error-container');

    errorContainer.innerHTML = '';

    for (let field in errorsObj.errors) {
        const error = errorsObj.errors[field][0]
        const divError = document.createElement('div')

        divError.textContent = error
        divError.style.color = '#9C3E3E'

        errorContainer.appendChild(divError)
    };
}

function createUser() {
    const username = document.getElementById('username').value;
    const birthday = document.getElementById('birthday').value;
    const gender = document.getElementById('gender').value;
    const email = document.getElementById('email').value;
    const phone_number = document.getElementById('phone_number').value;
    const password1 = document.getElementById('password1').value;
    const password2 = document.getElementById('password2').value;

    const userData = {
        username: username,
        birthday: birthday,
        gender: gender,
        email: email,
        phone_number: phone_number,
        password1: password1,
        password2: password2
    };

    const apiUrl = 'http://127.0.0.1:8000/users/registration/';
    
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify(userData)
    };

    fetch(apiUrl, requestOptions)
        .then(response => {
            if (!response.ok) {
                if (response.status === 400) {
                    return response.json().then(data => {
                        displayErrors(data)
                        throw new Error('Problem with input data')
                    });
                }
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data && data.errors) {
                console.log('Server errors:', data.errors);
            } else {
                console.log('User created successfully:', data);
                window.location.href = 'http://127.0.0.1:5501/auth/login.html';
            }
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error.message);
        });
}

function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const loginData = {
        username: username,
        password: password
    };

    const apiUrl = 'http://127.0.0.1:8000/users/login/';

    const requestOptions = {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify(loginData)
    };

    fetch(apiUrl, requestOptions)
        .then(response => {
            if (!response.ok) {
                if (response.status == 401) {
                    return response.json().then(data => {
                        displayErrors(data)
                        throw new Error('Problem with input data')
                    })
                }
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data && data.errors){
                console.log('Server errors:', data.errors);
            }
            else {
                console.log('Login successful:', data);
                window.location.href = 'http://127.0.0.1:8000/users/profile/'
            }
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}