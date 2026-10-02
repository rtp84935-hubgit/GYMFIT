from datetime import date, datetime
from django.contrib import messages

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from myapp.models import *
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate,login,logout 

# Create your views here.


# ==================================login==========================================

def logout_page(request):
    logout(request)
    return redirect('/myapp/login/')

def login_page(request):
    return render(request,'login.html')

def login_post(request):
    
    if request.method != 'POST':
        return JsonResponse({'status': 'invalid_request'})

    username = request.POST.get('username')
    password = request.POST.get('password')

   

    ob = authenticate(username=username, password=password)
    
    if ob is None:
        return JsonResponse({'status': 'invalid'})

    if ob.groups.filter(name='client').exists():
        login(request, ob)
        return JsonResponse({'status': 'client'})

    if ob.groups.filter(name='trainer').exists():

        login(request, ob)
        a=Trainer.objects.get(LOGIN=ob).status
        print(a)
        if a=='approved':
            print('kooooooooooooooioioio')
            return JsonResponse({'status': 'approve'})
        elif a=='rejected':
            return JsonResponse({'status': 'reject'})
        elif a=='pending':
            return JsonResponse({'status': 'pend'})
        
           
    if ob.groups.filter(name='admin').exists():
        login(request, ob)
        return JsonResponse({'status': 'admin'})
    

    # User exists but belongs to no recognized group
    return JsonResponse({'status': 'no_group'})
    

    
# ====================================admin============================= 
def view_all_trainers(request):
    ob=Trainer.objects.filter(status='approved')
    return render(request,'admin/view_all_trainers.html',{'trainers':ob})

def view_all_client(request):
    ob=Client.objects.all()
    return render(request,'admin/view_all_client.html',{'client':ob})

def admin_home(request):
    return render(request,'admin/admin_home.html')

def view_trainer_requests(request):
    ob=Trainer.objects.filter(status='pending')
    return render(request,'admin/view_trainer_requests.html',{'training':ob})

def view_rejected_trainers(request):
    ob=Trainer.objects.filter(status='rejected')
    return render(request,'admin/view_rejected_trainers.html',{'train':ob})


def reject_trainer(request,id):
    user=Trainer.objects.filter(id=id).update(status='rejected')
    return redirect('/myapp/view_trainer_requests/')

def verify_trainer(request,id):
    user=Trainer.objects.filter(id=id).update(status='approved')
    return redirect('/myapp/view_trainer_requests/')

def reject_approved_trainer(request,id):
    user=Trainer.objects.filter(id=id).update(status='rejected')
    return redirect('/myapp/view_all_trainers/')

def admin_changepassword(request):
    return render(request,'admin/admin_changepassword.html')

def admin_changepassword_post(request):
    current_password = request.POST['current_password']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']
    print(current_password,'sdfghjklkjhgfdsdfghjkjhgfd',new_password,confirm_password)
    user = request.user

    if not user.check_password(current_password):
        return JsonResponse({'status':'currentpassno'})
    
    elif new_password != confirm_password:
        return JsonResponse({'status':'nomatch'})

    else:
        user.set_password(new_password)
        user.save()
        return JsonResponse({'status':'yes'})

def add_premium(request):
    return render(request,'admin/add_premium.html')

def add_premium_post(request):
    title=request.POST['title']
    video=request.FILES['video']

    ob=PremiumVideo()
    ob.title=title
    ob.video=video
    ob.date=datetime.now()
    ob.save()
    return redirect('/myapp/admin_home/')

def view_premium_admin(request):
    ob=PremiumVideo.objects.all()
    return render(request,'admin/view_premium.html',{'premium':ob})

def view_premium_video(request):
    if PremiumMembership.objects.filter(CLIENT__LOGIN=request.user).exists():
        a=PremiumMembership.objects.get(CLIENT__LOGIN=request.user).EXPD
        ob=PremiumVideo.objects.all()
        tody=datetime.now().date()

        if a>tody:
            return render(request,'client/view_premium_video.html',{'premium':ob})
        else:
            return HttpResponse(' premium membership required')
        
    return HttpResponse(' premium membership required')
    

    





    





