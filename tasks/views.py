from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import TaskForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UserCreationForm(request.POST)
    context = {'form':form}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "User created successfully!")
            return redirect('login')
    return render(request, 'tasks/register.html', context=context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'you are now logged in as {username}')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    context = {}
    return render(request, 'tasks/login.html', context=context)


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        user = request.user
        form = TaskForm(request.POST, instance=Task(author=user))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))
    
    tasks = Task.objects.filter(author=request.user)
    
    form = TaskForm()
    context = {'form': form, 'tasks': tasks}
    return render(request, 'tasks/task.html', context=context)

@login_required(login_url='login')
def edit_task(request, id):
    task = Task.objects.get(id=id)
    form = TaskForm(instance=task)    
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('home'))
    
    context = {'form':form}
    return render(request, 'tasks/edit_task.html', context=context)

@login_required(login_url='login')
def delete_task(request, id):
    task = Task.objects.get(id=id)
    context = {'task':task}
    if request.method == 'POST':
         task.delete()
         return redirect('home')
    return render(request, 'tasks/delete_task.html', context=context)

