from django.shortcuts import render, redirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View
from .forms import CustomUserCreationForm

def login(request):
        username = request.POST.get('login','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            #return render(request, 'notes/posts.html', {} )
            return redirect('http://127.0.0.1:8000/notes/')
            #return HttpResponseRedirect("notes/posts.html")
        else:
            return render(request, 'singin/login.html', {} )

def logout(request):
    auth.logout(request)
    return redirect('/')

class PostUser(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'singin/register.html', context={'form': form})

    def post(self, request):
        bound_form = CustomUserCreationForm(request.POST)
        if bound_form.is_valid():
            #Post.objects.filter(author = request.user.username)
            bound_form.save()
            new_post = auth.authenticate(username=bound_form.cleaned_data['username'],password=bound_form.cleaned_data['password2'])
            #bound_form.save_m2m()
            auth.login(request,new_post)
            return redirect('http://127.0.0.1:8000/notes/')
        return render(request, 'singin/register.html', context={'form': bound_form})