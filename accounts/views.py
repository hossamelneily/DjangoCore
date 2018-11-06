from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth import get_user_model
from django.db.models import Q

User =get_user_model()

from .forms import LoginForm

def login_user(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        user_obj = form.cleaned_data.get('user_obj')
        # user_obj = User.objects.get(
        #     Q(username__iexact=query) |
        #     Q(email__iexact=query)
        # )
        # if request.user.is_authenticated:
        print("user is logged")
        # print(request.user.is_authenticated)
        login(request,user_obj)
        # print(request.user.is_authenticated)
        return redirect('/')
    context ={
        'form':form
    }

    return render(request,'test_form.html',context)




def logout_user(request):
    logout(request)
    return redirect('/login')