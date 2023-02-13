from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib import messages 
from  django.contrib.auth.models import User
from .forms import SignUpForm, EditProfileForm
from .models import Admin, Car, Body, Cylinder, Engine
from .forms import CustomerForm
from .models import Customer


# Create your views here.
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


def customer_view(request):
	if request.method == 'POST':
		val = request.POST.get('add_car_review')
		if val == 'add_car_review':
			form = CustomerForm(request.POST)
			if form.is_valid():
				name = form.cleaned_data.get('name')
				license = form.cleaned_data.get('lisence')
				age1 = form.cleaned_data.get('age')
				gender1 = form.cleaned_data.get('gender')
				customer_obj = Body.objects.filter(Customer_Name=name,License_No=license,age = age1,gender = gender1).first()
				if customer_obj==None:
					Customer.objects.create(Customer_Name=name, License_No=license, age = age1,gender = gender1)
					messages.success(request,("New customer added successfully"))
				#form1 = Reviewform()
				return render(request, 'customer.html', {'form': form})
	
	else:
		form = CustomerForm()
		return render(request, 'customer.html', {'form': form})
	

# cylinder -> engine , body, Car
def add_car(request):
	if request.method =='POST':
		body_obj = Body.objects.filter(boot_space=request.POST['Boot_Space'], ground_clearance=request.POST['Ground_Clearance'], body_type = request.POST['Body_Type'],no_of_doors=request.POST['no_of_doors']).first()
		if body_obj==None:
			body_obj = Body()
			body_obj.boot_space  = request.POST['Boot_Space']
			body_obj.ground_clearance  = request.POST['Ground_Clearance']
			body_obj.body_type = request.POST['Body_Type']
			body_obj.no_of_doors = request.POST['no_of_doors']
			body_obj.save()
		cylinder_obj = Cylinder.objects.filter(no_of_cylinders=request.POST['no_of_cylinders'],config=request.POST['config'], valves_per_cylinder=request.POST['valves_per_cylinder']).first()
		if cylinder_obj==None:
			cylinder_obj = Cylinder()
			cylinder_obj.config  = request.POST['config']
			cylinder_obj.no_of_cylinders  = request.POST['no_of_cylinders']
			cylinder_obj.valves_per_cylinder  = request.POST['valves_per_cylinder']
			cylinder_obj.save()
		print(cylinder_obj.id)
		engine_obj = Engine.objects.filter(cc=request.POST['cc'], fuel_system_type=request.POST['fuel_system_type'], capacity = request.POST['capacity'],fuel_type=request.POST['fuel_type'], id = cylinder_obj).first()
		if engine_obj==None:
			engine_obj = Engine()
			engine_obj.cc=request.POST['cc']
			engine_obj.fuel_system_type=request.POST['fuel_system_type']
			engine_obj.capacity = request.POST['capacity']
			engine_obj.fuel_type=request.POST['fuel_type']
			engine_obj.id = cylinder_obj
			engine_obj.save()
		obj1 = Car()
		obj1.variant = request.POST['variant']
		obj1.Model = request.POST['Model']
		obj1.Make = request.POST['Model']
		obj1.kerb_weight = request.POST['kerb_weight']
		obj1.Type = request.POST['Type']
		obj1.Mileage = request.POST['Mileage']
		admin_obj1 = Admin.objects.get(Admin_ID_id=request.user)
		obj1.Admin_ID = admin_obj1
		obj1.Engine_ID = engine_obj
		obj1.Body_ID = body_obj
		obj1.save()
		return render(request, 'sample.html')
	else:
		return render(request, 'sample.html')

