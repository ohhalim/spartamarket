from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, ProfileForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import User

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('products:product_list')
    else:
        form = SignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('products:product_list')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('products:product_list')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:login')

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    is_following = request.user.follows.filter(pk=profile_user.pk).exists()
    
    context = {
        'profile_user': profile_user,
        'is_following': is_following,
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def profile_edit(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', username=username)
    else:
        form = ProfileForm(instance=user)
    
    return render(request, 'accounts/profile_edit.html', {'form': form})

@login_required
def follow_view(request, username):
    target_user = get_object_or_404(User, username=username)
    if target_user != request.user:
        if request.user.follows.filter(pk=target_user.pk).exists():
            request.user.follows.remove(target_user)
        else:
            request.user.follows.add(target_user)
    return redirect('accounts:profile', username=username)