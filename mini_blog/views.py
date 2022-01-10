from django.http import request
from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group

# HOME
def home(req):
    posts = Post.objects.all()
    return render(req, 'mini_blog/home.html', {'posts':posts})


#ABOUT
def about(req):
    return render(req, 'mini_blog/about.html')


#CONTACT
def contact(req):
    return render(req, 'mini_blog/contact.html')


#DASHBOARD
def dashboard(req):
    if req.user.is_authenticated:
        posts = Post.objects.all()
        user = req.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(req, 'mini_blog/dashboard.html', {'posts':posts, 'full_name':full_name, 'groups':gps})
    else:
        return HttpResponseRedirect('/login')


#SIGN-UP
def signup(req):
    if req.method == 'POST':
        form = SignUpForm(req.POST)
        if form.is_valid():
            messages.success(req, 'Congratulations!! You are a author of our blog now!')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    return render(req, 'mini_blog/signup.html', {'form': form})


#LOGIN
def user_login(req):
    if not req.user.is_authenticated:
        if req.method == "POST":
            form = LoginForm(request=req, data=req.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(req, user)
                    messages.success(req, 'Logged in Successfully !!')
                    return HttpResponseRedirect('/dashboard')
        else:
            form = LoginForm()
        return render(req, 'mini_blog/login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard')


#LOGOUT
def user_logout(req):
    logout(req)
    return HttpResponseRedirect('/') 


#ADD NEW POST
def add_post(req):
    if req.user.is_authenticated:
        if req.method=="POST":
            form = PostForm(req.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                edited_post=Post(title=title, content=content)
                edited_post.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(req, "mini_blog/addpost.html", {'form':form})
    else:
        return HttpResponseRedirect("/login")

#EDIT POST
def update_post(req, id):
    if req.user.is_authenticated:
        if req.method=="POST":
            pi=Post.objects.get(pk=id)
            form = PostForm(req.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(req, "mini_blog/updatepost.html", {'form':form})
    else:
        return HttpResponseRedirect("/login")


#DELETE POST
def delete_post(req, id):
    if req.user.is_authenticated:
        if req.method == "POST":
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect("/login")