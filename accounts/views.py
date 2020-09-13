from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.forms import inlineformset_factory  #to create one form within multiple forms
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unaunthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group


# Create your views here.

@unaunthenticated_user
def loginpage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Paassword is incorrect')
    return render(request, 'accounts/login.html')

def logoutpage(request):
    logout(request)
    return redirect('login')

@unaunthenticated_user
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request,'Account was created for',username)
            return redirect('login')

    context = {"form":form}
    return render(request,'accounts/register.html',context)

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    my_dict = {'orders':orders,'customers':customers,'total_customers':total_customers,
               'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request,'accounts/dashboard.html',context=my_dict)

def userPage(request):
	context = {}
	return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)
    #orders = customer.order_set.all()
    orders = customer.orders.all()  #this is using related name

    ''' to get the Orders for a particular customer Django creates a related name automatically using
     the name of the related model with the suffix _set. You can filter this set to retrieve
      subsets of records — here, we are just using all() to get all of the related Orders.
      
      You can also pass in a related_name parameter if you’d like to set your own:
      Which would allow you to use orders = customer.orders.all() instead of using Django’s default 
      order_set naming convention'''

    myFilter = OrderFilter(request.GET,queryset=orders)
    orders = myFilter.qs
    order_count = orders.count()
    context = {'customer':customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}
    return render(request,'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def CreateOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer) #queryset is to hide to initil from the form data
    #form = OrderForm(initial={'customer':customer})
    '''
    The initial argument lets you specify the initial value to use when rendering
    this Field in an unbound Form. The use-case for this is when you want to display
    an “empty” form in which a field is initialized to a particular value.

'''
    if request.method == "POST":
        formset = OrderFormSet(request.POST,instance=customer)
        #form = OrderForm(request.POST)
        print("POST DATA",request.POST)
        if formset.is_valid():
            formset.save()
            return redirect ('/')
    context={'formset':formset}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST,instance=order)
        print("POST DATA",request.POST)
        if form.is_valid():
            form.save()
            return redirect ('/')
    context={'form':form}

    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render(request,'accounts/delete.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)

