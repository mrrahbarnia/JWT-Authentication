const emailRegex = /[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}/
const registerFormElem = document.querySelector('.form')
const resultElem = document.querySelector('.form__result')

registerFormElem.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!emailRegex.test(event.target.email.value)) {
        showResultInterval('Email format example: admin@example.com')
    } else if (event.target.password.value.length < 8) {
        showResultInterval('Password must be at least 8 characters')
    } else if (event.target.password.value !== event.target['confirm-password'].value) {
        showResultInterval("Passwords don't match")
    } else {
        registerUserApi(
            event.target.email.value,
            event.target.password.value,
            event.target['confirm-password'].value
        )
    }
})

const showResultInterval = (result) => {
    const intervalID = setInterval(() => {
        resultElem.innerHTML = result

        setTimeout(() => {
            resultElem.innerHTML = ''
            clearInterval(intervalID)
        }, 3000);
    });
}

const registerUserApi = async (email, password, password2) => {
    let fetchedData = await fetch('/accounts/api/v1/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(
            {email: email, password: password, confirm_password: password2}
        )
    })
    let fetchedJson = await fetchedData.json()
    if (fetchedData.status === 201) {
        location.href = '/'
    } else if (fetchedJson.email[0] === 'There is an active user with the provided email.') {
        showResultInterval('There is an active user with the provided email.')
    }
}