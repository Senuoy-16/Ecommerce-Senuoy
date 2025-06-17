from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from lockdown.decorators import lockdown

@lockdown()
@login_required
def home(request):
    return render(request, 'tombola/home.html')
