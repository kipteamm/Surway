const newSectionElement = document.querySelector('.new-section');
const newSectionWizard = document.querySelector('.new-section-wizard');
const questionTextarea = document.getElementById('question-input');
const sectionOptions = document.querySelector('.modal-options');
const answerOption = document.querySelector('.answer-option');
const settingsMenu = document.querySelector('.settings-menu');
const darkOverlay = document.querySelector('.dark-overlay');
const question = document.querySelector('.question');
const answer = document.querySelector('.answer');

let isSettingsMenuActive = false;
let isNewSectionActive = false;
let settingPanel = 'settings';
let sectionType = 0;


function openSettingsMenu(element, specificSettingPanel) {
    darkOverlay.style.opacity = '.5';
    settingsMenu.style.top = '50%';

    isSettingsMenuActive = true;

    document.querySelectorAll('i.active').forEach(function(element) {
        element.classList.remove('active')
    })

    element.classList.add('active')

    document.querySelector(`.setting.${settingPanel}`).style.display = 'none';
    document.querySelector(`.setting.${specificSettingPanel}`).style.display = 'flex';
    
    settingPanel = specificSettingPanel
}


function closeSettingsMenu() {
    darkOverlay.style.opacity = "0";
    settingsMenu.style.top = "-100%";

    isSettingsMenuActive = false;
}


function newSection() {
    darkOverlay.style.opacity = '.5';
    newSectionWizard.style.top = '50%';

    isNewSectionActive = true;
};


function closeNewSection() {
    darkOverlay.style.opacity = "0";
    newSectionWizard.style.top = "-100%";

    isNewSectionActive = false;
}


window.onclick = function (event) {
    if (isNewSectionActive) {
        if (event.target !== newSectionWizard && !event.target.classList.contains('new-section') && event.target.closest('.new-section-wizard') === null) {
            closeNewSection()
        };
    }
    
    if (isSettingsMenuActive) {
        if (event.target !== settingsMenu && event.target.closest('.toolbar') === null && event.target.closest('.settings-menu') === null) {
            closeSettingsMenu()
        };
    }  
};


function textResponse() {
    const elm = document.createElement('textarea')

    elm.placeholder = "Any answer (e.g. Depends on how many elephants you have.)"
    elm.id = "question-answer"
    elm.classList.add('no-resize')

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
        document.querySelector('.content').style.display = 'flex'

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
        required : document.getElementById('required-question').checked,
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
        newSectionElement.parentNode.insertBefore(createSection(json), newSectionElement) 

        closeNewSection()
    });
}


function createSection(questionData) {
    const section = document.createElement('div')

    section.classList.add('form-section')
    section.classList.add('form-question')
    section.setAttribute('data-index', questionData.index)

    answerType = ''

    switch (questionData.question_type) {
        case 1:
            questionType = '<i class="fas fa-quote-right"></i>'

            if (questionData.quiz) {
                answerType = '<textarea class="secondary-input" placeholder="Your answer" oninput="resizeTextarea(this)"></textarea>'
            }
            
            break;
        case 2:
            questionType = '<i class="fas fa-keyboard"></i>'

            if (questionData.quiz) {
                answerType = '<textarea class="secondary-input" placeholder="Your answer" oninput="resizeTextarea(this)"></textarea>'
            }
            
            break;
        case 3:
            questionType = '<i class="number">0</i>'

            if (questionData.quiz) {
                answerType = '<input class="secondary-input" type="number">'
            }

            break;
        case 4:
            questionType = '<i class="fas fa-calendar-alt"></i>'

            if (questionData.quiz) {
                answerType = '<input class="secondary-input" type="date">'
            }
            
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
            ${answerType}
        </div>
    `

    return section
}


function resizeTextarea(textarea) {
    textarea.style.height = 'auto'; // Reset height to auto
    textarea.style.height = this.scrollHeight + 'px'; // Set height to scrollHeight
}


// DRAG & DROP credit (https://stackoverflow.com/a/71474727/19069744)
const ELS_child = document.querySelectorAll('.form-question')

let EL_drag; // Used to remember the dragged element

const addEvents = (EL_ev) => {
  EL_ev.setAttribute("draggable", "true");
  EL_ev.addEventListener("dragstart", onstart);
  EL_ev.addEventListener("dragover", (ev) => ev.preventDefault());
  EL_ev.addEventListener("drop", ondrop);
};

const onstart = (ev) => EL_drag = ev.currentTarget;

const ondrop = (ev) => {
    if (!EL_drag) return;

    ev.preventDefault();
  
    const EL_targ = ev.currentTarget;
    const EL_targClone = EL_targ.cloneNode(true);
    const EL_dragClone = EL_drag.cloneNode(true);

    EL_targClone.setAttribute('data-index', parseInt(EL_drag.getAttribute('data-index')))
    EL_dragClone.setAttribute('data-index', parseInt(EL_targ.getAttribute('data-index')))

    if (EL_drag !== EL_targ) {
        updateQuestionPosition(EL_targClone.id, parseInt(EL_drag.getAttribute('data-index')))
    } 
  
    EL_targ.replaceWith(EL_dragClone);
    EL_drag.replaceWith(EL_targClone);
  
    addEvents(EL_targClone); // Reassign events to cloned element
    addEvents(EL_dragClone); // Reassign events to cloned element
  
    EL_drag = undefined;
};

ELS_child.forEach((EL_child) => addEvents(EL_child));


async function updateQuestionPosition(questionID, index) {
    const url = `${window.location.protocol}//${window.location.host}/api/question/update`
    
    data = {
        question_id : questionID,
        index : index
    }

    await fetch(url, {
        method: 'UPDATE',
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
    })
}


async function updateFormMeta(formID, title, description) {
    const url = `${window.location.protocol}//${window.location.host}/api/form/update`
    
    data = {
        form_id : formID,
    }

    if (title !== null) {
        data.title = title
    }

    if (description !== null) {
        data.description = description
    }

    await fetch(url, {
        method: 'UPDATE',
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
    })
}