const emailRegex = /[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}/
const loginFormElem = document.querySelector('.form')
const resultElem = document.querySelector('.form__result')

window.addEventListener('load', () => {
    if (localStorage.getItem('Logged in')) {
        location.href = 'notes/'
    }
})

loginFormElem.addEventListener('submit', (event) => {
    event.preventDefault();
    if (emailRegex.test(event.target.email.value) && event.target.password.value.length >= 8) {
        fetchUserData(event.target.email.value, event.target.password.value)
    } else {
            const intervalID = setInterval(() => {
            resultElem.innerHTML = 'Email format Example: admin@admin.com <br> Password must be at least 8 characters'

            setTimeout(() => {
                resultElem.innerHTML = ''
                clearInterval(intervalID)
            }, 3000);
        });
        
    }
})

const fetchUserData = async (email, password) => {
    let fetchedData = await fetch('/accounts/api/v1/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({email: email, password: password})
    })
    if (fetchedData.status === 200) {
        setUserToLocal(email=email)
        location.href = 'notes/'
    } else {
        const intervalID = setInterval(() => {
            resultElem.innerHTML = 'There is no user with the provided info'

            setTimeout(() => {
                resultElem.innerHTML = ''
                clearInterval(intervalID)
            }, 3000);
        });
    }
}

const setUserToLocal = (email) => {
    localStorage.setItem('Logged in', email)
}
