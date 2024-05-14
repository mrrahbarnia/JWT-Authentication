const ulListElem = document.querySelector('.ul-list')

window.addEventListener('load', async () => {
    if (!localStorage.getItem('Logged in')) {
        location.href = '/'
    } else {
        let fetchedData = await fetch('/notes/api/v1/')
        let fetchedJson = await fetchedData.json()
        if (fetchedData.status === 200) {
            fetchedJson.forEach(note => {
                ulListElem.insertAdjacentHTML('beforeend', 
                    `<li class="ul-list__item">${note.body}</li>`
                )
            })
        }
    }
})

