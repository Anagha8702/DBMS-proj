from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib import messages 
from  django.contrib.auth.models import User
from .forms import SignUpForm, EditProfileForm
from .models import Admin

# Create your views here.
def index(request):
    return render(request, 'sample.html')

def home(request):
    return render(request, 'authenticate/home.html')

def login_user (request):
	if request.method == 'POST': #if someone fills out form , Post it 
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:# if user exist
			login(request, user)
			messages.success(request,('Youre logged in'))
			return redirect('home') #routes to 'home' on successful login  
		else:
			messages.success(request,('Error logging in'))
			return redirect('login') #re routes to login page upon unsucessful login
	else:
		return render(request, 'authenticate/login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request,('Youre now logged out'))
	return redirect('home')

def register_user(request):
	if request.method =='POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			print(form.cleaned_data['email'])
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request,user)
			val1 = request.POST['salary']
			val2 = request.POST['addr']
			val4 = request.POST['ph']
			val3 = request.user
			print(val1,val2,val3)
			obj = Admin()
			obj.Admin_ID=val3
			obj.salary=val1
			obj.address=val2
			obj.Phone_no=val4
			obj.save()
			messages.success(request, ('Youre now registered'))
			return redirect('home')
	else: 
		form = SignUpForm()
	

	context = {'form': form}
	return render(request, 'authenticate/register.html', context)


def edit_profile(request):
	if request.method =='POST':
		form = EditProfileForm(request.POST, instance=request.user) 
		if form.is_valid():
			user_form = form.save()
			val1 = request.POST['salary']
			val2 = request.POST['addr']
			val4 = request.POST['ph']
			#val3 = request.user
			admin_obj = Admin.objects.get(Admin_ID_id=request.user)
			admin_obj.salary = val1
			admin_obj.Phone_no = val4
			admin_obj.address = val2
			admin_obj.save()
			messages.success(request, ('You have edited your profile'))
			return redirect('home')
	else: 		#passes in user information 
	
		form = EditProfileForm(instance= request.user)
	context = {'form': form,
	 }
	return render(request, 'authenticate/edit_profile.html', context)
	#return render(request, 'authenticate/edit_profile.html',{})



def change_password(request):
	if request.method =='POST':
		form = PasswordChangeForm(data=request.POST, user= request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('You have edited your password'))
			return redirect('home')
	else: 		#passes in user information 
		form = PasswordChangeForm(user= request.user) 

	context = {'form': form}
	return render(request, 'authenticate/change_password.html', context)