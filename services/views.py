from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from django.http import Http404
from .models import ClothType, Discounds, Feedback, Payment, ServiceType, Address, OrderNumber, Orders, Status
import logging

logger = logging.getLogger(__name__)

# Create your views here.


@login_required
def newlaundry(request):
    if request.method == 'POST':
        try:
            date = timezone.now()
            clothtype = request.POST.get('clothtype', '').strip()
            no = request.POST.get('noofclothes', '0')
            
            # Validate inputs
            if not clothtype:
                messages.error(request, 'Please select a cloth type')
                return redirect('newlaundry')
                
            try:
                noofclothes = int(no) if no else 0
                if noofclothes <= 0:
                    messages.error(request, 'Number of clothes must be greater than 0')
                    return redirect('newlaundry')
            except ValueError:
                messages.error(request, 'Invalid number of clothes')
                return redirect('newlaundry')
                
            servicetypes = request.POST.get('servicetype')
            if not servicetypes:
                messages.error(request, 'Please select a service type')
                return redirect('newlaundry')
                
            try:
                ser = get_object_or_404(ServiceType, id=servicetypes)
            except (ServiceType.DoesNotExist, ValueError, Http404):
                messages.error(request, 'Invalid service type selected')
                return redirect('newlaundry')
                
            cost = ser.price
            servicetyname = ser.servicetypes
            serviceid = ser.id
            
            # Get first status (should be 'Received')
            try:
                first_status = Status.objects.first()
                statusid = first_status.id if first_status else 1
            except Status.DoesNotExist:
                statusid = 1
                
            userid = request.user.id
            
            if OrderNumber.objects.filter(userid_id=userid).exists():
                on=OrderNumber.objects.get(userid_id=userid)
                orderno=on.orders
                on.orders=int(on.orders)+1
                on.save()
                if Discounds.objects.filter(orders__lte=orderno).exists():
                    d=Discounds.objects.get(orders__lte=orderno)
                    discound=d.discounds
                    homedelivery = request.POST.get('delivery')
                    if homedelivery == "True":
                        totalcost = ((cost*noofclothes)+50)-discound
                    else:
                        totalcost = (cost*noofclothes)-discound
                else:
                    discound=0
                    homedelivery = request.POST.get('delivery')
                    if homedelivery == "True":
                        totalcost = ((cost*noofclothes)+50)-discound
                    else:
                        totalcost = (cost*noofclothes)-discound
                ord=Orders.objects.create(date=date,noofclothes=noofclothes,cost=cost,discound=discound,totalcost=totalcost,userid_id=userid,serviceid_id=serviceid,homedelivery=homedelivery,servicetypes=servicetyname,clothtype=clothtype,statusid_id=statusid)
                ord.save()
            else:
                on=OrderNumber.objects.create(userid_id=userid,orders=1)
                on.save()
                orderno=1 
                homedelivery = request.POST.get('delivery')
                if homedelivery == "True":
                    totalcost = ((cost*noofclothes)+50)
                else:
                    totalcost = (cost*noofclothes)
                ord=Orders.objects.create(date=date,noofclothes=noofclothes,cost=cost,discound=0,totalcost=totalcost,userid_id=userid,serviceid_id=serviceid,homedelivery=homedelivery,servicetypes=servicetyname,clothtype=clothtype,statusid_id=statusid)
                ord.save()

            
            return redirect('checkout')
            
        except Exception as e:
            logger.error(f'Order creation error: {str(e)}')
            messages.error(request, 'An error occurred while creating your order')
            return redirect('newlaundry')
    
    # GET request
    ctypes = ClothType.objects.all()
    stypes = ServiceType.objects.all()
    add = Address.objects.filter(userid_id=request.user.id)
    return render(request, 'newlaundry.html', {'ctypes': ctypes, 'stypes': stypes, 'add': add})


@login_required
def checkout(request):
    try:
        # Get the last order for the current user
        order = Orders.objects.filter(userid=request.user).last()
        if not order:
            messages.error(request, 'No order found')
            return redirect('newlaundry')

        if request.method == 'POST':
            payment_method = request.POST.get('delivery')
            if payment_method == 'paid':
                ordid = order.id
                pay, created = Payment.objects.get_or_create(
                    orderid_id=ordid,
                    defaults={'payed': True}
                )
                if not created:
                    pay.payed = True
                    pay.save()
                messages.success(request, 'Payment processed successfully')
                return render(request, 'transaction.html', {'order': order})
            elif payment_method == 'cod':
                ordid = order.id
                pay, created = Payment.objects.get_or_create(
                    orderid_id=ordid,
                    defaults={'payed': False}
                )
                messages.success(request, 'Order placed successfully with Cash on Delivery')
                return redirect('index')
        
        return render(request, 'checkout.html', {'order': order})
    except Exception as e:
        logger.error(f'Checkout error: {str(e)}')
        messages.error(request, 'An error occurred during checkout')
        return redirect('newlaundry')


