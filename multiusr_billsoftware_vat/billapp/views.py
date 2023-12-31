from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import auth
from django.utils.crypto import get_random_string
import random
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.http.response import JsonResponse

def home(request):
  return render(request, 'home.html')

def login(request):
  return render(request, 'login.html')

def forgot_password(request):
  return render(request, 'forgot_password.html')

def cmp_register(request):
  return render(request, 'cmp_register.html')

def cmp_details(request,id):
  context = {'id':id}
  return render(request, 'cmp_details.html', context)

def emp_register(request):
  return render(request, 'emp_register.html')

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
      if CustomUser.objects.filter(username = uname).exists():
        messages.info(request, 'Sorry, Username already in Use !!')
        return redirect('cmp_register')
      
      elif Company.objects.filter(contact = phno).exists():
        messages.info(request, 'Sorry, Phone Number already in Use !!')
        return redirect('cmp_register')

      elif not CustomUser.objects.filter(email = email).exists():
        user_data = CustomUser.objects.create_user(first_name = fname, last_name = lname, username = uname, email = email, password = passw, is_company = 1)
        cmp = Company( contact = phno, user = user_data, profile_pic = rfile)
        cmp.save()
        return redirect('cmp_details',user_data.id)

      else:
        messages.info(request, 'Sorry, Email already in Use !!')
        return redirect('cmp_register')
      
    messages.info(request, 'Sorry, Passwords must match !!')
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

    if Company.objects.filter(pan_number = pannumber).exclude(pan_number='').exists():
      messages.info(request, 'Sorry, Pan number is already in Use !!')
      return redirect('cmp_details',id)
    
    if Company.objects.filter(gst_no = gstno).exclude(gst_no='').exists():
      messages.info(request, 'Sorry, GST number is already in Use !!')
      return redirect('cmp_details',id)

    code=get_random_string(length=6)

    usr = CustomUser.objects.get(id = id)
    cust = Company.objects.get(user = usr)
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

    if not Company.objects.filter(company_code = ccode).exists():
      messages.info(request, 'Sorry, Company Code is Invalid !!')
      return redirect('emp_register')
    
    cmp = Company.objects.get(company_code = ccode)
    emp_names = Employee.objects.filter(company = cmp).values_list('user',flat=True)
    for e in emp_names:
       usr = CustomUser.objects.get(id=e)
       if str(fname).lower() == (usr.first_name ).lower() and str(lname).lower() == (usr.last_name).lower():
        messages.info(request, 'Sorry, Employee With this name already exits, try adding an initial !!')
        return redirect('emp_register')
    
    if passw == cpass:
      if CustomUser.objects.filter(username = uname).exists():
        messages.info(request, 'Sorry, Username already exists !!')
        return redirect('emp_register')
      
      elif Employee.objects.filter(contact = phno).exists():
        messages.info(request, 'Sorry, Phone Number already in Use !!')
        return redirect('emp_register')

      elif not CustomUser.objects.filter(email = email).exists():
        user_data = CustomUser.objects.create_user(first_name = fname, last_name = lname, username = uname, email = email, password = passw)
        emp = Employee(user = user_data, company = cmp, profile_pic = rfile, contact=phno)
        emp.save()
        return redirect('login')

      else:
        messages.info(request, 'Sorry, Email already exists !!')
        return redirect('emp_register')
      
    messages.info(request, 'Sorry, Passwords must match !!')
    return render(request,'emp_register.html')
  
def change_password(request):
  if request.method == 'POST':
    email= request.POST.get('email')
    if not CustomUser.objects.filter(email=email).exists():
      messages.success(request,'Sorry, No user found with this email !!')
      return redirect('forgot_password')
    
    else:
      otp = random.randint(100000, 999999)
      usr = CustomUser.objects.get(email=email)
      usr.set_password(str(otp))
      usr.save()

      subject = 'Password Reset Mail'
      message = f'Hi {usr.first_name} {usr.last_name}, Your Otp for password reset is {otp}'
      email_from = settings.EMAIL_HOST_USER
      recipient_list = [email ]
      send_mail(subject, message, email_from, recipient_list)
      messages.info(request,'Password reset mail sent !!')
      return redirect('forgot_password')

def user_login(request):
  if request.method == 'POST':
    email = request.POST['email']
    cpass = request.POST['pass']

    try:
      usr = CustomUser.objects.get(email=email)
      log_user = auth.authenticate(username = usr.username, password = cpass)
      if log_user is not None:
        if usr.is_company == 1:
          auth.login(request, log_user)
          return redirect('dashboard')
        else:
          emp = Employee.objects.get(user=usr)
          if emp.is_approved == 0:
            messages.info(request,'Employee is not Approved !!')
            return redirect('login')
          else:
            auth.login(request, log_user)
            return redirect('dashboard')
      messages.info(request,'Invalid Login Details !!')
      return redirect('login')
    
    except:
        messages.info(request,'Employee do not exist !!')
        return redirect('login')
    

