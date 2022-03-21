from django.shortcuts import render,redirect,get_object_or_404
from .forms import PostForm, SignupForms
from django.contrib.auth import login, authenticate,logout
from .models import Profile, Post, Rating
import random
from django.contrib.auth.decorators import login_required
from .serializer import Profile_Serializer, Post_Serializer, User_Serializer
from rest_framework import viewsets,permissions

from django.contrib.auth.models import User
from django.contrib import messages



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
        posts = Post.objects.all()
        posts = posts[::-1]
        displayed_post = random.randint(0,len(posts)-1)
        random_posts = posts[displayed_post]
    except Post.DoesNotExist:
        posts = None    
    homepage = {'posts':posts, 'form':form,'random_posts':random_posts}
    return render(request, 'index.html', homepage)

class Profile_viewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = Profile_Serializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class Post_viewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = Post_Serializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class User_viewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = User_Serializer
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

def log_in(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.success(request, ("There Was An Error Logging In, Try Again..."))	
            return redirect('login')
    else:
		    return render(request, 'registration/login.html', {})
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
    
    return render(request, 'registration/signup.html', signup_context)

@login_required(login_url='login')
def profile(request, username):
    return render(request, 'profile.html')

def user_profile(request, username):
    userProfile = get_object_or_404(User, username=username)
    if request.user == userProfile:
        return redirect('profile', username=request.user.username)
        
    UserProfile_context = {'userProfile': userProfile }
    return render(request, 'userprofile.html', UserProfile_context)

def logout_view(request):
    logout(request)
    return redirect('login')

