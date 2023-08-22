const newSectionElement = document.querySelector('.new-section');
const newSectionWizard = document.querySelector('.new-section-wizard');
const questionTextarea = document.getElementById('question-input');
const sectionOptions = document.querySelector('.section-options');
const answerOption = document.querySelector('.answer-option');
const darkOverlay = document.querySelector('.dark-overlay');
const question = document.querySelector('.question');
const answer = document.querySelector('.answer');

let sectionType = 0;

function newSection() {
    darkOverlay.style.opacity = '.5';
    newSectionWizard.style.top = '50%';
};


window.onclick = function (event) {
    if (event.target !== newSectionWizard && !event.target.classList.contains('new-section') && event.target.closest('.new-section-wizard') === null) {
        darkOverlay.style.opacity = "0";
        newSectionWizard.style.top = "-100%";
    };
};


function textResponse() {
    const elm = document.createElement('textarea')

    elm.placeholder = "Any answer (e.g. Depends on how many elephants you have.)"
    elm.id = "question-answer"

    return elm 
}


function numberResponse() {
    const elm = document.createElement('input')

    elm.type = "number"
    elm.placeholder = "17"
    elm.id = "question-answer"

    return elm 
}


function dateResponse() {
    const elm = document.createElement('input')

    elm.type = "date"
    elm.id = "question-answer"

    return elm 
}


function setSectionType(elm, type) {
    let timeout = 0;

    if (sectionType === 0) {
        sectionOptions.style.top = 'var(--pdd)';
        timeout = 300;
    }

    document.querySelectorAll('.tooltip-wrapper.active').forEach(function(element) {
        element.classList.remove('active')
    })

    elm.classList.add('active')

    questionTextarea.placeholder = 'Any question (e.g. How many elephants fit in a fridge?)'

    setTimeout(function() {
        question.style.display = 'block';
        answer.style.display = 'block';

        answerOption.innerHTML = '';

        switch (type) {
            case 1:
                answerOption.appendChild(textResponse())
    
                break;
            case 2:
                answerOption.appendChild(textResponse())
    
                break;
            case 3:
                answerOption.appendChild(numberResponse())
    
                break;
    
            case 4:
                answerOption.appendChild(dateResponse())

                questionTextarea.placeholder = 'Any question (e.g. On what date did mankind "supposedly" land on the moon?)'
    
                break;
        }
    }, timeout);

    sectionType = type
}


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


async function addToForm() {
    const url = `${window.location.protocol}//${window.location.host}/api/question/create`

    answerValue = document.getElementById('question-answer').value

    if (sectionType === 3) {
        answerValue = parseInt(document.getElementById('question-answer').value)
    }
    
    data = {
        form_id : getCookie('ef_id'),
        question_type : sectionType,
        question : document.getElementById('question-input').value,
        answer : answerValue,
    }

    console.log(data)

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
        newSectionElement.parentNode.insertBefore(createSection(json, true), newSectionElement) 
    });
}


function createSection(questionData, editing) {
    const section = document.createElement('div')

    console.log(questionData)

    section.classList.add('form-section')
    section.classList.add('form-question')

    switch (questionData.question_type) {
        case 1:
            questionType = '<i class="fas fa-quote-right"></i>'
            answerType = '<textarea class="secondary-input" placeholder="Your answer" oninput="resizeTextarea(this)"></textarea>'

            break;
        case 2:
            questionType = '<i class="fas fa-keyboard"></i>'
            answerType = '<textarea class="secondary-input" placeholder="Your answer" oninput="resizeTextarea(this)"></textarea>'

            break;
        case 3:
            questionType = '<i class="number">0</i>'
            answerType = '<input class="secondary-input" type="number">'

            break;
        case 4:
            questionType = '<i class="fas fa-calendar-alt"></i>'
            answerType = '<input class="secondary-input" type="date">'

            break;
    }

    editButton = ''

    if (editing) {
        editButton = '<i class="fas fa-edit"></i>'
    }

    section.innerHTML = `
        <div class="section-type">
            ${questionType}
            ${editButton}
        </div>
        <div class="section-content">
            <h3>${questionData.question}</h3>
            ${answerType}
        </div>
    `

    return section
}


function resizeTextarea(textarea) {
    textarea.style.height = 'auto'; // Reset height to auto
    textarea.style.height = this.scrollHeight + 'px'; // Set height to scrollHeight
}