def dashboard(request):
  context = {'usr':request.user}
  return render(request, 'dashboard.html', context)

def logout(request):
  auth.logout(request)
  return redirect('/')

def cmp_profile(request):
  cmp = Company.objects.get(user = request.user)
  context = {'usr':request.user, 'cmp':cmp}
  return render(request,'cmp_profile.html',context)

def load_edit_cmp_profile(request):
  cmp = Company.objects.get(user = request.user)
  context = {'usr':request.user, 'cmp':cmp}
  return render(request,'cmp_profile_edit.html',context)

def edit_cmp_profile(request):
  cmp =  Company.objects.get(user = request.user)
  if request.method == 'POST':
    email = request.POST['email']
    current_email = cmp.user.email
    if email != current_email:
      if CustomUser.objects.filter(email=email).exists():
        messages.info(request,'Sorry, Email Already in Use !!')
        return redirect('load_edit_cmp_profile')
      
    phno_list = list(filter(None,Company.objects.exclude(user = request.user).values_list('contact', flat=True)))
    gst_list = list(filter(None,Company.objects.exclude(user = request.user).values_list('pan_number', flat=True)))
    gno_list = list(filter(None,Company.objects.exclude(user = request.user).values_list('gst_no', flat=True)))

    if request.POST['phno'] in phno_list:
      messages.info(request,'Sorry, Phone number already in Use !!')
      return redirect('load_edit_cmp_profile')

    if request.POST['pan'] in gst_list:
      messages.info(request,'Sorry, PAN number already in Use !!')
      return redirect('load_edit_cmp_profile')

    if request.POST['gstnoval'] in gno_list:
      messages.info(request,'Sorry, GST number already in Use !!')
      return redirect('load_edit_cmp_profile')

    cmp.company_name = request.POST['cname']
    cmp.user.email = request.POST['email']
    cmp.user.first_name = request.POST['fname']
    cmp.user.last_name = request.POST['lname']
    cmp.contact = request.POST['phno']
    cmp.address = request.POST['address']
    cmp.city = request.POST['city']
    cmp.state = request.POST['state']
    cmp.country = request.POST['country']
    cmp.pincode = request.POST['pincode']
    cmp.pan_number = request.POST['pan']
    cmp.gst_type = request.POST['gsttype']
    cmp.gst_no = request.POST['gstnoval']
    old=cmp.profile_pic
    new=request.FILES.get('image')
    if old!=None and new==None:
      cmp.profile_pic=old
    else:
      cmp.profile_pic=new
    
    cmp.save() 
    cmp.user.save() 
    return redirect('cmp_profile') 
  
def emp_profile(request):
  emp = Employee.objects.get(user=request.user)
  context = {'usr':request.user, 'emp':emp}
  return render(request,'emp_profile.html',context)

def load_edit_emp_profile(request):
  emp = Employee.objects.get(user=request.user)
  context = {'usr':request.user, 'emp':emp}
  return render(request,'emp_profile_edit.html',context)

def edit_emp_profile(request):
  emp =  Employee.objects.get(user = request.user)
  if request.method == 'POST':
    email = request.POST['email']
    current_email = emp.user.email
    if email != current_email:
      if CustomUser.objects.filter(email=email).exists():
        messages.info(request,'Email Already in Use')
        return redirect('load_edit_emp_profile')
          
    phno_list = list(Employee.objects.exclude(user = request.user).values_list('contact', flat=True))

    if request.POST['phno'] in phno_list:
      messages.info(request,'Sorry, Phone number already in Use !!')
      return redirect('load_edit_emp_profile')

    emp.user.email = request.POST['email']
    emp.user.first_name = request.POST['fname']
    emp.user.last_name = request.POST['lname']
    emp.contact = request.POST['phno']
    old=emp.profile_pic
    new=request.FILES.get('image')
    if old!=None and new==None:
      emp.profile_pic=old
    else:
      emp.profile_pic=new
    
    emp.save() 
    emp.user.save() 
    return redirect('emp_profile') 

def load_staff_request(request):
  cmp = Company.objects.get(user = request.user)
  emp = Employee.objects.filter(company = cmp, is_approved = 0)
  context = {'usr':request.user, 'emp':emp, 'cmp':cmp}
  return render(request,'staff_request.html',context)

def load_staff_list(request):
  cmp = Company.objects.get(user = request.user)
  emp = Employee.objects.filter(company = cmp, is_approved = 1)
  context = {'usr':request.user, 'emp':emp, 'cmp':cmp}
  return render(request,'staff_list.html',context)

def accept_staff(request,id):
  emp = Employee.objects.get(id=id)
  emp.is_approved = 1
  emp.save()
  messages.info(request,'Employee Approved !!')
  return redirect('load_staff_request')

