const overview = document.getElementById('overview')
const form = document.querySelector('.form')


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


function createSection(answerData) {
    const questionData = answerData.question
    const section = document.createElement('div')

    section.classList.add('form-section')
    section.classList.add('form-question')
    section.setAttribute('data-index', questionData.index)

    switch (questionData.question_type) {
        case 1:
            questionType = '<i class="fas fa-quote-right"></i>'
            
            break;
        case 2:
            questionType = '<i class="fas fa-keyboard"></i>'
            
            break;
        case 3:
            questionType = '<i class="number">0</i>'

            break;
        case 4:
            questionType = '<i class="fas fa-calendar-alt"></i>'
            
            break;
    }

    required = ''

    if (questionData.required) {
        required = '<span class="required">*</span>'
    }

    editButton = ''

    section.innerHTML = `
        <div class="section-type">
            ${questionType}
        </div>
        <div class="section-content">
            <h3>${questionData.question}${required}</h3>
            <p>
                ${answerData.answer}
            </p>
        </div>
    `

    return section
}


async function getResponse(trackID) {
    const url = `${window.location.protocol}//${window.location.host}/api/answers/${getCookie('ef_id')}/${trackID}`

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
        const answerElement = document.createElement('div')
        
        answerElement.classList.add('active')
        answerElement.classList.add('answer')

        answerElement.id = trackID

        json.forEach(function(question) {
            answerElement.appendChild(createSection(question))
        })

        form.appendChild(answerElement)
    });
}


function previousAnswer() {
    if (index === responses.length - 1) {
        index --
    }

    if (index >= 0) {
        document.querySelector('.active').classList.remove('active')

        let response = document.getElementById(responses[index])

        if (response === null) {
            response = getResponse(responses[index])
        } else {
            response.classList.add('active')
        }

        if (index > 0) {
            index --
        }
    }
}


function nextAnswer() {
    if (index === 0) {
        index ++
    }

    if (index < responses.length) {
        document.querySelector('.active').classList.remove('active')

        let response = document.getElementById(responses[index])

        if (response === null) {
            console.log('fetch')

            response = getResponse(responses[index])
        } else {
            response.classList.add('active')
        }

        if (index < 1) {
            index ++
        }
    }
}


function answerOverview() {
    document.querySelector('.active').classList.remove('active');

    document.getElementById('overview').classList.add('active');

    index = 0;
}