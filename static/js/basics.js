document.querySelectorAll('textarea:not(.no-resize)').forEach(function(element) {
    element.addEventListener('input', function(event) {
        this.style.height = "";
        this.style.height = this.scrollHeight - 20 + "px";
    });
});


const toCapitalize = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1);
};


const messageSpan = document.querySelector('.text.text-2');
const alertIcon = document.querySelector('.alert-icon')
const titleSpan = document.querySelector('.text.text-1')
const progress = document.querySelector('.progress');
const alert = document.querySelector('.alert');

let timer1, timer2;


function sendAlert(type, message) {
    titleSpan.innerText = toCapitalize(type)
    messageSpan.innerText = message

    alert.classList.add(type)
    alert.classList.add("active");
    progress.classList.add("active");

    if (type === 'error') {
        alertIcon.innerHTML = '<i class="fas fa-times"></i>'
    } else if (type === 'success') {
        alertIcon.innerHTML = '<i class="fas fa-check"></i>'
    }

    timer1 = setTimeout(() => {
        alert.classList.remove("active");
    }, 5000); //1s = 1000 milliseconds

    timer2 = setTimeout(() => {
        progress.classList.remove("active");
    }, 5300);
}


function closeAlert() {
    alert.classList.remove(...alert.classList);
    alert.classList.add('alert')

    setTimeout(() => {
        progress.classList.remove("active");
    }, 300);

    clearTimeout(timer1);
    clearTimeout(timer2);
}