def reject_staff(request,id):
  emp = Employee.objects.get(id=id)
  emp.user.delete()
  emp.delete()
  messages.info(request,'Employee Deleted !!')
  return redirect('load_staff_request')

def item_list_first(request):
  if request.user.is_company:
    itm_list = Item.objects.filter(company = request.user.company)
  else:
    itm_list = Item.objects.filter(company = request.user.employee.company)
  
  if itm_list:
    itm = itm_list[0]
    trans = ItemTransactions.objects.filter(item = itm)
    context = {'itm_list':itm_list, 'usr':request.user, 'itm':itm, 'trans':trans}
  else:
    context = {'itm_list':itm_list, 'usr':request.user}
  return render(request,'item_list.html',context)

def item_list(request,id):
  if request.user.is_company:
    itm_list = Item.objects.filter(company = request.user.company)
  else:
    itm_list = Item.objects.filter(company = request.user.employee.company)
  
  itm = Item.objects.get(id=id)
  trans = ItemTransactions.objects.filter(item=itm.id)
  context = {'itm_list':itm_list, 'usr':request.user, 'itm':itm, 'trans':trans}
  return render(request,'item_list.html',context) 

def load_item_create(request):
  tod = timezone.now().date().strftime("%Y-%m-%d")
  if request.user.is_company:
    cmp = request.user.company
  else:
    cmp = request.user.employee.company
  unit = Unit.objects.filter(company=cmp)
  return render(request,'item_create.html',{'tod':tod, 'usr':request.user, 'unit':unit})

def item_create(request):
  if request.method=='POST':
    itm_type = request.POST.get('itm_type')
    itm_name = request.POST.get('name')
    itm_hsn = request.POST.get('hsn')
    itm_unit = request.POST.get('unit')
    itm_vat = request.POST.get('vat')
    taxable_result = request.POST.get('taxable_result')
    itm_sale_price = request.POST.get('sale_price')
    itm_purchase_price = request.POST.get('purchase_price')
    stock_in_hand = request.POST.get('stock_in_hand')
    if stock_in_hand == '' or None :
      stock_in_hand = 0
    itm_at_price = request.POST.get('at_price')
    if itm_at_price == '' or None:
      itm_at_price = 0
    itm_date = request.POST.get('itm_date')
    
    item = Item(user = request.user,
                itm_type = itm_type,
                itm_name = itm_name,
                itm_hsn = itm_hsn,
                itm_unit = itm_unit,
                itm_vat = itm_vat,
                itm_taxable = taxable_result,
                itm_sale_price = itm_sale_price,
                itm_purchase_price = itm_purchase_price,
                itm_stock_in_hand = stock_in_hand,
                itm_at_price = itm_at_price,
                itm_date = itm_date)
    item.save()

    trans = ItemTransactions(user = request.user, item = item, trans_type = 'Stock Open', trans_date = itm_date, trans_qty = 0, trans_current_qty = stock_in_hand, 
                         trans_adjusted_qty = stock_in_hand, trans_price = itm_at_price)

    if request.user.is_company:
      item.company = request.user.company
      trans.company = request.user.company

    else:
      item.company = request.user.employee.company
      trans.company = request.user.employee.company
 
    item.save()
    trans.save()

    trhis = ItemTransactionsHistory(user = request.user, transaction = trans, hist_trans_qty = 0, hist_trans_current_qty = stock_in_hand, action = 'Created',
                      hist_trans_adjusted_qty = stock_in_hand)
    trhis.save()

    if request.POST.get('save_and_next'):
      return redirect('load_item_create')
    elif request.POST.get('save'):
      return redirect('item_list_first')
    
def adjust_stock(request,id):
  if request.method=='POST':
    itm = Item.objects.get(id=id)
    if request.user.is_company:
      cmp = request.user.company
    else:
      cmp = request.user.employee.company

    trans_type = request.POST.get('trans_type')
    if trans_type == 'on':
      trans_type = 'Stock Reduction'
      trans_qty = request.POST.get('reduced_qty')
    else:
      trans_type = 'Stock Addition'
      trans_qty = request.POST.get('added_qty')
    trans_date = request.POST.get('trans_date')

    adjusted_qty= request.POST.get('adjusted_qty')
    current_qty = request.POST.get('item_qty')
    itm.itm_stock_in_hand = adjusted_qty
    itm.save()
    trans = ItemTransactions(user=request.user,
                          company=cmp,
                          item=itm,
                          trans_type=trans_type,
                          trans_date=trans_date,
                          trans_qty=trans_qty,
                          trans_current_qty=current_qty,
                          trans_adjusted_qty=adjusted_qty)
    trans.save()

    trhis = ItemTransactionsHistory(user = request.user, transaction = trans, hist_trans_qty = trans_qty, hist_trans_current_qty = current_qty, action = 'Created',
                      hist_trans_adjusted_qty = adjusted_qty)
    trhis.save()

  return redirect('item_list',id)

