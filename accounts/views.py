from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import RegisterForm, UserUpdateForm
from .models import Account
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

# ACTIVATION ACCOUNT
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name   = form.cleaned_data['first_name']
            last_name    = form.cleaned_data['last_name']
            email        = form.cleaned_data['email']
            country      = form.cleaned_data['country']
            password     = form.cleaned_data['password']
            username     = email.split('@')[0]
            phone_number = form.cleaned_data['phone_number']

            user = Account.objects.create_user(
                first_name = first_name,
                last_name  = last_name,
                email      = email,
                username   = username,
                country    =country,
                password   =password
            )
            user.phone_number = phone_number
            user.save()
            #User Activate
            domain_name   = get_current_site(request)
            email_subject = 'Please Activate Your Account'
            message       = render_to_string('accounts/account_verification_email.html', {
                'user':user,
                'domain':domain_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email  = email
            send_mail = EmailMessage(email_subject, message, to=[to_email])
            send_mail.send()
            login_url = reverse('accounts:login')  # Resolves to /account/login/
            redirect_url = f"{login_url}?command=verification&mail={email}"
            return HttpResponseRedirect(redirect_url)
    else:
        form = RegisterForm()
    
    context = {
        'form':form
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login is successfully')
            return redirect('store:home')
        else:
            messages.error(request, 'Invalid Login')
            return redirect('accounts:login')
    
    return render(request, 'accounts/login.html')


def activate(request, uidb64, token):
    try:
        uid  = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is activated')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Your Account is not active, Please again.')
        return redirect('accounts:register')



def logout(request):
    auth_logout(request)
    return redirect('accounts:login')




@login_required
def update_profile(request):
    user = request.user
    print("User instance type:", type(user))
    print(user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            print("✅ Updated account:", Account.__dict__)
            user.save(force_update=True)
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('accounts:update_profile') 
        else:
            print("❌ Form errors:", form.errors)
    else:
        form = UserUpdateForm(instance=user)
    
    return render(request, 'accounts/update_profile.html', {'form': form})
 
















































































