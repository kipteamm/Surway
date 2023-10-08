const sectionContent = document.querySelector('.content');
const sectionOptions = document.querySelector('.modal-options');
const createNewForm = document.querySelector('.create-new-form');
const darkOverlay = document.querySelector('.dark-overlay');

let formType = 0;


function openNewForm() {
    darkOverlay.style.opacity = '.5';
    createNewForm.style.top = '50%';
};


function closeNewForm() {
    darkOverlay.style.opacity = "0";
    createNewForm.style.top = "-100%";

    formType = 0;

    sectionOptions.style.top = '50%';
    sectionContent.style.display = 'none';

    document.querySelectorAll('.tooltip-wrapper.active').forEach(function(element) {
        element.classList.remove('active')
    })

    document.querySelectorAll('.form-type').forEach(function(element) {
        element.style.display = 'none'
    })
}


function setFormType(elm, type) {
    if (formType === 0) {
        document.querySelector('.modal-options').style.top = 'var(--pdd)';

        setTimeout(function() {
            document.querySelector(`.content`).style.display = 'flex';
            document.querySelector(`.form-type.type-${type}`).style.display = 'block';
        }, 300);
    } else {
        document.querySelector(`.form-type.type-${formType}`).style.display = 'none';
        document.querySelector(`.form-type.type-${type}`).style.display = 'block';
    }

    document.querySelectorAll('.tooltip-wrapper.active').forEach(function(element) {
        element.classList.remove('active')
    })

    elm.classList.add('active')

    formType = type
}


window.onclick = function (event) {
    if (event.target !== createNewForm && event.target.closest('.create-form') === null && event.target.closest('.modal') === null) {
        closeNewForm()
    };
};


function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');

    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];

        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }

    return null;
}


async function createForm() {
    const url = `${window.location.protocol}//${window.location.host}/api/form/create`

    titleValue = document.getElementById('title').value

    if (titleValue.length < 1 || titleValue.length > 100) {
        document.getElementById('title').value = ''

        return
    }
    
    data = {
        title : titleValue,
        quiz : formType === 2,
        require_account: document.getElementById('require-account').checked
    }

    descriptionValue = document.getElementById('description').value

    if (descriptionValue !== '') {
        data.description = descriptionValue
    }

    await fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': getCookie('au_id'),
        }
    }).then(async response => {
        if (!response.ok) {
            let result;
            try {
                result = await response.json();

                console.log(result)
            } catch {
                throw new Error(response.status);
            }
            const { message: message_1 } = result;
            throw new Error(message_1 || response.status);
        }

        return response.json();
    }).then((json) => {
        window.location.href=`/forms/edit?id=${BigInt(json.form_id).toString()}`
    });
}


async function deleteForm(formID) {
    const url = `${window.location.protocol}//${window.location.host}/api/form/delete/${formID}`

    await fetch(url, {
        method: 'DELETE',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': getCookie('au_id'),
        }
    }).then(async response => {
        if (!response.ok) {
            sendAlert('error', 'An error occured.')

            let result;
            try {
                result = await response.json();

                console.log(result)
            } catch {
                throw new Error(response.status);
            }
            const { message: message_1 } = result;
            throw new Error(message_1 || response.status);
        }

        form = document.getElementById(`form-${formID}`)

        form.parentNode.removeChild(form)

        sendAlert('success', 'Successfully deleted your form.')
    });
}


window.onload = async function(event) {
    const url = `${window.location.protocol}//${window.location.host}/api/user/storage/`

    await fetch(url, {
        method: 'GET',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': getCookie('au_id'),
        }
    }).then(async response => {
        if (!response.ok) {
            let result;
            try {
                result = await response.json();

                console.log(result)
            } catch {
                throw new Error(response.status);
            }
            const { message: message_1 } = result;
            throw new Error(message_1 || response.status);
        }

        return response.json()
    }).then((json) => {
        storageValue = document.getElementById('storage-value')

        storageValue.innerText = Math.floor(json.total_size)
        
        storagePercent = document.getElementById('storage-percent')

        storagePercent.innerText = Math.floor((json.total_size / 50) * 100)
    });
}