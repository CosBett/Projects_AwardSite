from django.shortcuts import render,redirect
from .forms import PostForm, SignupForms
from django.contrib.auth import login, authenticate
from .models import Profile, Post, Rating
import random


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post= form.save(commit=False)
            post.user =request.user
            post.save()
    else:
        form = PostForm()

    try:
        post = Post.objects.all()
        posts =posts[::-1]
        displayed_post = random.ranint(0,len(posts)-1)
        random_posts = posts[displayed_post]
    except Post.DoesNotExist:
        posts = None    
    homepage = {'posts':posts, 'form':form,'random_posts':random_posts}
    return render(request, 'index.html', homepage)

def signup(request):
    if request.method == 'POST':
        form = SignupForms(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form =  SignupForms     

    signup_context = {'form':form}
    
    return render(request, 'registration /signup.html', signup_context)

