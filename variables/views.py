from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ProjectForm
from .logic import get_projects, create_project

def variable_list(request):
    projects = get_projects()
    context = {
        'variable_list': projects
    }
    return render(request, 'Variable/variables.html', context)

def variable_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            create_project(form)
            messages.add_message(request, messages.SUCCESS, 'Project created')
            return HttpResponseRedirect(reverse('variableCreate'))
        else:
            print(form.errors)
    else:
        form = ProjectForm()

    context = {
        'form': form,
    }
    return render(request, 'Variable/variableCreate.html', context)
