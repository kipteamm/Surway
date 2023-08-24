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


function loadForm() {
    if (document.querySelector('iframe').getAttribute('data-hcaptcha-response') !== '') {
        document.querySelector('.captcha').style.display = 'none';
        document.querySelector('.form').style.display = 'block';
    } else {
        sendAlert('error', "Still unsure whether you are human or not.")
    }
}


async function submit(formID, trackID) {
    error = false;

    let data = {
        form_id: formID,
        track_id : trackID,
        answers: []
    }

    const requiredElements = document.querySelectorAll('.form-question.required-question');
    const totalRequired = requiredElements.length;

    for (let currentIndex = 0; currentIndex < totalRequired; currentIndex++) {
        const element = requiredElements[currentIndex];
        const input = element.querySelector('input, textarea');

        if (input.value === '') {
            sendAlert('error', "You don't have all required fields filled in.");
            element.classList.add('bounce');

            error = true;

            await new Promise(resolve => {
                setTimeout(() => {
                    element.classList.remove('bounce');
                    resolve(); // Resolve the promise after the animation
                }, 2000); // Animation duration is 2 seconds
            });
        } else {
            const answer = {
                question_id: element.id.split('-')[1],
                answer: input.value
            }

            data.answers.push(answer);
        }
    }

    if (error) {
        return
    }

    const url = `${window.location.protocol}//${window.location.host}/api/answer/submit`

    authorization = getCookie('au_id')

    if (authorization === null) {
        headers = {
            'Content-Type': 'application/json',
        }
    } else {
        headers = { 
            'Authorization': getCookie('au_id'),
            'Content-Type': 'application/json',
        }
    }

    console.log(data)

    await fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        mode: 'cors',
        headers: headers
    }).then(async response => {
        if (!response.ok) {
            let result;
            try {
                result = await response.json();

                console.log(result)

                sendAlert('error', result);
            } catch {
                throw new Error(response.status);
            }
            sendAlert('error', "Unexpected error occured.");

            const { message: message_1 } = result;
            throw new Error(message_1 || response.status);
        }
        
        form = document.querySelector('.form')

        form.innerHTML = `
            <div class="form-section form-meta">
                <h1>Answer submitted.</h1>
                <p>
                    Thank you for submitting your answer.
                </p>
            </div>
        `

        sendAlert('success', "Your answer has been submitted.");
    })
}