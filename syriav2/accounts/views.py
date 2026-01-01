from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm
from .models import User
from .repositories import UserRepository  
from django.http import JsonResponse

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user_data = form.cleaned_data
            document = request.FILES.get('document')
            
            user = UserRepository.create_user(
                username=user_data['username'],
                password=user_data['password1'],
                phone_number=user_data['phone_number'],
                role=user_data['role'],
                document=document
            )
            
            
            login(request, user)
            messages.success(request, 'تم إنشاء الحساب بنجاح')
           
            if user.role == 'contractor' or user.role == 'system_admin':
                return redirect('accounts:profile')
            else:
             return redirect('home:index')
       
    else:
        form = UserRegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form, 'hide_navbar': True})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'أهلاً وسهلاً')
                if user.role == 'contractor' or user.role == 'system_admin':
                    return redirect('accounts:profile')
                else:
                 return redirect('home:index')
            form.add_error(None, 'اسم المستخدم أو كلمة المرور غير صحيحة')
                
        else:
            
            form.add_error(None, 'اسم المستخدم أو كلمة المرور غير صحيحة')
              
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form, 'hide_navbar': True})


    

@login_required
def logout_view(request):
    messages.success(request, 'تم تسجيل الخروج بنجاح')
    logout(request)
    return redirect('home:index')

@login_required
def profile_view(request):
    user = request.user 
    return render(request, 'accounts/profile.html', {'user': request.user, 'hide_navbar': True})

