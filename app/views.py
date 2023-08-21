from django.shortcuts import render


def forms(request):
    return render(request, 'app/forms.html')


def create_form(request):
    return render(request, 'app/create_form.html')


def edit_form(request):
    return render(request, 'app/edit_form.html')