from django.shortcuts import render,redirect
from django.http import HttpResponse
from CustomerManage.models import Customer,Product,Tag,Order
from .forms import OrderForm,CustomerForm,CreateUserForm
from .decorators import allowed_users, unauthenticated_user,admin_only

from django.forms import fields, formsets, inlineformset_factory
from django.db.models import Q
from .filters import OrderFilter

from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.urls.base import reverse_lazy

# Create your views here.

@login_required(login_url='/cmr/login/')
@admin_only
def home(request):    
     orders=Order.objects.all()
     customers=Customer.objects.all()
     last_five = Order.objects.filter().order_by('-id')[:5]                                  
     total_orders=orders.count()
     delivered=Order.objects.filter(status='Delivered').count()
     pending=Order.objects.filter(status='Pending').count()
     

     context={'orders':orders,'customers':customers,'total_orders':total_orders,'delivered':delivered,'pending':pending,'last_five':last_five}
     return render(request,"CustomerManage/dashboard.html",context)


@login_required(login_url='/cmr/login/')
@allowed_users(allowed_roles=['admin'])
def Products(request):
     products=Product.objects.all()
     return render(request,"CustomerManage/products.html",{'products':products})


@login_required(login_url='/cmr/login/')
@allowed_users(allowed_roles=['admin'])
def customer(request,custid):
     custmr=Customer.objects.get(id=custid)
     orders=custmr.order_set.all()
     total_orders=orders.count()

     myFilter = OrderFilter(request.GET, queryset=orders)
     orders = myFilter.qs
     return render(request,"CustomerManage/customer.html",{'customer':custmr,'orders':orders,'total_orders':total_orders,'myFilter':myFilter})


@login_required(login_url='/cmr/login/')
@allowed_users(allowed_roles=['admin'])
def CreateOrder(request):
     form=OrderForm()
     if request.method=='POST':
          form=OrderForm(request.POST)
          if form.is_valid():
               form.save()
               return redirect('/cmr/home/')
          
     else:
          return render(request,"CustomerManage/order_form.html",{'form':form})
     

@login_required(login_url='/cmr/login/')
@allowed_users(allowed_roles=['admin'])
def UpdateOrder(request,ordid):
     order=Order.objects.get(id=ordid)
     form=OrderForm(instance=order)
     if request.method=='POST':
          form=OrderForm(request.POST,instance=order)
          if form.is_valid():
               form.save()
               return redirect('/cmr/home/')
     else:
          return render(request,"CustomerManage/order_form.html",{'form':form})


@login_required(login_url='/cmr/login/')
@allowed_users(allowed_roles=['admin'])
def DeleteOrder(request,ordid):
     order=Order.objects.get(id=ordid)
     if request.method=='POST':
          order.delete()
          return redirect('/cmr/home/')
     else:
          return render(request,"CustomerManage/delete.html",{'item':order})


@login_required(login_url='/cmr/login/')
@allowed_users(allowed_roles=['admin'])
def CreateCustomer(request):
     form=CustomerForm()
     if request.method=='POST':
          form=CustomerForm(request.POST)
          if form.is_valid():
               form.save()
               return redirect('/cmr/home/')
          
     else:
          return render(request,"CustomerManage/customer_form.html",{'form':form})


@login_required(login_url='/cmr/login/')
@allowed_users(allowed_roles=['admin'])
def UpdateCustomer(request,custid):
     customer=Customer.objects.get(id=custid)
     form=CustomerForm(instance=customer)
     if request.method=='POST':
          form=CustomerForm(request.POST,instance=customer)
          if form.is_valid():
               form.save()
               return redirect('/cmr/home/')
     else:
          return render(request,"CustomerManage/customer_form.html",{'form':form})


@login_required(login_url='/cmr/login/')
@allowed_users(allowed_roles=['admin'])
def PlaceOrder(request,custid):
     OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=5)
     customer=Customer.objects.get(id=custid)
     formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
     
     if request.method=='POST':
          formset=OrderFormSet(request.POST,instance=customer)
          if formset.is_valid():
               formset.save()
               return redirect('/cmr/home/')
          
     else:
          return render(request,"CustomerManage/place_order.html",{'formset':formset})


@unauthenticated_user
def Register(request):
     form=CreateUserForm()
     if request.method=='POST':
          form=CreateUserForm(request.POST)
          if form.is_valid():
               user=form.save()
               username=form.cleaned_data.get('username')
               email=form.cleaned_data.get('email')

               
               messages.success(request,'Account was created for '+ username)
               return redirect('/cmr/login/')
          
     return render(request,"CustomerManage/register.html",{'form':form})


@unauthenticated_user
def Login(request):
     if request.method=='POST':
          usname=request.POST.get('username')
          pswd=request.POST.get('password')

          user=authenticate(request,username=usname,password=pswd)
          if user is not None:
               login(request,user)
               return redirect('/cmr/home/')
          else:
               messages.info(request,'Username or Password is incorrect')

     return render(request,"CustomerManage/login.html")


def Logout(request):
     logout(request)
     return redirect('/cmr/login/')


@login_required(login_url='/cmr/login/')
@allowed_users(allowed_roles=['customer'])
def Userpage(request):
     orders=request.user.customer.order_set.all()                                     
     total_orders=orders.count()
     delivered=orders.filter(status='Delivered').count()
     pending=orders.filter(status='Pending').count()
     return render(request,"CustomerManage/user.html",{'orders':orders,'total_orders':total_orders,'delivered':delivered,'pending':pending})


@login_required(login_url='/cmr/login/')
@allowed_users(allowed_roles=['customer'])
def Useraccount(request):
     customer=request.user.customer
     form=CustomerForm(instance=customer)
     if request.method=='POST':
          form=CustomerForm(request.POST,request.FILES,instance=customer)
          if form.is_valid():
               form.save()
     return render(request,"CustomerManage/user_account.html",{'form':form})