# =================================client================================= #

def client_home(request):
    trainer = Trainer.objects.all()
    requests = Requests.objects.filter(CLIENT__LOGIN=request.user)
    diet = Dietplan.objects.filter(CLIENT__LOGIN=request.user).order_by('-date')
    tip = Tip.objects.all()
    for t in trainer:
        t.request = requests.filter(TRAINER=t).first()
    
    if  PremiumMembership.objects.filter(CLIENT__LOGIN=request.user).exists():
            a=PremiumMembership.objects.get(CLIENT__LOGIN=request.user).EXPD
            tody=datetime.now().date()
            if tody<=a:
                return render(request, 'client/client_home.html', {
                'trainer': trainer,
                'requests': requests,
                'diet': diet,
                'tips':tip,
                'status':'active'
            })
            else:
                print('hiiiiiiiiiiiiiiiiiiiiiiiiii')
                return render(request, 'client/client_home.html', {
                'trainer': trainer,
                'requests': requests,
                'diet': diet,
                'tips':tip,
                'status':'expired'
            })



    return render(request, 'client/client_home.html', {
        'trainer': trainer,
        'requests': requests,
        'diet': diet,
        'tips':tip,
        'status':'no'
    })





def searchtrainer(request):
    name = request.GET.get('name', '')
    trainer = Trainer.objects.filter(tname__icontains=name)
    requests = Requests.objects.filter(CLIENT__LOGIN=request.user)

    return render(request, 'client/view_trainer_cards.html', {
        'trainer': trainer,
        'requests': requests
    })


def client_signup(request):
    return render(request,'client/client_signup.html')

def client_signup_post(request):
    cname=request.POST['cname']
    cage=request.POST['cage']
    cplace=request.POST['cplace']
    cemail=request.POST['cemail']
    password=request.POST['password']

    a=User.objects.create_user(username=cemail,password=password)
    a.groups.add(Group.objects.get(name='client'))
    ob=Client()
    ob.cname=cname
    ob.cage=cage
    ob.cplace=cplace
    ob.cemail=cemail
    ob.LOGIN=a
    ob.save()
    return JsonResponse({'status':'yes'})

def check_username_client(request):
    username=request.GET.get('username')
    if Client.objects.filter(cemail=username).exists():
        return JsonResponse({'status':'yes'})
    else:
        return JsonResponse({'status':'no'})
    
def view_trainer(request):
    ob=Trainer.objects.filter(status='approved')
    return render(request,'client/client_home.html',{'trainer':ob})

def send_admission_request(request,id):
    if Requests.objects.filter(CLIENT__LOGIN=request.user,TRAINER_id=id).exists():
        return redirect('/myapp/client_home/')
    else:
        ob=Requests()
        ob.date=datetime.now()
        ob.status='pending'
        ob.CLIENT=Client.objects.get(LOGIN=request.user)
        ob.TRAINER=Trainer.objects.get(id=id)
        ob.save()
        messages.success(request,'request sended successfully')
        return redirect('/myapp/client_home/')
    
def client_changepassword(request):
    return render(request,'admin/client_changepassword.html')

def client_viewprofile(request):
    ob=Client.objects.get(LOGIN=request.user)
    return render(request,'client/client_viewprofile.html',{'data':ob})

def edit_clientprofile(request):
    ob=Client.objects.get(LOGIN=request.user)
    return render(request,'client/client_viewprofile.html',{'data':ob})

def edit_clientprofile_post(request):
    cage=request.POST['cage']
    cname=request.POST['cname']
    cplace=request.POST['cplace']
    cemail=request.POST['cemail']
    ob=Client.objects.get(LOGIN=request.user)
    obb=request.user
    obb.username=cemail
    obb.save()
    ob.cname=cname
    ob.cage=cage
    ob.cplace=cplace
    ob.cemail=cemail
    ob.save()
    return JsonResponse({'status':'yes'})

