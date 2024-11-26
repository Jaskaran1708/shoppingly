from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from .models import customer, product, cart, orderplaced
from django.contrib import messages
from .form import CustomerRegisterationForm, CustomerProfileForm
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate,login,logout

class ProductView(View):
 def get(self, request):
  Topwear = product.objects.filter(Category = 'TW')
  Bottomwear = product.objects.filter(Category = 'BW')
  Mobile = product.objects.filter(Category = 'M')
  Laptop = product.objects.filter(Category = 'L')
 

  
  return render(request, 'app/home.html', 
                {'Topwear' : Topwear,
                 'Bottomwear': Bottomwear,
                 'Mobile' : Mobile,
                 'Laptop' : Laptop
                 })
 

class ProductDetailedView(View):
 def get(self,request,pk):
  prduct = product.objects.get(pk=pk)
  item_already_in_cart = False
  item_already_in_cart = cart.objects.filter(Q(Product= prduct.id)).exists()
  return render(request, 'app/productdetail.html', {'product':prduct, 'item_already_in_cart': item_already_in_cart})
 
# def cart_counter(request):
#    cart_count = cart.objects.filter(user = request.user).count()
# #    return render(request, 'addtocart.html', {'cart_count': cart_count})
# def cart_count(request):
#     # Retrieve the total count of products in the cart
#     cart_count = cart.objects.filter(user=request.user).count()  # Assuming you have a user-based cart system

#     # Pass the cart count to the template context
#     return render(request, 'addtocart.html', {'cart_count': cart_count})



@login_required
def add_to_cart(request):
  user = request.user
  product_id = request.GET.get('prod_id')
  Product = product.objects.get(id = product_id)
  cart(user = user, Product = Product).save()
  return redirect('/cart')

@login_required
def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  Cart = cart.objects.filter(user = user)
  cart_count = cart.objects.filter(user=request.user).count()
  amount = 0.0
  shipping_amount= 70.0
  total_amount = 0.0
  cart_product = [p for p in cart.objects.all() if p.user == user ]
  if cart_product:
   for p in cart_product:
    tempamount = (p.Quantity * p.Product.Discounted_price) 
    amount += tempamount
    total_amount = amount + shipping_amount
    return render(request, 'app/addtocart.html', {'carts': Cart, 'total_amount': total_amount, 'amount': amount, 'cart_count': cart_count})
  else:
   return render(request, 'app/emptycart.html')
  
