const profileEmailElem = document.querySelector('.profile__email')
const profileRuleElem = document.querySelector('.profile__role')

window.addEventListener('load', async () => {
    if (!localStorage.getItem('Logged in')) {
        location.href = '/'
    } else {
        let fetchedData = await fetch('/accounts/api/v1/my-profile/')
        let fetchedJson = await fetchedData.json()
        if (fetchedData.status === 200) {
            if (fetchedJson.role === 'NU') {
                profileEmailElem.innerHTML = fetchedJson.email
                profileRuleElem.innerHTML = 'My Role: Normal User'
            } else if (fetchedJson.role === 'AD') {
                profileEmailElem.innerHTML = fetchedJson.email
                profileRuleElem.innerHTML = 'My Role: Admin'
            }
        } else if (fetchedData.status === 401) {
            localStorage.removeItem('Logged in')
            location.href = '/'
        }
    }
})