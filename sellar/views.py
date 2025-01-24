from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import (
    CustomUserCreationForm, ManufacturerForm,
    MachineVendorForm, ProfessionalWorkerForm, UserTypeLoginForm
)
from .models import CustomUser, ManufacturerOrProductSeller, MachineVendor, ProfessionalWorker
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)

# Utility function to generate unique IDs
def generate_unique_id():
    while True:
        unique_id = get_random_string(8)
        if not ManufacturerOrProductSeller.objects.filter(unique_vendor_id=unique_id).exists() and \
           not MachineVendor.objects.filter(unique_vendor_id=unique_id).exists() and \
           not ProfessionalWorker.objects.filter(unique_vendor_id=unique_id).exists():
            return unique_id


# Register View
def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            messages.success(request, 'Account created successfully')
            if user.user_type == 'manufacturer':
                return redirect('manufacturer_form')
            elif user.user_type == 'machine_vendor':
                return redirect('machine_vendor_form')
            elif user.user_type == 'professional_worker':
                return redirect('professional_worker_form')
        else:
            messages.error(request, 'Error creating account. Please correct the errors below.')
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


# Manufacturer Form View
@login_required(login_url='login')
def manufacturer_form(request):
    if request.method == 'POST':
        form = ManufacturerForm(request.POST, request.FILES)
        if form.is_valid():
            manufacturer = form.save(commit=False)
            manufacturer.user = request.user
            manufacturer.unique_vendor_id = generate_unique_id()
            manufacturer.save()
            messages.success(request, 'Manufacturer profile created successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ManufacturerForm()
    return render(request, 'registration/manufacturer_form.html', {'form': form})


# Machine Vendor Form View
@login_required(login_url='login')
def machine_vendor_form(request):
    if request.method == 'POST':
        form = MachineVendorForm(request.POST, request.FILES)
        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.user = request.user
            vendor.unique_vendor_id = generate_unique_id()
            vendor.save()
            messages.success(request, 'Machine vendor profile created successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = MachineVendorForm()
    return render(request, 'registration/machine_vendor_form.html', {'form': form})


# Professional Worker Form View
@login_required(login_url='login')
def professional_worker_form(request):
    if request.method == 'POST':
        form = ProfessionalWorkerForm(request.POST, request.FILES)
        if form.is_valid():
            worker = form.save(commit=False)
            worker.user = request.user
            worker.unique_vendor_id = generate_unique_id()
            worker.save()
            messages.success(request, 'Professional worker profile created successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfessionalWorkerForm()
    return render(request, 'registration/professional_worker_form.html', {'form': form})


# Login View

def login_view(request):
    if request.method == 'POST':
        form = UserTypeLoginForm(request.POST)
        logger.debug(f"POST data received: {request.POST}")
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            try:
                # Get the user from CustomUser model
                custom_user = CustomUser.objects.get(username=username)
                logger.debug(f"Found user: {username}, user type: {custom_user.user_type}")
                
                # Verify password using CustomUser's password field
                if custom_user.password == password:  # Direct password comparison
                    if custom_user.is_active:
                        # Login successful
                        login(request, custom_user)
                        logger.info(f"Login successful for user: {username}")
                        
                        # Handle user type specific redirection
                        if custom_user.user_type == 'manufacturer':
                            return redirect('profile')
                        elif custom_user.user_type == 'machine_vendor':
                            return redirect('profile')
                        elif custom_user.user_type == 'professional_worker':
                            return redirect('profile')
                        else:
                            logger.error(f"Invalid user type: {custom_user.user_type}")
                            messages.error(request, "Invalid user type")
                    else:
                        logger.error("Account is inactive")
                        messages.error(request, "Your account is not active")
                else:
                    logger.error("Password verification failed")
                    messages.error(request, "Invalid username or password")
                    
            except CustomUser.DoesNotExist:
                logger.error(f"User not found: {username}")
                messages.error(request, "Invalid username or password")
            except Exception as e:
                logger.error(f"Login error: {str(e)}")
                messages.error(request, "An error occurred during login")
        else:
            logger.error(f"Form validation errors: {form.errors}")
            messages.error(request, "Please correct the form errors")
    else:
        form = UserTypeLoginForm()
    
    return render(request, 'registration/login.html', {'form': form})
# Profile View
@login_required(login_url='login')
def profile_view(request):
    user = request.user
    profile = None
    try:
        if user.user_type == 'manufacturer':
            profile = ManufacturerOrProductSeller.objects.get(user=request.user)
        elif user.user_type == 'machine_vendor':
            profile = MachineVendor.objects.get(user=request.user)
        elif user.user_type == 'professional_worker':
            profile = ProfessionalWorker.objects.get(user=request.user)
    except (ManufacturerOrProductSeller.DoesNotExist, MachineVendor.DoesNotExist, ProfessionalWorker.DoesNotExist):
        messages.error(request, 'Profile not found.')
        return redirect('some_error_page')  # Replace with a valid fallback.
    return render(request, 'registration/profile.html', {'profile': profile, 'user': user})
