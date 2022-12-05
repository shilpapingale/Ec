from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
    def get(self,request):
        totalitem = 0
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'totalitem':totalitem})


class ProductDetailView(View):
    def get(self,request,pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        
        user = request.user
        cart = Cart.objects.filter(user=user)
        # print(cart)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount,'totalitem':totalitem})
        else:
            return render(request,'app/emptycart.html',)

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount


        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount

        data = {
            'amount':amount,
            'totalamount':amount + shipping_amount
            }
        return JsonResponse(data)




def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',{'add':add,'active':'btn btn-primary'})
 
@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'order_placed':op})



def mobile(request,data=None):
 if data == None:
     mobiles = Product.objects.filter(category='M')
 elif data == 'Samsung' or data == 'Apple' or data == 'Mi':
     mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'below':
     mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
 elif data == 'above':
     mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)

 return render(request, 'app/mobile.html',{'mobiles':mobiles})


def laptop(request,data=None):
 if data == None:
     laptops = Product.objects.filter(category='L')
 elif data == 'HP' or data == 'Dell' or data == 'Lenovo':
     laptops = Product.objects.filter(category='L').filter(brand=data)
 elif data == 'below':
     laptops = Product.objects.filter(category='L').filter(discounted_price__lt=30000)
 elif data == 'above':
     laptops = Product.objects.filter(category='L').filter(discounted_price__gt=30000)

 return render(request, 'app/laptop.html',{'laptops':laptops})

def headphone(request,data=None):
 if data == None:
     headphones = Product.objects.filter(category='H')
 elif data == 'Boat' or data == 'Boult':
     headphones = Product.objects.filter(category='H').filter(brand=data)
 elif data == 'below':
     headphones = Product.objects.filter(category='H').filter(discounted_price__lt=600)
 elif data == 'above':
     headphones = Product.objects.filter(category='H').filter(discounted_price__gt=600)

 return render(request, 'app/headphone.html',{'headphones':headphones})
 
 

def topwear(request,data=None):
 if data == None:
     topwears = Product.objects.filter(category='TW')
 elif data == 'levis' or data == 'Lee' or data == 'Allen' or data == 'Polo':
     topwears = Product.objects.filter(category='TW').filter(brand=data)
 elif data == 'below':
     topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=1200)
 elif data == 'above':
     topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=1200)

 return render(request, 'app/topwear.html',{'topwears':topwears})


def bottomwear(request,data=None):
 if data == None:
     bottomwears = Product.objects.filter(category='BW')
 elif data == 'Lee' or data == 'levis' or data == 'Allen' or data == 'Polo':
     bottomwears = Product.objects.filter(category='BW').filter(brand=data)
 elif data == 'below':
     bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=1200)
 elif data == 'above':
     bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=1200)

 return render(request, 'app/bottomwear.html',{'bottomwears':bottomwears})


def wtopwear(request,data=None):
 if data == None:
     wtopwears = Product.objects.filter(category='WTW')
 elif data == 'levis' or data == 'Lee' or data == 'Allen':
     wtopwears = Product.objects.filter(category='WTW').filter(brand=data)
 elif data == 'below':
     wtopwears = Product.objects.filter(category='WTW').filter(discounted_price__lt=500)
 elif data == 'above':
     wtopwears = Product.objects.filter(category='WTW').filter(discounted_price__gt=500)

 return render(request, 'app/wtopwear.html',{'wtopwears':wtopwears})

def wbottomwear(request,data=None):
 if data == None:
     wbottomwears = Product.objects.filter(category='WBW')
 elif data == 'levis' or data == 'Lee' or data == 'Allen':
     wbottomwears = Product.objects.filter(category='WBW').filter(brand=data)
 elif data == 'below':
     wbottomwears = Product.objects.filter(category='WBW').filter(discounted_price__lt=600)
 elif data == 'above':
     wbottomwears = Product.objects.filter(category='WBW').filter(discounted_price__gt=600)

 return render(request, 'app/wbottomwear.html',{'wbottomwears':wbottomwears})



def mcosmetics(request,data=None):
 if data == None:
     mcosmeticss = Product.objects.filter(category='MC')
 elif data == 'Bombay' or data == 'Nivea' or data == 'Fogg' :
     mcosmeticss = Product.objects.filter(category='MC').filter(brand=data)
 elif data == 'below':
     mcosmeticss = Product.objects.filter(category='MC').filter(discounted_price__lt=300)
 elif data == 'above':
     mcosmeticss = Product.objects.filter(category='MC').filter(discounted_price__gt=300)

 return render(request, 'app/mensc.html',{'mcosmeticss':mcosmeticss})


def wcosmetics(request,data=None):
 if data == None:
     wcosmeticss = Product.objects.filter(category='WC')
 elif data == 'Lakme' or data == 'Maybelline':
     wcosmeticss = Product.objects.filter(category='WC').filter(brand=data)
 elif data == 'below':
     wcosmeticss = Product.objects.filter(category='WC').filter(discounted_price__lt=300)
 elif data == 'above':
     wcosmeticss = Product.objects.filter(category='WC').filter(discounted_price__gt=300)

 return render(request, 'app/womensc.html',{'wcosmeticss':wcosmeticss})


def mwatch(request,data=None):
 if data == None:
     mwatches = Product.objects.filter(category='MW')
 elif data == 'Fastrack' or data == 'Fossil' or data == 'Titan':
     mwatches = Product.objects.filter(category='MW').filter(brand=data)
 elif data == 'below':
     mwatches = Product.objects.filter(category='MW').filter(discounted_price__lt=1200)
 elif data == 'above':
     mwatches = Product.objects.filter(category='MW').filter(discounted_price__gt=1200)

 return render(request, 'app/mwatch.html',{'mwatches':mwatches})


def wwatch(request,data=None):
 if data == None:
     wwatches = Product.objects.filter(category='WW')
 elif data == 'Fastrack' or data == 'Fossil' or data == 'Titan':
     wwatches = Product.objects.filter(category='WW').filter(brand=data)
 elif data == 'below':
     wwatches = Product.objects.filter(category='WW').filter(discounted_price__lt=1200)
 elif data == 'above':
     wwatches = Product.objects.filter(category='WW').filter(discounted_price__gt=1200)

 return render(request, 'app/wwatch.html',{'wwatches':wwatches})



# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulations!! Registered Successfully')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})
  
@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items })

@login_required
def paymemt_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


@method_decorator(login_required ,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulations!! Profile Updated Successfully')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})  


def search_bar(request):
    query=request.GET.get('query')
    data=Product.objects.filter(brand__icontains=query)
    return render(request,'app/search.html',{'data':data})