def view_diet_plan(request):
    ob=Dietplan.objects.filter(CLIENT__LOGIN=request.user)
    return render(request,'client/client_home.html',{'diet':ob})

def view_tip(request):
    ob=Tip.objects.all()
    return render(request,'client/client_home.html',{'tips':ob})

def premium(request):
    return render(request,'premium.html')


def Membership(request):
    from datetime import datetime,timedelta
    ob=PremiumMembership()
    duration=request.POST['duration']
    if duration == '3':
        ob.duration=90
        ob.DOR=datetime.now().date()
        tod=datetime.now().date()
        ob.EXPD=tod+timedelta(days=90)
        ob.Price=2499
        ob.CLIENT=Client.objects.get(LOGIN=request.user)
        ob.save()
        return redirect('/myapp/client_home/')
    elif duration == '6' :
        ob.duration=180
        ob.DOR=datetime.now().date()
        tod=datetime.now().date()
        ob.EXPD=tod+timedelta(days=180)
        ob.Price=2249
        ob.CLIENT=Client.objects.get(LOGIN=request.user)
        ob.save()
        return redirect('/myapp/client_home/')
    else:
        ob.duration=365
        ob.DOR=datetime.now().date()
        tod=datetime.now().date()
        ob.EXPD=tod+timedelta(days=365)
        ob.Price=1999
        ob.CLIENT=Client.objects.get(LOGIN=request.user)
        ob.save()
        return redirect('/myapp/client_home/')
    
def renew_membership(request):
    return render(request,'client/renew_membership.html')

def renew_membership_post(request):
    from datetime import datetime,timedelta
    mid=PremiumMembership.objects.get(CLIENT__LOGIN=request.user).id
    ob=PremiumMembership.objects.get(id=mid)
    duration=request.POST['duration']
    if duration == '3':
        ob.duration=90
        ob.DOR=datetime.now().date()
        tod=datetime.now().date()
        ob.EXPD=tod+timedelta(days=90)
        ob.Price=2499
        ob.CLIENT=Client.objects.get(LOGIN=request.user)
        ob.save()
        return redirect('/myapp/client_home/')
    elif duration == '6' :
        ob.duration=180
        ob.DOR=datetime.now().date()
        tod=datetime.now().date()
        ob.EXPD=tod+timedelta(days=180)
        ob.Price=2249
        ob.CLIENT=Client.objects.get(LOGIN=request.user)
        ob.save()
        return redirect('/myapp/client_home/')
    else:
        ob.duration=365
        ob.DOR=datetime.now().date()
        tod=datetime.now().date()
        ob.EXPD=tod+timedelta(days=365)
        ob.Price=1999
        ob.CLIENT=Client.objects.get(LOGIN=request.user)
        ob.save()
        return redirect('/myapp/client_home/')
    

        


    
# ====================================trainer==========================================

def trainer_changepassword(request):
    return render(request,'admin/trainer_changepassword.html')

def trainer_home(request):
    return render(request,'trainer/trainer_home.html')

def trainer_signup(request):
    return render(request,'trainer/trainer_signup.html')

def trainer_signup_post(request):
    tname=request.POST['tname']
    tage=request.POST['tage']
    tplace=request.POST['tplace']
    temail=request.POST['temail']
    password=request.POST['password']
    specification=request.POST['specification']
    experience=request.POST['experience']
    photo=request.FILES['photo']

    if User.objects.filter(username=temail).exists():
        return JsonResponse({'status':'no'})
    else:
        a=User.objects.create_user(username=temail,password=password)
        a.groups.add(Group.objects.get(name='trainer'))
        ob=Trainer()
        ob.tname=tname
        ob.tage=tage
        ob.tplace=tplace
        ob.temail=temail
        ob.specification=specification
        ob.experience=experience
        ob.photo=photo
        ob.LOGIN=a
        ob.save()
        return JsonResponse({'status':'yes'})