def transaction(request):
    return render(request,'transaction.html')
    

def feedback(request):
    if request.user.is_authenticated:
        if request.method =='POST':
            message = request.POST['message']
            uid = request.user.id
            feed = Feedback.objects.create(userid_id = uid,message = message)
            feed.save()
            messages.info(request,'Feedback Posted')
            return redirect('feedback')
        else:
            return render(request,'feedback.html')
    else:
        return redirect("/")


@login_required
def orderhistory(request):
    try:
        # Get completed orders (status 6 = Completed)
        completed_status = Status.objects.filter(status='Completed').first()
        if completed_status:
            hist = Orders.objects.filter(
                userid=request.user, 
                statusid=completed_status
            ).order_by('-date')
        else:
            hist = Orders.objects.none()
        
        return render(request, 'orderhistory.html', {'hist': hist})
    except Exception as e:
        logger.error(f'Order history error: {str(e)}')
        return render(request, 'orderhistory.html', {'hist': Orders.objects.none()})

def profileupdate(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            address=request.POST['address']
            if Address.objects.filter(userid_id=request.user.id).exists():
                add = Address.objects.get(userid_id=request.user.id)
                add.address=address
                add.save()
                messages.info(request,'Address updated')
                return redirect('profileupdate')
            else:
                add = Address.objects.create(userid_id=request.user.id,address=address)
                add.save()
                messages.info(request,'Address added')
                return redirect('profileupdate')
        else:
            add = Address.objects.filter(userid_id=request.user.id)
            return render(request,'profileupdate.html', {'add':add})
    else:
        return redirect("/")


@login_required
def active(request):
    try:
        # Get active orders (not completed)
        completed_status = Status.objects.filter(status='Completed').first()
        if completed_status:
            hist = Orders.objects.filter(userid=request.user).exclude(
                statusid=completed_status
            ).order_by('-date')
        else:
            hist = Orders.objects.filter(userid=request.user).order_by('-date')
        
        return render(request, 'active.html', {'hist': hist})
    except Exception as e:
        logger.error(f'Active orders error: {str(e)}')
        return render(request, 'active.html', {'hist': Orders.objects.none()})


def changepassword(request):
    if request.user.is_staff:
        if request.method =='POST':
            cpassword = request.POST['cpassword']
            n1password = request.POST['n1password']
            n2password = request.POST['n2password']
            currentpassword = request.user.password
            if check_password(cpassword,currentpassword) == True:
                if n1password == n2password:
                    u = User.objects.get(username=request.user.username)
                    u.set_password(n1password)
                    u.save()
                    messages.info(request,'Password Changed')
                    return redirect('changepassword')
                else:
                    messages.info(request,'Password not matching')
                    return redirect('changepassword')
            else:
                messages.info(request,'Current Password Entered is Wrong')
                return redirect('changepassword')
        else:
            return render(request,'changepassword.html')
 
    elif request.user.is_authenticated:
        if request.method =='POST':
            cpassword = request.POST['cpassword']
            n1password = request.POST['n1password']
            n2password = request.POST['n2password']
            currentpassword = request.user.password

            if check_password(cpassword,currentpassword) == True:
                if n1password == n2password:
                    u = User.objects.get(username=request.user.username)
                    u.set_password(n1password)
                    u.save()
                    messages.info(request,'Password Changed')
                    return redirect('changepassword')
                else:
                    messages.info(request,'Password not matching')
                    return redirect('changepassword')
            else:
                messages.info(request,'Current Password Entered is Wrong')
                return redirect('changepassword')
        else:
            return render(request,'changepassword.html')
    else:
        return redirect("/")

@login_required
def adddetails(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('index')
    
    if request.method == 'POST':
        if request.POST.get('addclothtype'):
            clothtypes = request.POST['clothtype']
            c = ClothType.objects.create(clothtypes=clothtypes)
            c.save()
            messages.info(request,'Record added')
            return redirect('adddetails')
        elif request.POST.get('addnewservice'):
            newservice = request.POST['newservice']
            price = request.POST['price']
            s = ServiceType.objects.create(servicetypes=newservice,price=price)
            s.save()
            messages.info(request,'Record added')
            return redirect('adddetails')
    
    return render(request,'adddetails.html')

@login_required
def reports(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('index')
    
    if request.method == 'POST':
        fromdate=request.POST['fdate']
        todate=request.POST['tdate']
        s=0
        if Orders.objects.filter(date__gte=fromdate,date__lte=todate).order_by('id'):
            ord=Orders.objects.filter(date__gte=fromdate,date__lte=todate).order_by('id')
            for orders in ord:
                s=s+orders.totalcost
        order = Orders.objects.filter(date__gte=fromdate,date__lte=todate).order_by('id')
        messages.info(request,'Report Generated')
        return render(request,'reports.html',{'order':order,'s':s})
    else:
        return render(request,'reports.html')

@login_required
def allreports(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('index')
        
    try:
        users = User.objects.filter(is_staff=False).count()
        staffs = User.objects.filter(is_staff=True).count()
        order_count = Orders.objects.count()
        totalcost_result = Orders.objects.aggregate(Sum('totalcost'))
        total_cost = totalcost_result['totalcost__sum'] or 0
        
        context = {
            'users': users,
            'staffs': staffs,
            'order': order_count,
            'totalcost': total_cost
        }
        return render(request, 'allreports.html', context)
    except Exception as e:
        logger.error(f'All reports error: {str(e)}')
        messages.error(request, 'Error generating reports')
        return render(request, 'allreports.html', {
            'users': 0, 'staffs': 0, 'order': 0, 'totalcost': 0
        })

@login_required
def allorders(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('index')
    
    order=Orders.objects.all().order_by('date')
    return render(request,'allorders.html',{'order':order})
    

@login_required
def changestatus(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('index')
    
    if request.method == 'POST':
        status=request.POST.get('statusd')
        orderid=request.POST.get('update')
        if Orders.objects.filter(id=orderid).exists():
            order = Orders.objects.get(id=orderid)
            order.statusid_id=status
            order.save()
            messages.info(request,'Status changed')
            return redirect('changestatus')
    elif Orders.objects.exclude(statusid='6'):
        order = Orders.objects.exclude(statusid='6').order_by('id')
        s=Status.objects.all()
        return render(request,'changestatus.html',{'order':order,'s':s})
    else:
        return render(request,'changestatus.html')



@login_required
def adduser(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('index')
    
    if request.method =='POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        checks = request.POST.get('checks',False)

        if User.objects.filter(username=username).exists():
            messages.info(request,'Username Taken')
            return redirect('adduser')
        elif User.objects.filter(email=email).exists():
            messages.info(request,'Email Taken')
            return redirect('adduser')
        elif checks == 'True':
            user = User.objects.create_user(username = username,  first_name = fname,  last_name = lname, password = password, email = email, is_staff = True)
            user.save()
            messages.info(request,'Staff Added')
            return redirect('adduser')
        else:
            user = User.objects.create_user(username = username,  first_name = fname,  last_name = lname, password = password, email = email)
            user.save()
            messages.info(request,'User Added')
            return redirect('adduser')
    else:
        return render(request,'adduser.html')


@login_required
def adddiscound(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('index')
    
    if request.method =='POST':
        orderno = request.POST['ordernumber']
        discound = request.POST['discound']
        dis = Discounds.objects.create(discounds = discound,orders = orderno)
        dis.save()
        messages.info(request,'Discound Added')
        return redirect('adddiscound')
    else:
        return render(request,'adddiscound.html')


@login_required
def vfeedback(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('index')
    
    feed = Feedback.objects.all()
    return render(request,'vfeedback.html',{'feed':feed})

@login_required
def unpaid(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('index')
    
    if request.method == 'POST':
        p="True"
        orderid=request.POST.get('update')
        if Payment.objects.filter(orderid_id=orderid).exists():
            pay = Payment.objects.get(orderid_id=orderid)
            pay.payed=p
            pay.save()
            messages.info(request,'Status changed')
            return redirect('unpaid')
    
    pay = Payment.objects.all().exclude(payed=True)
    return render(request,'unpaid.html',{'pay':pay})


@login_required
def cdelivery(request):
    if not request.user.is_staff:
        messages.error(request, 'Access denied')
        return redirect('index')
    
    if Orders.objects.filter(homedelivery=True).exclude(statusid_id='6').exists():
        for ord in Orders.objects.filter(homedelivery=True).exclude(statusid_id='6'):
            print('ord:',ord.userid_id)
            addid=ord.userid_id
            add = Address.objects.get(userid_id=addid)
            return render(request,'cdelivery.html',{'ord':ord,'add':add})
    else:
        return render(request,'cdelivery.html')