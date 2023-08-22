document.querySelectorAll('textarea:not(.no-resize)').forEach(function(element) {
    element.addEventListener('input', function(event) {
        this.style.height = "";
        this.style.height = this.scrollHeight - 20 + "px";
    });
});