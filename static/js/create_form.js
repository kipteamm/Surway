const createNewForm = document.querySelector('.create-new-form');
const darkOverlay = document.querySelector('.dark-overlay');

function openNewForm() {
    console.log('huh?')

    darkOverlay.style.opacity = '.5';
    createNewForm.style.top = '50%';
};


function closeNewSection() {
    darkOverlay.style.opacity = "0";
    createNewForm.style.top = "-100%";
}


window.onclick = function (event) {
    if (event.target !== createNewForm && event.target.id !== 'btn' && event.target.closest('.modal') === null) {
        closeNewSection()
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