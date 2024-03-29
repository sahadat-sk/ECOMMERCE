from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

def store(request):
    things = Product.objects.all()
    mylist=request.POST.getlist('gendercheck')

    if request.GET.get('Apply') == 'Apply':
        print('user clicked apply')
        if 'Female' in mylist:
            things = Product.objects.filter(tag = True)
        elif 'Male' in mylist:
            things = Product.objects.filter(tag = False)

    context = {'things': things}
    return render(request, 'store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False) #order number obtained
        items = order.orderitem_set.all() #obtained the ordered items for that order number
    else:
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = {'items': items, 'order': order}
    return render(request, 'cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False) #order number obtained
        items = order.orderitem_set.all() #obtained the ordered items for that order number
    else:
        items=[]
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = {'items': items, 'order': order}
    return render(request, 'checkout.html', context)

@csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    prod_id = data.get('prod_id')
    action = data.get('action')
    print('Action : ', action)
    print('Product : ', prod_id)

    return JsonResponse('Item was added', safe=False)

def searchview(request):
    things = Product.objects.all()
    term = request.GET.get('searchname', None)
    if term:
        things=Product.objects.filter(item__icontains=term)
    context = {'things': things}
    return render(request,'store.html',context)

def filterview(request):
    things = Product.objects.all()
    mylist=request.GET.getlist('gendercheck')
    if 'Male' in mylist:
        things=Product.objects.filter(tag=False)
    else:
        things=Product.objects.filter(tag=True)
    context = {'things': things}
    return render(request,'store.html',context)

def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return redirect('store')
    else:
        print('USER NOT FOUND')

    context = {}
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect('store')
    # Redirect to a success page.