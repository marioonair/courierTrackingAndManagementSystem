from django.contrib.auth import logout
from django.http import HttpResponseRedirect, response
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_users,allowed_users,admin_only
from .forms import RegisterForm

# Create your views here.
from django.urls import reverse


@unauthenticated_users
def login(request):
    return render(request, 'login.html')

@login_required(login_url="/login/")
@allowed_users(allowed_roles=['Admin', 'Manager'])
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Staff')
            user.groups.add(group)
            return redirect('success')
        else:
            return render(request, 'registration/register.html', {'form': form})

    else:
        return render(request, 'registration/register.html', {'form': form})




@login_required(login_url="/login/")
# @allowed_users(allowed_roles=['Admin']) # add allowed list
# @admin_only
def success(request):
    return render(request, 'success/success.html')
# @unauthenticated_users
def user_logout(request):
    if request.method == "POST":
        logout(request)
        return HttpResponseRedirect(reverse('index'),)

    # from django import template
    # from django.contrib.auth.models import Group
    #
    # register = template.Library()
    #
    # @register.filter(name='has_group')
    # def has_group(user, group_name):
    #     group = Group.objects.get(name=group_name)
    #     return group in user.groups.all()

    # def register(request):
    #     form = RegisterForm()
    #     if request.method == 'POST':
    #         form = RegisterForm(request.POST)
    #         if form.is_valid():
    #             form.save()
    #             return redirect('success')
    #         else:
    #             return render(request, 'registration/register.html', {'form': form})
    #
    #     else:
    #         return render(request, 'registration/register.html', {'form': form})
