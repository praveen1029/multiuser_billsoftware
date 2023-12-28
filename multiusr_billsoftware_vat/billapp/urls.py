from django.urls import re_path,path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [

    path('',views.home,name='home'),
    path('cmp_register/',views.cmp_register,name='cmp_register'),
    path('login/',views.login,name='login'),
    path('cmp_details/<int:id>/',views.cmp_details,name='cmp_details'),
    path('emp_register/',views.emp_register,name='emp_register'),
    path('cmp_dash/',views.cmp_dash,name='cmp_dash'),
    path('emp_dash/',views.emp_dash,name='emp_dash'),
     
    path('register_company',views.register_company,name='register_company'),  
    path('register_company_details/<int:id>',views.register_company_details,name='register_company_details'),
    path('register_employee',views.register_employee,name='register_employee'),  
    path('user_login',views.user_login,name='user_login'),  

]
