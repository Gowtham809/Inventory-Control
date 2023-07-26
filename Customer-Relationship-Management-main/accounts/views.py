from multiprocessing import context
from django.shortcuts import redirect, render
from django.forms import formset_factory, inlineformset_factory, modelformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import F

# Create your views here.
from .models import *
from .forms import *
from .filter import *



def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    #last_orders = Order.objects.all().order_by('-date_created')[0:5]
    # To reduces the redundant columns in the original object
    last_orders = Order.objects.select_related('customer__user', 'product').prefetch_related('product__tags').all().order_by('-date_created')[0:5]

    totalOrders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders':orders,
        'customers':customers,
        'last_orders': last_orders,
        'totalOrders':totalOrders,
        'delivered':delivered,
        'pending':pending
        }
    return render(request, 'accounts/dashboard.html',context)


def userPage(request):
    orders = request.user.customer.order_set.all()

    totalOrders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
     
    context = {'orders':orders, 'totalOrders':totalOrders,
    'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/user.html', context)


   



def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html',{'products':products})



def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    total_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer':customer, 'orders':orders, 'total_orders':total_orders, 'myFilter':myFilter}

    return render(request, 'accounts/customer.html', context)


def createProduct(request):
    ProductFormSet = modelformset_factory(Product, form=CreateProductForm, extra=5)
    formset = ProductFormSet(queryset=Order.objects.none())
    if request.method == 'POST':
        formset = ProductFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('products')
    
    context = {'formset':formset}
    return render(request, 'accounts/create_product.html', context)          



def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
        return redirect('customer',customer.id)

    context = {'formset':formset}
    return render(request, 'accounts/place_order.html', context)   