def update(request):
	if request.method == 'POST':
		val = request.POST.get('form1')
		if val=='form1':
			cid = request.POST.get('car_id')
			car_obj = Car.objects.filter(Car_ID=cid).first()
			if(car_obj==None):
				return render(request, 'update.html',{'error':1,'errormsg':"Invalid Car ID"})	
			engine_obj = car_obj.Engine_ID
			body_obj = car_obj.Body_ID
			cylinder_obj = engine_obj.id
			context = {'show':1,'variant':car_obj.variant,'Type':car_obj.Type,'Make':car_obj.Make,'Mileage':car_obj.Mileage,'Model':car_obj.Model,'kerb_weight':car_obj.kerb_weight,'fuel_system_type':engine_obj.fuel_system_type,'fuel_type':engine_obj.fuel_type,'cc':engine_obj.cc,'capacity':engine_obj.capacity,'no_of_cylinders':cylinder_obj.no_of_cylinders,'valves_per_cylinder':cylinder_obj.valves_per_cylinder,'config':cylinder_obj.config,'body_type':body_obj.body_type,'boot_space':body_obj.boot_space,'ground_clearance':body_obj.ground_clearance,'no_of_doors':body_obj.no_of_doors,'cid':cid}
			return render(request, 'update.html',context)
		elif val=='form2':
			body_obj = Body.objects.filter(boot_space=request.POST['Boot_Space'], ground_clearance=request.POST['Ground_Clearance'], body_type = request.POST['Body_Type'],no_of_doors=request.POST['no_of_doors']).first()
			if body_obj==None:
				body_obj = Body()
				body_obj.boot_space  = request.POST['Boot_Space']
				body_obj.ground_clearance  = request.POST['Ground_Clearance']
				body_obj.body_type = request.POST['Body_Type']
				body_obj.no_of_doors = request.POST['no_of_doors']
				body_obj.save()
				body_obj = Body.objects.filter(boot_space=request.POST['Boot_Space'], ground_clearance=request.POST['Ground_Clearance'], body_type = request.POST['Body_Type'],no_of_doors=request.POST['no_of_doors']).first()
			cylinder_obj = Cylinder.objects.filter(no_of_cylinders=request.POST['no_of_cylinders'],config=request.POST['config'], valves_per_cylinder=request.POST['valves_per_cylinder']).first()
			if cylinder_obj==None:
				print('new cylinder')
				cylinder_obj = Cylinder()
				cylinder_obj.config  = request.POST['config']
				cylinder_obj.no_of_cylinders  = request.POST['no_of_cylinders']
				cylinder_obj.valves_per_cylinder  = request.POST['valves_per_cylinder']
				cylinder_obj.save()
				cylinder_obj = Cylinder.objects.filter(no_of_cylinders=request.POST['no_of_cylinders'],config=request.POST['config'], valves_per_cylinder=request.POST['valves_per_cylinder']).first()
			engine_obj = Engine.objects.filter(cc=request.POST['cc'], fuel_system_type=request.POST['fuel_system_type'], capacity = request.POST['capacity'],fuel_type=request.POST['fuel_type'], id = cylinder_obj).first()
			if engine_obj==None:
				print('new engine')
				engine_obj = Engine()
				engine_obj.cc=request.POST['cc']
				engine_obj.fuel_system_type=request.POST['fuel_system_type']
				engine_obj.capacity = request.POST['capacity']
				engine_obj.fuel_type=request.POST['fuel_type']
				engine_obj.id = cylinder_obj
				engine_obj.save()
				engine_obj = Engine.objects.filter(cc=request.POST['cc'], fuel_system_type=request.POST['fuel_system_type'], capacity = request.POST['capacity'],fuel_type=request.POST['fuel_type'], id = cylinder_obj).first()
			print(engine_obj)
			obj1 = Car.objects.get(Car_ID=request.POST.get('cid'))
			obj1.variant = request.POST['variant']
			obj1.Model = request.POST['Model']
			obj1.Make = request.POST['Model']
			obj1.kerb_weight = request.POST['kerb_weight']
			obj1.Type = request.POST['Type']
			obj1.Mileage = request.POST['Mileage']
			admin_obj1 = Admin.objects.get(Admin_ID_id=request.user)
			obj1.Admin_ID = admin_obj1
			obj1.Engine_ID = engine_obj
			obj1.Body_ID = body_obj
			obj1.save()
			return render(request, 'update.html')
	else:
		return render(request, 'update.html',{'show':0})

def home(request):
    if request.user.is_authenticated:
        admin_obj = Admin.objects.get(Admin_ID_id=request.user)
        context = {'sal': admin_obj.salary, 'addr': admin_obj.address, 'phone': admin_obj.Phone_no}
        return render(request, 'authenticate/home.html',context)
    else:
        return render(request, 'authenticate/home.html')