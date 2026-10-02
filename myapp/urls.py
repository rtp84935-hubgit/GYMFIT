"""
URL configuration for sample2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from myapp import views

urlpatterns = [
    path('login/',views.login_page),
    path('login_post/',views.login_post),
    path('logout/',views.logout_page),
    # ======================client============================
    path('client_home/',views.client_home),
    path('client_signup/',views.client_signup),
    path('client_signup_post/',views.client_signup_post),
    path('check_username_client/',views.check_username_client),
    path('send_admission_request/<id>',views.send_admission_request),
    path('searchtrainer/',views.searchtrainer),
    path('client_changepassword/',views.client_changepassword), 
    path('client_viewprofile/',views.client_viewprofile),
    path('edit_clientprofile/',views.edit_clientprofile),
    path('Membership/',views.Membership),
    path('view_premium_video/',views.view_premium_video),
    path('renew_membership/',views.renew_membership),
    path('renew_membership_post/',views.renew_membership_post),

    # =====================trainer===========================
    path('trainer_home/',views.trainer_home),
    path('trainer_signup/',views.trainer_signup),
    path('trainer_signup_post/',views.trainer_signup_post),
    path('check_email/',views.check_email),
    path('view_admission_request/',views.view_admission_request),
    path('accept_request/<id>',views.accept_request),
    path('reject_request/<id>',views.reject_request),
    path('view_members/',views.view_members),
    path('trainer_changepassword/',views.trainer_changepassword),
    path('trainer_deit_home/',views.trainer_deit_home),
    path('add_diet/',views.add_diet),
    path('add_diet_post/',views.add_diet_post),
    path('view_diet_trainer/',views.view_diet_trainer),
    path('edit_diet_plan/<int:id>/', views.edit_diet_plan, name='edit_diet_plan'),
    path('edit_diet_plan_post/<int:id>/', views.edit_diet_plan_post, name='edit_diet_plan_post'),
    path('delete_diet/<id>',views.delete_diet),
    path('add_tip/', views.add_tip),
    path('add_tip_post/', views.add_tip_post),
    path('view_tip_trainer/',views.view_tip_trainer),
    path('edit_tip/<id>',views.edit_tip),
    path('edit_tip_post/<id>',views.edit_tip_post),




    # ========================admin======================
    path('view_all_trainers/',views.view_all_trainers),
    path('admin_home/',views.admin_home),
    path('view_all_client/',views.view_all_client),
    path('view_trainer_requests/',views.view_trainer_requests),
    path('reject_trainer/<id>',views.reject_trainer),
    path('verify_trainer/<id>',views.verify_trainer),
    path('view_rejected_trainers/',views.view_rejected_trainers),
    path('reject_approved_trainer/<id>',views.reject_approved_trainer),
    path('admin_changepassword/',views.admin_changepassword),
    path('admin_changepassword_post/',views.admin_changepassword_post),
    path('view_premium/',views.view_premium_admin),
    path('add_premium/',views.add_premium),
    path('add_premium_post/',views.add_premium_post)
    






    




]
