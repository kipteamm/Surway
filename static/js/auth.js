const authInputs = document.querySelectorAll('input');
const emailRegex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

function hideInputs() {
    authInputs.forEach(function(element) {
        if (element.type !== 'text') {
            element.style.display = 'none'
        }
    })
}

hideInputs()


function nextInput(elm) {
    elm = elm.nextElementSibling

    elm.style.display = 'block';
    elm.focus()
}


async function checkEmail(elm, checkEmailUnique) {
    if (!elm.value.match(emailRegex)) {
        elm.value = '';

        hideInputs()

        return
    }

    if (!checkEmailUnique) {
        nextInput(elm) 

        return
    }

    const url = `${window.location.protocol}//${window.location.host}/api/user/${elm.value}`

    await fetch(url, {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(async response => {
        if (!response.ok) {
            nextInput(elm) 

            return
        }

        elm.value = '';

        hideInputs()

        return
    })
}


function checkPassword(elm, index) {
    if (elm.value.length < 8) {
        elm.value = '';

        return
    }

    if (index === 2 && elm.value !== document.getElementsByName('password')[0].value) {
        console.log(elm.value, document.getElementsByName('password')[0].value)

        elm.value = '';

        return
    }

    nextInput(elm)
}


document.addEventListener('keydown', function(event) {
    if (event.code === 'Tab') {
        event.preventDefault(); 

        authInputs.forEach(function(element) {
            if (element.id === 'ea') {
                checkEmail(element)

                return
            }

            checkPassword(element)
        })
    }

    if (event.code === 'Enter') {
        if (document.querySelector("input[type='submit']").style.display === 'none') {
            event.preventDefault()

            authInputs.forEach(function(element) {
                if (element.id === 'ea') {
                    checkEmail(element)

                    return
                }

                if (element.type !== 'submit') {
                    checkPassword(element)

                    return
                }
            })
        }
    }
});
