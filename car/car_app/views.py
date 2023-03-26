from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib import messages 
from  django.contrib.auth.models import User
from .forms import SignUpForm, EditProfileForm
from .models import Admin, Car, Body, Cylinder, Engine, Customer, Bought_by
from .forms import CustomerForm
import firebase_admin
from firebase_admin import credentials,db
import sqlite3
import json
import math
import nltk
#nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

# Create your views here.
def login_user (request):
	if request.method == 'POST': #if someone fills out form , Post it 
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None: #if user exist
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

def powerbi(request):
	return render(request, 'powerbi.html')

def custom(request):
	return render(request, 'custom.html')

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
		admin_obj = Admin.objects.get(Admin_ID_id=request.user)
		form = EditProfileForm(instance= request.user)
		v1 = admin_obj.address
		v2 = admin_obj.Phone_no
		context = {'form': form, 'sal':admin_obj.salary,'addr1': v1[:len(v1)-1],'ph1' :v2[:len(v2)-1],
	 	}
		print(admin_obj.address, admin_obj.salary)
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
	global customer_obj
	if request.method == 'POST':
		val = request.POST.get('add_car_review')
		if val == 'add_car_review':
			form = CustomerForm(request.POST)
			if form.is_valid():
				name = form.cleaned_data.get('name')
				license = form.cleaned_data.get('lisence')
				age1 = form.cleaned_data.get('age')
				gender1 = form.cleaned_data.get('gender')
				customer_obj = Customer.objects.filter(Customer_Name=name,License_No=license,age = age1,gender = gender1).first()
				if customer_obj==None:
					Customer.objects.create(Customer_Name=name, License_No=license, age = age1,gender = gender1)
					customer_obj = Customer.objects.filter(Customer_Name=name,License_No=license,age = age1,gender = gender1).first()
					print(customer_obj)
					messages.success(request,("New customer added successfully"))
				return render(request, 'customer.html', {'form': form, 'show':1, 'cid':customer_obj.Customer_ID})
		elif val == 'car_review':
			form = CustomerForm()
			rate = request.POST.get('rating')
			model = request.POST.get('Model')
			variant = request.POST.get('Variant')
			make = request.POST.get('Make')
			review = request.POST.get('review')
			print("cid",request.POST.get('cid'))
			customer_obj1 = Customer.objects.filter(Customer_ID = request.POST.get('cid')).first()
			print(customer_obj1)
			car_obj = Car.objects.filter(Make=make,variant=variant,Model=model).first()
			if car_obj==None:
				return render(request, 'customer.html',{'form': form, 'show':0,'error':1,'errormsg':"Register Car Details First"})		
			bought_by_obj = Bought_by.objects.create(Car_ID=car_obj,Customer_ID=customer_obj1,rating=rate)
			try:
				cred = credentials.Certificate(r"car_app/a.json")
				firebase_admin.initialize_app(cred, {'databaseURL': 'https://cardata-413aa-default-rtdb.asia-southeast1.firebasedatabase.app'})
				ref = db.reference("/Data")
				ref1 = ref.child(str(car_obj.Car_ID))
				ref1.push().set({
				car_obj.Car_ID: review
				})
			except:
				ref = db.reference("/Data")
				ref1 = ref.child(str(car_obj.Car_ID))
				ref1.push().set({
				car_obj.Car_ID: review
				})
			#ref = db.reference()
			return render(request, 'customer.html', {'form': form, 'show':0})
	else:
		form = CustomerForm()
		return render(request, 'customer.html', {'form': form, 'show':0})
	

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
			body_obj = Body.objects.filter(boot_space=request.POST['Boot_Space'], ground_clearance=request.POST['Ground_Clearance'], body_type = request.POST['Body_Type'],no_of_doors=request.POST['no_of_doors']).first()
		cylinder_obj = Cylinder.objects.filter(no_of_cylinders=request.POST['no_of_cylinders'],config=request.POST['config'], valves_per_cylinder=request.POST['valves_per_cylinder']).first()
		if cylinder_obj==None:
			cylinder_obj = Cylinder()
			cylinder_obj.config  = request.POST['config']
			cylinder_obj.no_of_cylinders  = request.POST['no_of_cylinders']
			cylinder_obj.valves_per_cylinder  = request.POST['valves_per_cylinder']
			cylinder_obj.save()
			cylinder_obj = Cylinder.objects.filter(no_of_cylinders=request.POST['no_of_cylinders'],config=request.POST['config'], valves_per_cylinder=request.POST['valves_per_cylinder']).first()
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
			engine_obj = Engine.objects.filter(cc=request.POST['cc'], fuel_system_type=request.POST['fuel_system_type'], capacity = request.POST['capacity'],fuel_type=request.POST['fuel_type'], id = cylinder_obj).first()
		obj1 = Car()
		obj1.variant = request.POST['variant']
		obj1.Model = request.POST['Model']
		obj1.Make = request.POST['Make']
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
		if(request.method == 'POST'):
			cid = request.POST.get('id')
			print(cid)
			try:
				cred = credentials.Certificate(r"car_app/a.json")
				firebase_admin.initialize_app(cred, {'databaseURL': 'https://cardata-413aa-default-rtdb.asia-southeast1.firebasedatabase.app'})
				ref = db.reference("/Data")
				car_reviews_ref = ref.child(str(cid))
				x = car_reviews_ref.get()
				review = []
				for i in x.values():
					review.append(i[str(cid)])
				print(review)
			except:
				ref = db.reference("/Data")
				car_reviews_ref = ref.child(str(cid))
				x = car_reviews_ref.get()
				review = []
				for i in x.values():
					review.append(i[str(cid)])
				print(review)
			sia = SentimentIntensityAnalyzer()
			review_val = []
			label = []
			for review1 in review:
				score = sia.polarity_scores(str(review1))
				x1 = math.floor(score['compound']*100)
				review_val.append(x1)
				label.append('')

			print(review_val)

			admin_obj = Admin.objects.get(Admin_ID_id=request.user)
			context = {'sal': admin_obj.salary, 'addr': admin_obj.address, 'phone': admin_obj.Phone_no,'review_val':review_val,'show':1,'cid':cid,'lab':json.dumps(label)}
			return render(request, 'authenticate/home.html',context)
		else:
			admin_obj = Admin.objects.get(Admin_ID_id=request.user)
			context = {'sal': admin_obj.salary, 'addr': admin_obj.address, 'phone': admin_obj.Phone_no}
			return render(request, 'authenticate/home.html',context)
	else:
		return render(request, 'authenticate/home.html')


