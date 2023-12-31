from django.forms import PasswordInput
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from Applyme import settings
from django.core.mail import send_mail

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist please try again")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered")
            return redirect('home')
        
        if len(username)> 10:
            messages.error(request, "username must not be under 10 characters")

        if pass1 != pass2:
            messages.error(request, "password did'nt match")

        if not username.isalnum():
            messages.error(request, "usernam modt be alpha numeric!")
            return redirect('home')
            

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your Account Has been successfully created. we have sent you a confirmation email, please confirm your email account")

        # Welcome Email

        subject = "welcome to Applyme"
        message = "Hello" + myuser.first_name + "!! \n" + "welcome to applyme!! \n Thanks for visiting my website \n we have sent you a confirmation email, please confirm your email address in order to activate your account. \n\n Thanking you\n Johnpaul Uzowuru "
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('signin')
    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname': fname})

        else:
            messages.error(request, "Bad Credential")
            return redirect('home')

    return render(request, "authentication/signin.html")
    
def signout(request):
    logout(request)
    messages.success(request, "logged out successfully")
    return redirect('home')
