from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here.

def index(request): 
    properties = Property.objects.all() 
    search = request.GET.get('search')
    rent = request.GET.get('available')
    if search is not None: 
        properties = Property.objects.filter(title__icontains = search)
    if rent=="true": 
        properties = Property.objects.filter(available_for_rent = True)
    elif rent == "false":
        properties = Property.objects.filter(available_for_rent = False)

    return render(request,'index.html',{'properties':properties,"rent":rent})


def propertyDetail(request,id):
    if request.user.is_authenticated:
        try : 
            property = Property.objects.get(pk = id)
        except: 
            return redirect('/')
        return render(request,'propertyDetail.html',{'property':property})
    else:
        return redirect('/login/')


def signin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not username or not password:
                messages.error(request, 'Please provide both username and password.')
            else:
                user = authenticate(request, username=username, password=password)
                
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        # Redirect to a success page or any other page you want
                        return redirect('/')  # Change '/' to your actual success URL
                    else:
                        messages.error(request, 'Your account is not active. Please contact support.')
                else:
                    messages.error(request, 'Invalid username or password.')
        
        return render(request, 'login.html', {})
    else:
        return redirect('/')
def register(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            # Extract data from the form
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('fname')
            last_name = request.POST.get('lname')
            password = request.POST.get('password')
            confirm_password = request.POST.get('cpassword')

            # Your non-field validation logic
            if not username or not email or not first_name or not last_name or not password or not confirm_password:
                messages.error(request, 'Please fill in all the fields.')
                return redirect('register')

            # Check if the username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists. Please choose a different one.')
                return redirect('register')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email address already registered. Please use a different one.')
                return redirect('register')

            # Check if passwords match
            if password != confirm_password:
                messages.error(request, 'Passwords do not match.')
                return redirect('register')

            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Log in the user
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)

            # Add a success message
            messages.success(request, 'Registration successful. You are now logged in.')

            # Redirect to a success page or any other page you want
            return redirect('login')  # Change 'login' to your actual login URL

        return render(request, 'register.html', {})
    else:
        return redirect('/')
    


def contact_owner(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        message = request.POST.get('message')
        username = request.POST.get('owner')
        owner = User.objects.filter(id = username).first()

        # Create a Contact instance and save it to the database
        contact = Contact(
            owner = owner,
            name=name,
            email=email,
            contact_number=contact_number,
            message=message
        )
        contact.save()

        # Redirect or perform other actions after saving to the database
        return redirect('/')  # Change 'success_url' to your actual success URL

    return render(request, 'propertyDetail.html', {})


def messages(request):
    if request.user.is_authenticated:
        messages = Contact.objects.filter(owner = request.user)
        return render(request,'viewMessage.html',{'messages':messages})
    else:
        return redirect('/')


def messageDetail(request,pk): 
    message = Contact.objects.filter(pk =pk).first()
    return render(request,'messageDetail.html',{'message':message})


def logout_view(request):
    logout(request)
    return redirect('/') 


def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            fm =form.save(commit=False)
            fm.owner = request.user
            fm.save()
            # messages.success(request,'Property Listed')
            return redirect('property_create')
    else:
        form = PropertyForm()
    return render(request, 'RegisterProperty.html', {'form': form})



def property_update(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = PropertyForm(instance=property)
    return render(request, 'RegisterProperty.html', {'form': form})