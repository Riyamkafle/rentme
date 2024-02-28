from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .models import *
from .forms import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.contrib.auth.models import User
from .models import Property, BookProperty
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from reportlab.pdfgen import canvas

# Create your views here.

import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import linear_kernel
import joblib
# Function to get recommendations based on item index
def get_recommendations(item_index, cosine_similarities=None):
    file_path = "ds_new.csv"
    df = pd.read_csv(file_path)
    if cosine_similarities is None:
        # Load the saved cosine similarity matrix
        cosine_similarities = joblib.load("cosine_similarity_model.joblib")    
    sim_scores = list(enumerate(cosine_similarities[item_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:4]  # Top 5 recommendations (excluding itself)
    item_indices = [i[0] for i in sim_scores]
    return item_indices
    # return df['title'].iloc[item_indices]
    
index_to_recommend = 2
recommendations = get_recommendations(index_to_recommend)

def index(request):
    properties_list = Property.objects.filter(available_for_rent=True, is_approved=True)

    search = request.GET.get('search')
    from_ = request.GET.get('from')
    to_ = request.GET.get('to')
    location = request.GET.get('location')

    if from_ and to_:
        properties_list = properties_list.filter(price__gte=from_, price__lt=to_)
    elif from_:
        properties_list = properties_list.filter(price__gte=from_)
    elif to_:
        properties_list = properties_list.filter(price__lt=to_)

    if location:
        properties_list = properties_list.filter(location=location)

    if search:
        properties_list = properties_list.filter(title__icontains=search)

    # Pagination
    paginator = Paginator(properties_list, 10)  # Show 10 properties per page
    page_number = request.GET.get('page')
    try:
        properties = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        properties = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        properties = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'properties': properties})    


def propertyDetail(request,id):
    if request.user.is_authenticated:
        try : 
            property = Property.objects.get(pk = id)
            if not property.id > 43:
                
                items_to_recommend = get_recommendations(property.id)
                print(items_to_recommend)
                recommended_property = Property.objects.filter(id__in= items_to_recommend)
                print(recommended_property)
            else:
                recommended_property = None
        except Exception as e: 
            print(e)
            return redirect('/')
        return render(request,'propertyDetail.html',{'property':property,'recommended_property':recommended_property})
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
            phone = request.POST.get('phone')

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
            phone = Phone(user = user,phone = phone)
            phone.save()

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


def message(request):
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
            messages.success(request,'Property Listed')
            return redirect('property_create')
    else:
        form = PropertyForm()
    return render(request, 'RegisterProperty.html', {'form': form})



def property_update(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if property.owner !=request.user:
        return redirect('/')
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request,"property updated")
            return redirect('/propertyList/')
    else:
        form = PropertyForm(instance=property)
    return render(request, 'RegisterProperty.html', {'form': form})

def property_delete(request, pk):
    property = get_object_or_404(Property, pk=pk)
    
    property.delete()
    messages.success(request,"property deleted")

    return redirect('/propertyList/')
    

def propertyList(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            properties = Property.objects.all()

        else:
            
            properties = Property.objects.filter(owner = request.user)
        return render(request,'propertyList.html',{'properties':properties})
    else:
        return redirect('/')
    


def bookproperty(request):
     if request.method == "POST": 
        owner = request.POST.get('owner')
        property = request.POST.get('property') 
        owner_ = User.objects.filter(pk =owner).first()
        property_ = Property.objects.filter(pk = property).first()
        property_.available_for_rent = False
        phone = Phone.objects.filter(user = request.user).first()
        book = BookProperty(property = property_,renter = request.user,owner = owner_,renter_phone= phone.phone)
        book.save()
        property_.save()
        pdf_response = generate_pdf_report(book)
        messages.success(request,'booked successfully')
        return redirect(f'/property/{property}/')

     
        

def generate_pdf_report(book):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{book.property.title}_report.pdf"'

    # Create the PDF content using ReportLab
    pdf = canvas.Canvas(response)

    # Add big title "Home Rental Receipt"
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(100, 800, "Home Rental Receipt")

    # Add property details
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 770, f"Property Title: {book.property.title}")
    pdf.drawString(100, 730, f"Location: {book.property.location}")
    pdf.drawString(100, 710, f"Price: {book.property.price}")
    pdf.drawString(100, 750, f"Property Description: {book.property.description}") 
    pdf.drawString(100, 690, f"Bedrooms: {book.property.bedrooms}")
    pdf.drawString(100, 670, f"Bathrooms: {book.property.bathrooms}")
    pdf.drawString(100, 650, f"Owner: {book.owner.username}")
    pdf.drawString(100, 630, f"Renter: {book.renter.username}")
    # Add more fields as needed

    # Save the PDF
    pdf.showPage()
    pdf.save()

    return response     

def orderlist(request): 
    orders = BookProperty.objects.filter(owner = request.user)
    return render(request,'orderlist.html',{'orders':orders})



def aboutus(request): 
    return render(request,'about.html')



@login_required
def update_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')  # Get phone number from the form
        
        # Update user profile
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        
        # Update phone number
        phone_obj, created = Phone.objects.get_or_create(user=user)
        phone_obj.phone = phone
        phone_obj.save()
        
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('update_profile')  # Redirect to the same page to clear form data
        
    context = {"firstname":request.user.first_name,
               "lastname":request.user.last_name,
               "email":request.user.email,
               "phone":Phone.objects.filter(user = request.user).first().phone
               }

    return render(request, 'updateProfile.html',context)



def dashboardPropertyListing(request):
    if request.user.is_superuser:
        properties_list = Property.objects.filter(is_approved=False)
        
        # Pagination
        paginator = Paginator(properties_list, 10)  # Show 10 properties per page
        page_number = request.GET.get('page')
        try:
            properties = paginator.page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            properties = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            properties = paginator.page(paginator.num_pages)
        
        if request.method == "POST":
            property_id = request.POST.get('propertyId')
            property_ = Property.objects.filter(pk=property_id).first()
            if property_:
                property_.is_approved = True
                if not property_.available_for_rent:
                    property_.available_for_rent = True
                property_.save()
                messages.success(request, 'Property approved')
                return redirect('dashboardProductListing')

        return render(request, 'adminPropertyListing.html', {'properties': properties})
    else:
        return redirect("/")
    
    
    
    
    
def adminorderlist(request):
    if request.user.is_superuser:
        orders_list = BookProperty.objects.filter(owner=request.user)
        
        # Pagination
        paginator = Paginator(orders_list, 10)  # Show 10 orders per page
        page_number = request.GET.get('page')
        try:
            orders = paginator.page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            orders = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            orders = paginator.page(paginator.num_pages)

        return render(request, 'adminorderlist.html', {'orders': orders})
    else:
        return redirect('/')
    
    
    
def adminpropertyList(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            properties_list = Property.objects.all()
        else:
            properties_list = Property.objects.filter(owner=request.user)
        
        # Pagination
        paginator = Paginator(properties_list, 10)  # Show 10 properties per page
        page_number = request.GET.get('page')
        try:
            properties = paginator.page(page_number)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            properties = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            properties = paginator.page(paginator.num_pages)

        return render(request, 'adminmanageproperty.html', {'properties': properties})
    else:
        return redirect('/')