def create_unit(request):
  if request.method == 'POST':
    if request.user.is_company:
      cmp = request.user.company
    else:
      cmp = request.user.employee.company
    unit_name = request.POST.get('unit_name')
    unit = Unit(company=cmp, unit_name=unit_name)    
    unit.save()
    return JsonResponse({'message': 'success','unit_name':unit_name})
  
def load_item_edit(request,id):
  itm = Item.objects.get(id=id)
  context = {'usr':request.user, 'itm':itm}
  return render(request,'item_edit.html',context)
  
def item_edit(request,id):
  if request.method == 'POST':
    itm = Item.objects.get(id=id)
    itm.itm_type = request.POST.get('itm_type')
    itm.itm_name = request.POST.get('name')
    itm.itm_hsn = request.POST.get('hsn')
    itm.itm_unit = request.POST.get('unit')
    itm.itm_vat = request.POST.get('vat')
    itm.itm_taxable = request.POST.get('taxable_result')
    itm.itm_sale_price = request.POST.get('sale_price')
    itm.itm_purchase_price = request.POST.get('purchase_price')

    stock_in_hand = request.POST.get('stock_in_hand')
    if stock_in_hand == '' or None :
      stock_in_hand = 0
    itm.itm_stock_in_hand = stock_in_hand

    itm_at_price = request.POST.get('at_price')
    if itm_at_price == '' or None:
      itm_at_price = 0
    itm.itm_at_price = itm_at_price

    itm.itm_date = request.POST.get('itm_date')
    itm.save()

    trans = ItemTransactions.objects.get(item=itm, trans_type='Stock Open')
    trans.trans_current_qty = stock_in_hand
    trans.trans_adjusted_qty = stock_in_hand
    trans.trans_date = request.POST.get('itm_date')
    trans.save()
    
    trhis = ItemTransactionsHistory(user = request.user, transaction = trans, hist_trans_qty = 0, hist_trans_current_qty = stock_in_hand, action = 'Updated',
                      hist_trans_adjusted_qty = stock_in_hand)
    trhis.save()

    if request.POST.get('save_and_next'):
      return redirect('load_item_create')
    elif request.POST.get('save'):
      return redirect('item_list',id)
    
def load_trans_details(request):
  id = request.POST.get('id')
  trans = ItemTransactions.objects.get(id=id)
  trans_id = trans.id
  name = trans.item.itm_name
  date = trans.trans_date.strftime("%Y-%m-%d")
  current_qty = trans.trans_current_qty
  qty = trans.trans_qty
  adj_qty = trans.trans_adjusted_qty
  trans_type = trans.trans_type
  return JsonResponse({'message': 'success',
                       'trans_id':trans_id,
                       'name':name, 
                       'date':date,
                       'current_qty':current_qty, 
                       'qty':qty, 
                       'adj_qty':adj_qty, 
                       'trans_type':trans_type})

def edit_transactions(request):
  if request.method=='POST':
    id = request.POST.get('id')
    trans_stock_change = request.POST.get('trans_stock_change')
    trans_itm_date = request.POST.get('trans_itm_date')
    trans_item_quantity = request.POST.get('trans_item_quantity')
    stock_value = request.POST.get('stock_value')
    trans_adj_quantity = request.POST.get('trans_adj_quantity')

    trans = ItemTransactions.objects.get(id=id)
    trans.trans_type = trans_stock_change
    trans.trans_date = trans_itm_date
    trans.trans_qty = stock_value 
    trans.trans_current_qty = trans_item_quantity
    trans.trans_adjusted_qty = trans_adj_quantity
    trans.save()
    trans.item.itm_stock_in_hand = trans_adj_quantity
    trans.item.save()

    trhis = ItemTransactionsHistory(user = request.user, transaction = trans, hist_trans_qty = stock_value, hist_trans_current_qty = trans_item_quantity, action = 'Updated',
                      hist_trans_adjusted_qty = trans_adj_quantity)
    trhis.save()
    return JsonResponse({'message': 'success'})

def delete_item(request,id):
  Item.objects.get(id=id).delete()
  messages.info(request,'Item Deleted Successfully !!')
  return redirect('item_list_first')

def delete_transaction(request,id):
  ItemTransactions.objects.get(id=id).delete()
  messages.info(request,'Item Transaction Deleted Successfully !!')
  return redirect('item_list_first')

def load_itm_trans_history(request,id):
  trans = ItemTransactions.objects.get(id=id)
  trhis = ItemTransactionsHistory.objects.filter(transaction=trans)
  context = {'usr':request.user, 'trans':trans, 'trhis':trhis}
  return render(request,'item_transaction_history.html',context)