def check_email(request):
    username=request.GET.get('temail')
    if Trainer.objects.filter(temail=username).exists():
        return JsonResponse({'status':'yes'})
    else:
        return JsonResponse({'status':'no'})
    
def view_admission_request(request):
    ob=Requests.objects.filter(TRAINER__LOGIN=request.user)
    return render(request,'trainer/view_admission_request.html',{'req':ob})

def accept_request(request,id):
    ob=Requests.objects.get(id=id)
    ob.status='accepted'
    ob.save()
    return redirect('/myapp/view_admission_request/')
    

def reject_request(request,id):
    ob=Requests.objects.get(id=id)
    ob.status='rejected'
    ob.save()
    return redirect('/myapp/view_admission_request/')

def view_members(request):
    ob=Requests.objects.filter(TRAINER__LOGIN=request.user,status='accepted')
    return render(request,'view_members.html',{'members':ob})
   
def trainer_deit_home(request):
    return render(request,'trainer/trainer_diet_home.html')

def add_diet(request):
    ob=Requests.objects.filter(TRAINER__LOGIN=request.user,status='accepted')
    return render(request,'trainer/add_diet.html',{'client':ob})


def add_diet_post(request):
    if request.method == "POST":

        dietplan = request.POST['dietplan']
        cid = request.POST['client']
        date = request.POST['date']

        ob = Dietplan()
        ob.CLIENT = Client.objects.get(id=cid)
        ob.TRAINER = Trainer.objects.get(LOGIN=request.user)
        ob.date = date
        ob.dietplan = dietplan
        ob.save()

        return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'error'})

def view_diet_trainer(request):
    ob=Dietplan.objects.filter(TRAINER__LOGIN=request.user)
    return render(request,'trainer/view_diet_trainer.html',{'diet':ob})

def edit_diet_plan(request, id):
    diet = Dietplan.objects.get(id=id)

    client = Requests.objects.filter(
        TRAINER__LOGIN=request.user,
        status='accepted'
    )

    return render(request, 'trainer/edit_diet_plan.html', {
        'diet': diet,
        'client': client
    })

def edit_diet_plan_post(request, id):
    if request.method == "POST":

        ob = Dietplan.objects.get(id=id)

        ob.CLIENT = Client.objects.get(id=request.POST['client'])
        ob.TRAINER = Trainer.objects.get(LOGIN=request.user)
        ob.date = request.POST['date']
        ob.dietplan = request.POST['dietplan']

        ob.save()

        return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'error'})

def delete_diet(request,id):
    ob=Dietplan.objects.get(id=id)
    ob.delete()
    return redirect('/myapp/view_diet_trainer/')

def add_tip(request):
    return render(request,'trainer/add_tip.html')

def add_tip_post(request):

    if request.method == "POST":

        date = request.POST['date']
        tip = request.POST['tip']

        trainer = Trainer.objects.get(LOGIN=request.user)

        ob = Tip()
        ob.TRAINER = trainer
        ob.date = date
        ob.tip = tip
        ob.save()

        return JsonResponse({'status':'ok'})

    return JsonResponse({'status':'error'})

def view_tip_trainer(request):
    ob=Tip.objects.filter(TRAINER__LOGIN=request.user)
    return render(request,'trainer/view_tip_trainer.html',{'tips':ob})

def edit_tip(request,id):
    ob=Tip.objects.get(id=id)
    return render(request,'trainer/edit_tip.html',{'tip':ob})

def edit_tip_post(request,id):
    if request.method == "POST":

        date = request.POST['date']
        tip = request.POST['tip']

        trainer = Trainer.objects.get(LOGIN=request.user)

        ob = Tip.objects.get(id=id)
        ob.TRAINER = trainer
        ob.date = date
        ob.tip = tip
        ob.save()

        return JsonResponse({'status':'ok'})

    return JsonResponse({'status':'error'})


