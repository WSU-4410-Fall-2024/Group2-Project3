from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm  # Import this for the registration form
from django.contrib import messages

from .models import Review
from .forms import ReviewForm

from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm


# Home view (already defined)
def home(request):
    context = {}
    return render(request, "myApp/home.html", context)

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'myApp/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('home')


# About Us view (newly added)
def about_us(request):
    return render(request, 'myApp/about_us.html')






def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            # Send the welcome email
            send_mail(
                'Welcome to Find One!',
                'Thank you for registering with Find One. We are excited to have you on board!',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            messages.success(request, "Your account has been created successfully! You can now log in.")
            return redirect("login")  # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, "myApp/register.html", {"form": form})



# views.py

def review_us(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Associate review with the logged-in user
            review.save()
            return redirect('review_us')  # Redirect to the same page after submitting the review
    else:
        form = ReviewForm()

    reviews = Review.objects.all()  # Fetch all reviews to display
    return render(request, 'myApp/review_us.html', {'form': form, 'reviews': reviews})





# @login_required  # Ensure only logged-in users can access the quiz
# def quiz(request):
#     if request.method == 'POST':
#         # Fetch data from the form submission
#         recipient = request.POST.get('recipient')
#         gender = request.POST.get('gender')
#         age = request.POST.get('age')
#         occasion = request.POST.get('occasion')
#         weekend_activities = request.POST.get('weekend_activities')
#         # personality = request.POST.get('personality')
#         stores = request.POST.get('stores')
#         # price_range = request.POST.get('price_range')

#         # Logic to redirect based on store selection
#         store_urls = {
#             "amazon": "https://www.amazon.com/s?k=",
#             "walmart": "https://www.walmart.com/search/?query=",
#             "target": "https://www.target.com/s?searchTerm="
#         }

#         # Create a search query using the quiz data
#         # search_query = f"{recipient} {occasion} gift {gender} {age} years {weekend_activities} {personality}".replace(" ", "+")
#         search_query = f"{recipient} {occasion} gift {gender} {age} years {weekend_activities}".replace(" ", "+")

#         selected_store_url = store_urls.get(stores, "#") + search_query

#         # Redirect the user to the generated store URL
#         return redirect(selected_store_url)

#     return render(request, 'myApp/quiz.html')


# //duplicate


from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render

@login_required
def quiz(request):
    if request.method == 'POST':
        # Fetch data from the form submission
        weekend_activities = request.POST.get('weekend_activities', '')
        price_range = request.POST.get('price_range', '')

        # Validate the input data (optional)
        if not weekend_activities or not price_range:
            messages.error(request, "Please select a weekend activity and a price range.")
            return redirect('quiz')

        # Store URLs for redirection
        store_urls = {
            "amazon": "https://www.amazon.com/s?k=",
            "walmart": "https://www.walmart.com/search/?query=",
            "target": "https://www.target.com/s?searchTerm=",
        }

        # Get the selected store
        stores = request.POST.get('stores', 'amazon')  # Default to Amazon if none is selected

        # Generate the search query
        search_query = f"{weekend_activities} {price_range}".replace(" ", "+")
        selected_store_url = store_urls.get(stores, "#") + search_query

        # Redirect the user directly to the generated store URL
        return redirect(selected_store_url)

    return render(request, 'myApp/quiz.html')






