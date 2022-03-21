from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from .forms import PostForm, SignupForms,RatingsForm
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
            messages.success(request, "Logged in Sucessfully!")	
            return redirect('homepage')
        else:
            messages.success(request, "There Was An Error Logging In, Try Again...")	
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

@login_required(login_url='login')
def project_rating(request, post):
    post = Post.objects.get(title=post)
    ratings = Rating.objects.filter(user=request.user, post=post).first()
    rating_status = None
    if ratings is None:
        rating_status = False
    else:
        rating_status = True
    if request.method == 'POST':
        form = RatingsForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.post = post
            rate.save()
            post_ratings = Rating.objects.filter(post=post)

            design_ratings = [d.design for d in post_ratings]
            design_average = sum(design_ratings) / len(design_ratings)

            usability_ratings = [us.usability for us in post_ratings]
            usability_average = sum(usability_ratings) / len(usability_ratings)

            content_ratings = [content.content for content in post_ratings]
            content_average = sum(content_ratings) / len(content_ratings)

            score = (design_average + usability_average + content_average) / 3
            print(score)
            rate.design_average = round(design_average, 2)
            rate.usability_average = round(usability_average, 2)
            rate.content_average = round(content_average, 2)
            rate.score = round(score, 2)
            rate.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = RatingsForm()
    project_context = {'post': post,'rating_form': form,'rating_status': rating_status
    }
    return render(request, 'project_rating.html', project_context)



def logout_view(request):
    logout(request)
    messages.success(request, "Logged out Sucessfully!")	

    return redirect('login')

