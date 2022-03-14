from django.shortcuts import render,redirect
from .forms import SignupForms
from django.contrib.auth import login, authenticate



# Create your views here.
def index(request):

    return render(request, 'index.html')

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