def custom(request):
    global x1,x2,x3,x4,y1,y3,lineM,lineF,y4
    if(request.method == 'POST'):
        xAxis = request.POST.get('dropdown1')
        yAxis= request.POST.get('dropdown2')
        print(xAxis,yAxis)
        
        print("hi")
        xQuery = ""
        xGroup = ""
        if xAxis == 'Make':
            xQuery = "SELECT c.Make"
            xGroup = "GROUP BY c.Make;"
        elif xAxis == 'Model':
            xQuery = "SELECT c.Model"
            xGroup = "GROUP BY c.Model;"
        elif xAxis == 'Varient':
            xQuery = "SELECT c.variant"
            xGroup = "GROUP BY c.variant;"
        
        joinQuery = ""
        if yAxis == "cc" or yAxis == "capacity":
            joinQuery = "INNER JOIN car_app_engine as e "+"ON c.Engine_ID_id = e.Engine_ID"
        elif yAxis == 'no_of_doors' or yAxis == 'boot_space' or yAxis == 'ground_clearance':
            joinQuery = "INNER JOIN car_app_body as b ON c.Body_ID_id = b.Body_ID"
        elif yAxis == 'no_of_cylinders' or yAxis == 'valves_per_cylinder':
            joinQuery = "INNER JOIN car_app_engine AS e INNER JOIN car_app_cylinder as cy ON c.Engine_ID_id = e.Engine_ID and cy.id = e.id_id"
            
        yValue = "AVG("+yAxis+") \n"
        mainQuery = xQuery+","+yValue+"FROM car_app_car AS c\n"+joinQuery+"\n"+xGroup
        print(mainQuery)
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        print(mainQuery)
        cursor.execute(mainQuery)
        results = cursor.fetchall()
        conn.close()
        x = []
        y = []
        
        for i in results:
            x.append(i[0])
            y.append(i[1])
        #print(x,y)

        # temp = results[0]
        return render(request,'custom.html',{'x':x,'y':y,'x1':json.dumps(x1),'y1':y1,'x2':x2,'linem':lineM, 'linef': lineF,'x3':x3,'y3':y3,'x4':x4,'y4':y4, 'show':1})
        # return render(request,'custom.html')
    else:
        #print("HI")
        # age of customer vs car body type
        q4="SELECT b.body_type,AVG(cu.age)\nFROM car_app_car AS c\nINNER JOIN car_app_body AS b\nINNER JOIN car_app_bought_by AS bb\nINNER JOIN car_app_customer AS cu \nON c.Body_ID_id = b.Body_ID and bb.Customer_ID_id = cu.Customer_ID and bb.Car_ID_id = c.Car_ID\nGROUP BY b.body_type;"
        #print(q4)
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute(q4)
        results1 = cursor.fetchall()
        conn.close()
        x1=[]
        y1=[]
        for i in results1:
            x1.append(i[0])
            y1.append(i[1])
            
        
        #gender vs car body type
        q5="select b.body_type,cu.gender,count(cu.gender) FROM car_app_car as c INNER JOIN car_app_body as b INNER JOIN car_app_bought_by as bb INNER JOIN car_app_customer as cu ON c.Body_ID_id = b.Body_ID and bb.Customer_ID_id = cu.Customer_ID and bb.Car_ID_id = c.Car_ID group by b.body_type,cu.gender;"
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute(q5)
        results2 = cursor.fetchall()
        conn.close()
        dict={}
        bodyTypeSet = set()
        x2 = []
        lineM = []
        lineF = []
        for i in results2:
            dict.update({i[0]:{}})
            bodyTypeSet.add(i[0])
        for i in results2:
            dict[i[0]].update({i[1]:i[2]})
        for i in results2:
            dict[i[0]].update({i[1]:i[2]})
    
        for i in bodyTypeSet:
            x2.append(i)
            if 'M' in dict[i].keys():
                lineM.append(dict[i]['M'])
            else:
                lineM.append(0) 			
            if 'F' in dict[i].keys():
                lineF.append(dict[i]['F'])
            else:
                lineF.append(0)
        print(results2,x2,lineM,lineF)



		# fuel type vs mileage	
        q7="select e.fuel_type,avg(c.Mileage) FROM car_app_car as c INNER JOIN car_app_engine as e ON c.Engine_ID_id = e.Engine_ID group by e.fuel_type;"
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute(q7)
        results3 = cursor.fetchall()
        conn.close()
        x3 = []
        y3 = []
        for i in results3:
            x3.append(i[0])
            y3.append(i[1])
        print(x3,y3)


		#feul system type vs capacity
        q9="select e.fuel_system_type,avg(e.capacity) FROM car_app_engine as e group by e.fuel_system_type;"
				
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        cursor.execute(q9)
        results4 = cursor.fetchall()
        conn.close()
        x4 = []
        y4 = []
        for i in results4:
            x4.append(i[0])
            y4.append(i[1])
        print(x4,y4)
        return render(request,'custom.html',{'x1':json.dumps(x1),'y1':y1,'x2':x2,'linem':lineM, 'linef': lineF,'x3':x3,'y3':y3,'x4':x4,'y4':y4, 'x':[],'y':[],'show':0 })
        # return render(request,'custom.html')