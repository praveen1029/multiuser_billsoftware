from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.utils.crypto import get_random_string

def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def cmp_register(request):
    return render(request, 'cmp_register.html')

def cmp_details(request,id):
    context = {'id' : id}
    return render(request, 'cmp_details.html', context)

def emp_register(request):
    return render(request, 'emp_register.html')

def cmp_dash(request):
    return render(request, 'cmp_dash.html')

def emp_dash(request):
    return render(request, 'emp_dash.html')

def register_company(request):
  if request.method == 'POST':
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    uname = request.POST['uname']
    phno = request.POST['phno']
    passw = request.POST['pass']
    cpass = request.POST['cpass']
    rfile = request.FILES.get('rfile')
    
    if passw == cpass:
      if User.objects.filter(username = uname).exists():
        messages.info(request, 'Sorry, Username already exists')
        return redirect('cmp_register')

      elif not User.objects.filter(email = email).exists():
        user_data = User.objects.create_user(first_name = fname, last_name = lname, username = uname, email = email, password = passw)

        cmp = company( contact = phno, user = user_data, profile_pic = rfile)
        cmp.save()
        return redirect('cmp_details',user_data.id)

      else:
        messages.info(request, 'Sorry, Email already exists')
        return redirect('company_reg')
    return render(request,'cmp_register.html')
  
def register_company_details(request,id):
  if request.method == 'POST':
    cname = request.POST['cname']
    address = request.POST['address']
    city = request.POST['city']
    state = request.POST['state']
    country = request.POST['country']
    pincode = request.POST['pincode']
    pannumber = request.POST['pannumber']
    gsttype = request.POST['gsttype']
    gstno = request.POST['gstno']

    code=get_random_string(length=6)

    usr = User.objects.get(id = id)
    cust = company.objects.get(user = usr)
    cust.company_name = cname
    cust.address = address
    cust.city = city
    cust.state = state
    cust.company_code = code
    cust.country = country
    cust.pincode = pincode
    cust.pan_number = pannumber
    cust.gst_type = gsttype
    cust.gst_no = gstno
    cust.save()

    return redirect('login')

def register_employee(request):
  if request.method == 'POST':
    fname = request.POST['fname']
    lname = request.POST['lname']
    email = request.POST['email']
    uname = request.POST['uname']
    phno = request.POST['phno']
    passw = request.POST['pass']
    cpass = request.POST['cpass']
    ccode = request.POST['ccode']
    rfile = request.FILES.get('rfile')

    if not company.objects.filter(company_code = ccode).exists():
        messages.info(request, 'Sorry, Company Code is Invalid')
        return redirect('emp_register')
    
    if passw == cpass:
      if User.objects.filter(username = uname).exists():
        messages.info(request, 'Sorry, Username already exists')
        return redirect('emp_register')

      elif not User.objects.filter(email = email).exists():
        user_data = User.objects.create_user(first_name = fname, last_name = lname, username = uname, email = email, password = passw)
        emp = employee(user = user_data, profile_pic = rfile, company_code=ccode, contact=phno)
        emp.save()
        return redirect('login')

      else:
        messages.info(request, 'Sorry, Email already exists')
        return redirect('emp_register')
    return render(request,'emp_register.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        cpass = request.POST['pass']
        try:
            usr = User.objects.get(email=email)
            log_user = auth.authenticate(username = usr.username, password = cpass)
            if log_user is not None:
                if company.objects.filter(user=usr).exists():
                    auth.login(request, log_user)
                    return redirect('cmp_dash')
                else:
                    emp = employee.objects.get(user=usr)
                    if emp.is_approved == 0:
                        messages.info(request,'Employee is not Approved')
                        return redirect('login')
                    else:
                        auth.login(request, log_user)
                        return redirect('emp_dash')
        except:
           messages.info(request,'Invalid Login Details')
           return redirect('login')

        return redirect('login')

    return redirect('login')
