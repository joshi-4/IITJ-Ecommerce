from django.shortcuts import render, redirect
from users import forms
from django.contrib.auth.models import User
from django.contrib import auth
from users.models import account, item
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
	return render(request, 'users/index.html')

def aboutus(request):
	return render(request, 'users/aboutus.html')

 

# Buy views

def buy(request):

	item_all = item.objects.all().order_by('-createdAt')

	n = len(item_all)
	
	collist = [[],[],[],[]]

	for i in range(n):
		collist[i%4].append(item_all[i])
	
	print("This is the collist")
	print(collist)

	context = { 
		'allitems': item_all,
		'collist':collist,	
	 }

	return render(request, 'users/buy.html', context)


def categorybuy(request, cat = 'OT'):
	print("category:" + cat)

	item_all = item.objects.filter(category = cat).order_by('-createdAt') 
	
	n = len(item_all)
	
	collist = [[],[],[],[]]

	for i in range(n):
		collist[i%4].append(item_all[i])
	
	print("This is the collist")
	print(collist)

	context = { 
		'allitems': item_all,
		'collist':collist,	
	 }


	return render(request,'users/buy.html', context)



# Login, Logout, Register, Profile views

def register(request):

	if request.method == "POST":

		if request.POST['pass'] == request.POST['passagain']:
			try:
				user = User.objects.get(username= request.POST['uname'])
				return render(request, 'users/register.html', {'error': "Username Already exists"})

			except User.DoesNotExist:

				phnum = request.POST['phone']
				address = request.POST['address']
				name = request.POST['name']

				if request.POST['uname'] == '':
					return render(request, 'users/register.html', {'error': "Username is required"})

				if name == '':
					return render(request, 'users/register.html', {'error': "Name is required"})

				if phnum == '':
					return render(request, 'users/register.html', {'error': "Phone Number is required"})

				user = User.objects.create_user(username = request.POST['uname'], password = request.POST['pass'])
				


				newaccount = account(phone_num = phnum, address = address, user = user, name = name)
				newaccount.save()
				auth.login(request, user)

				return redirect('profile')


		else:
			return render(request, 'users/register.html', {'error': "Passwords Dont Match"} )

	return render(request, 'users/register.html')



def login(request):
	if request.method == "POST":

		user = 	auth.authenticate(username= request.POST['uname'], password = request.POST['pass'] )
		if user is not None :
			auth.login(request,user)
			return redirect('profile')
		else:
			return render(request, 'users/login.html', {'error': "Invalid login credentials"})

	return render(request, 'users/login.html')


@login_required
def logout(request):
	auth.logout(request)
	return redirect('login')


@login_required
def profile(request):

	user = account.objects.filter(user = request.user)
	items = 0

	for u in user:
		items = u.item_set.all()


	n = len(items)
	collist = [[],[],[],[]]

	for i in range(n):
		collist[i%4].append(items[i])


	context = {
		'data': user,
		'items': items,
		'collist':collist
	}

	return render(request, 'users/profile.html',context)


# Add Items view

@login_required
def additem(request):

	itemform = forms.ItemForm()

	if request.method == 'POST':

		#print('Arjun JOshi')

		user = account.objects.filter(user = request.user)
		itemform = forms.ItemForm(request.POST, request.FILES)

		#print("HEY THIS IS THE ITEMFORM")
		#print(itemform)


		if itemform.is_valid():

			#print("ARjun is soooo coool")

			title = itemform.cleaned_data['title']
			price = itemform.cleaned_data['price']
			description = itemform.cleaned_data['description']
			image = itemform.cleaned_data['image']
			category = itemform.cleaned_data['category']
			
			owner = 0
			for u in user:
				owner = u

			newitem = item(title = title, price = price, description = description, category = category, owner = owner, image = image)
			newitem.save()

			return redirect('profile')
			#print('Item is saved')



	context = {
		'form': itemform,
	}

	return render(request, 'users/additem.html',context)


def delitem(request, it = ''):
	#print('Hey this is delitems')


	if request.method == 'POST':
		ditem = item.objects.get(title = it)
		ditem.delete()

	return redirect('profile')


def viewitem(request, it = ''):
	#print("Hey this is viewitem")

	context = {}

	if request.method == 'POST':

		vitem = item.objects.get(title = it)
		context = {'item': vitem}

	return render(request, 'users/viewitem.html', context)