@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def plus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = cart.objects.get(Q(Product=prod_id) & Q(user=request.user))
		c.Quantity+=1
		c.save()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.Quantity * p.Product.Discounted_price)
			amount += tempamount
		data = {
			'quantity':c.Quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")


@login_required
def minus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = cart.objects.get(Q(Product=prod_id) & Q(user=request.user))
		c.Quantity-=1
		c.save()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.Quantity * p.Product.Discounted_price)
			amount += tempamount
		data = {
			'quantity':c.Quantity,
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")
   
@login_required
def remove_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = cart.objects.get(Q(Product=prod_id) & Q(user=request.user))
		c.delete()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.Quantity * p.Product.Discounted_price)
			amount += tempamount
		data = {
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")


@method_decorator(login_required, name = 'dispatch')
class ProfileView(View):
 def get(self,request):
  form = CustomerProfileForm()
  return render(request, 'app/profile.html', {'form': form , 'active' : 'btn-primary'})
 def post(self,request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   Name = form.cleaned_data['Name']
   Locality = form.cleaned_data['Locality']
   City = form.cleaned_data['City']
   State = form.cleaned_data['State']
   Zipcode = form.cleaned_data['Zipcode']
   reg = customer(user = usr, Name= Name,Locality = Locality, City = City, State = State, Zipcode = Zipcode)
   reg.save()
   messages.success(request, 'Congratulation!! Profile updated successfully')
  return render(request, 'app/profile.html', {'form' : form, 'active'  : 'btn-primary'})

@login_required
def address(request):
 add = customer.objects.filter(user = request.user)
 return render(request, 'app/address.html', {'add':add, 'active': 'btn-primary'})

@login_required
def orders(request):
 op = orderplaced.objects.filter(user = request.user)
 return render(request, 'app/orders.html', {'order_placed': op })

@login_required
def change_password(request):
 return render(request, 'app/changepassword.html')

@login_required
def mobile(request, data= None):
 if data == None:
  mobiles = product.objects.filter(Category = 'M')
 elif data == 'Apple' or data == 'samsung' or data == 'mi':
  mobiles = product.objects.filter(Category = 'M').filter(Brand = data)
 elif data == 'below':
  mobiles = product.objects.filter(Category = 'M').filter(Discounted_price__lt = 10000)
 elif data == 'above':
  mobiles = product.objects.filter(Category = 'M').filter(Discounted_price__gt = 10000)
 return render(request, 'app/mobile.html', {'mobiles' : mobiles})

@login_required
def laptop(request, data = None):
   if data == None:
      laptop = product.objects.filter(Category = "L")
   elif data == 'Apple' or data == 'Dell' or data == 'Lenovo':
      laptop = product.objects.filter(Category = 'L').filter(Brand = data)
   elif data == 'below':
      laptop = product.objects.filter(Category = 'L').filter(Discounted_price__lt = 65000)
   elif data == 'above':
      laptop = product.objects.filter(Category = 'L').filter(Discounted_price__gt = 65000)
   return render(request, 'app/laptop.html', {'laptop' : laptop})
      

@login_required
def topwear(request,data = None):
 if data == None:
  topwear = product.objects.filter(Category = 'TW')
 elif  data == 'People' or data == 'Tommy Hilfiger':
  topwear = product.objects.filter(Category = 'TW').filter(Brand = data)
 elif data == 'below':
  topwear = product.objects.filter(Category = 'TW').filter(Discounted_price__lt = 600)
 elif data == 'above':
  topwear = product.objects.filter(Category = 'TW').filter(Discounted_price__gt = 600)
 return render(request,'app/topwear.html', {'topwear':topwear})

@login_required
def bottomwear(request,data = None):
 if data == None:
  bottomwear = product.objects.filter(Category = 'BW')
 elif  data == 'Tommy Hilfiger' or data == 'Levis':
  bottomwear = product.objects.filter(Category = 'BW').filter(Brand = data)
 elif data == 'below':
  bottomwear = product.objects.filter(Category = 'BW').filter(Discounted_price__lt = 700)
 elif data == 'above':
  bottomwear = product.objects.filter(Category = 'BW').filter(Discounted_price__gt = 700)
 return render(request,'app/bottomwear.html', {'bottomwear': bottomwear})

class CustomerRegistrationView(View):
 def get(self,request):
  form = CustomerRegisterationForm()
  return render(request, 'app/customerregistration.html', {'form':form})
 def post(self, request):
  form = CustomerRegisterationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully.')
   form.save()
  return render(request, 'app/customerregistration.html', {'form':form})

@login_required
def checkout(request):
 user = request.user
 add = customer.objects.filter(user=user)
 cart_item = cart.objects.filter(user = user)
 amount = 0.0
 shipping_amount= 70.0
 totalamount = 0.0
 cart_product = [p for p in cart.objects.all() if p.user == request.user]
 if cart_product:
  for p in cart_product:
      tempamount = (p.Quantity * p.Product.Discounted_price)
      amount += tempamount
  totalamount = amount +shipping_amount
 return render(request, 'app/checkout.html',{'add': add, 'totalamount': totalamount, 'cart_product':cart_product})

@login_required
def payment_done(request):
   user = request.user
   custid = request.GET.get('custid')
   Customer = customer.objects.get(id=custid)
   Cart = cart.objects.filter(user= user)
   for c in Cart:
      orderplaced(user = user, customer = Customer, product = c.Product, quantity = c.Quantity).save()
      c.delete()
   return redirect('/orders')

	
def searchview(request):
   query = request.GET.get('q')
   result = product.objects.filter(Title__icontains = query)
   displayed_ids = list(set(obj.id for obj in result))

   return render(request, "app/search.html", {'result': result, 'displayed_ids': displayed_ids})

def logoutview(request):
   logout(request)
   return redirect('login')