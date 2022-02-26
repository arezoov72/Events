


from django.http import request

from django.db import models
from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django_jalali.db.models import jDateField
from requests import auth
from requests.adapters import SSLError
from urllib3.connection import VerifiedHTTPSConnection
from .models import Event
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from datetime import date, datetime,timedelta

from django.db.models import F
from django.contrib.auth.models import User

from jalali_date import datetime2jalali, date2jalali,jdatetime
from .forms import TestForm
from time import sleep
# Create your views here.

def home(request):
    return redirect('event_page')





import os 
def event_page(request):
    allevents=Event.objects.all()
    compare_date=Event.objects.all().filter(date=date.today())
    current_user = os.environ.get("USERNAME")
    selected_user=Event.objects.all().filter(tousers=current_user).filter(date=date.today())
    main_user=Event.objects.all().filter(tousers=F('username')).filter(date=date.today())
    
    #selected_user=Event.objects.all().filter(tousers='fallah').order_by('-id')[0]
    if compare_date:
        if selected_user:
            
            print(selected_user)
            #print(str(compare_date))
            print(current_user)
            return render (request,'event.html',{"allevents":allevents})
        
        elif main_user:
            print(main_user)
            return render (request,'event.html',{"allevents":allevents})  
            
                
        else:
            print(date)
            return HttpResponse('<script type="text/javascript">setTimeout(window.close, 1);</script>')
        #print(selected_user)
        print(compare_date)
        print(current_user)

    else:
        #print(selected_user)
        print(compare_date)
        print(current_user)
        
        # browserExe = "chrome.exe" 
        # os.system("taskkill /f /im "+browserExe) 
        return HttpResponse('<script type="text/javascript">setTimeout(window.close, 1);</script>')


@login_required(login_url='/event/login/')
def adminpanel(request):
    
    form=TestForm(request.POST)
    if request.user.is_authenticated and request.user.has_perm('lotus_cooperators.is_manager') :
        if request.method=="POST":
            form=TestForm(request.POST)
            username_id= request.user
            fullname =  request.user.get_full_name()
            title=request.POST['title']
            picture=request.FILES.get('picture',0)
            event=request.POST['event']
            information=request.POST['information']
            date = request.POST['date']
            tousers = request.POST['tousers']
            #user = User.objects.get(username=tousers2)
            if tousers=='':
                user=request.user
            else:
                user = User.objects.get(username=tousers)


            tousers = user
            #date_time=JalaliToGregorian(date)
            #date = datetime2jalali(request.POST['date']).strftime('%y/%m/%d _ %H:%M:%S')
            #date_time = jdatetime.date(date).togregorian()
            event_obj=Event(title=title,picture=picture,event=event,information=information,username_id=username_id,date=date,tousers=tousers)
            event_obj.save()
          
            print(date)
    else:
        return HttpResponseRedirect('/event/login')  
 
    return render(request,'adminpannel.html',{'form':form})


def send_selected_combo(self):
    value_from_select = self.request.GET.get('hokmtime')
    return value_from_select

#from lotusCoorperators.lotus_cooperators import models
from lotus_cooperators.models import employee
#from lotus_cooperators.models import employee


import jdatetime
from jdatetime import j_days_in_month,GregorianToJalali,JalaliToGregorian
from persiantools.jdatetime import JalaliDate
from django.db.models import Q
from itertools import chain


@login_required(login_url='/event/login/')
def birthdayreminder(request):

    #today=JalaliDate.today()

    #jalili_date =  jdatetime.date.fromgregorian(day=today.day,month=today.month,year=today.year)
    #jalili_date2 =  jdatetime.date.fromgregorian(day=birthdate__day,month=birthdate__month,year=birthdate__year)
    today=date.today()
    if today.month != 12:
        next_month = datetime(year=today.year, month=today.month+1, day=1)
    else:
        next_month=datetime(year=today.year+1, month=1, day=1)
    last_day_month = next_month - timedelta(days=1)
    twoweeks=(today+timedelta(days=14))
    allbirth=employee.objects.all().filter(birthdate__month__range=[today.month,twoweeks.month],birthdate__day__range=[today.day,twoweeks.day]).exclude(postid=70).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
    Employment=employee.objects.all().filter(EmploymentDate__month__range=[today.month,twoweeks.month],EmploymentDate__day__range=[today.day,twoweeks.day]).exclude(postid=70).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['-EmploymentDate_month','EmploymentDate_day'])
    Hokm=employee.objects.all().filter(EmploymentDate__month__range=[today.month,twoweeks.month],EmploymentDate__day__range=[today.day,twoweeks.day]).exclude(postid=70).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['-EmploymentDate_month','EmploymentDate_day'])
    
    hokm3mah=today-timedelta(days=93)
    
    Hokm1sal=today-timedelta(days=365)
    
    Hokm2sal=Hokm1sal-timedelta(days=365)
    Hokm4sal=today-timedelta(days=(365*4))
    Hokm6sal=today-timedelta(days=(365*6))
    Hokm8sal=today-timedelta(days=(365*8))
    Hokm10sal=today-timedelta(days=(365*10))
    Hokm12sal=today-timedelta(days=(365*12))
    
    
    weekdaylist=14-(last_day_month.day - today.day)
    if (last_day_month.day - today.day) < 14:

            allbirth1=employee.objects.all().filter(birthdate__month=today.month ,birthdate__day__range=[today.day,last_day_month.day]
            ).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day']).exclude(postid=70)
            allbirth2=employee.objects.all().filter(birthdate__month=twoweeks.month ,birthdate__day__range=[1,weekdaylist]
            ).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day']).exclude(postid=70)
            allbirth=list(chain(allbirth1,allbirth2))

            Employment1=employee.objects.all().filter(EmploymentDate__month=today.month ,EmploymentDate__day__range=[today.day,last_day_month.day]
            ).exclude(postid=70).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['EmploymentDate_month','EmploymentDate_day'])
            Employment2=employee.objects.all().filter(EmploymentDate__month=twoweeks.month ,EmploymentDate__day__range=[1,weekdaylist]
            ).exclude(postid=70).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['EmploymentDate_month','EmploymentDate_day'])
            Employment=list(chain(Employment1,Employment2))
           
    else:
            

        allbirth=employee.objects.all().filter(birthdate__month__range=[today.month,twoweeks.month],birthdate__day__range=[today.day,twoweeks.day]).exclude(postid=70).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
        Employment=employee.objects.all().filter(EmploymentDate__month__range=[today.month,twoweeks.month],EmploymentDate__day__range=[today.day,twoweeks.day]).exclude(postid=70).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['-EmploymentDate_month','EmploymentDate_day'])


    
    
    
   
    
    if request.method=="POST":
        allbirth=employee.objects.all().exclude(postid=70).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
        selectedtime=request.POST.get('selectedtime',' ')
   
        empbirth=request.POST.get('empbirth',' ')
        hokmtime=request.POST.get('hokmtime',' ')
        tolerance=request.POST.get('tolerance','')
        print(tolerance)
        if tolerance == '':
            tolerance= 7

        

        if hokmtime =='3ماه':
            tolerance1=hokm3mah-timedelta(days=int(tolerance))
            tolerance2=hokm3mah+timedelta(days=int(tolerance))
            value_from_select =request.GET.get('hokmtime')
            
            Hokm=employee.objects.all().filter(EmploymentDate__range=[tolerance1,tolerance2]).exclude(postid=70)
            
            print(hokmtime)
            print(value_from_select)
            

            return render(request,'birth.html',{"Hokm":Hokm,hokmtime:hokmtime,value_from_select:value_from_select})
        elif hokmtime =='1سال':
            
            tolerance1=Hokm1sal-timedelta(days=int(tolerance))
            tolerance2=Hokm1sal+timedelta(days=int(tolerance))
            Hokm=employee.objects.all().filter(EmploymentDate__range=[tolerance1,tolerance2]).exclude(postid=70)
            
            print(tolerance1)
            print(hokmtime)
            print(Hokm1sal)
            return render(request,'birth.html',{"Hokm":Hokm,'hokmtime':hokmtime})
        elif hokmtime =='2سال':
            tolerance1=Hokm2sal-timedelta(days=int(tolerance))
            tolerance2=Hokm2sal+timedelta(days=int(tolerance))
            Hokm=employee.objects.all().filter(EmploymentDate__range=[tolerance1,tolerance2]).exclude(postid=70)
            
            return render(request,'birth.html',{"Hokm":Hokm})
        elif hokmtime =='4سال':
            tolerance1=Hokm4sal-timedelta(days=int(tolerance))
            tolerance2=Hokm4sal+timedelta(days=int(tolerance))
            Hokm=employee.objects.all().filter(EmploymentDate__range=[tolerance1,tolerance2]).exclude(postid=70)
            
            print(tolerance)
 
            return render(request,'birth.html',{"Hokm":Hokm})
        elif hokmtime =='6سال':
            tolerance1=Hokm6sal-timedelta(days=int(tolerance))
            tolerance2=Hokm6sal+timedelta(days=int(tolerance))
            Hokm=employee.objects.all().filter(EmploymentDate__range=[tolerance1,tolerance2]).exclude(postid=70)
            
 
            return render(request,'birth.html',{"Hokm":Hokm})
        elif hokmtime =='8سال':
            tolerance1=Hokm8sal-timedelta(days=int(tolerance))
            tolerance2=Hokm8sal+timedelta(days=int(tolerance))
            Hokm=employee.objects.all().filter(EmploymentDate__range=[tolerance1,tolerance2]).exclude(postid=70)
            
 
            return render(request,'birth.html',{"Hokm":Hokm})
        elif hokmtime =='10سال':
            tolerance1=Hokm10sal-timedelta(days=int(tolerance))
            tolerance2=Hokm10sal+timedelta(days=int(tolerance))
            Hokm=employee.objects.all().filter(EmploymentDate__range=[tolerance1,tolerance2]).exclude(postid=70)
         
 
            return render(request,'birth.html',{"Hokm":Hokm})
        elif hokmtime =='12سال':
            tolerance1=Hokm12sal-timedelta(days=int(tolerance))
            tolerance2=Hokm12sal+timedelta(days=int(tolerance))
            Hokm=employee.objects.all().filter(EmploymentDate__range=[tolerance1,tolerance2]).exclude(postid=70)
          
 
            return render(request,'birth.html',{"Hokm":Hokm})
        elif selectedtime == 'امروز':
            
            allbirth=employee.objects.all().filter(birthdate__day=today.day,birthdate__month=today.month).exclude(postid=70).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
            Employment=employee.objects.all().filter(EmploymentDate__day=today.day,EmploymentDate__month=today.month).exclude(postid=70).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['-EmploymentDate_month','EmploymentDate_day'])
         
            
            return render(request,'birth.html',{"allbirth":allbirth,"Employment":Employment})
        elif selectedtime == 'هفته':
            today=date.today()
            #today=JalaliDate.today()
            
            week=(today+timedelta(days=7))

            allbirth=employee.objects.all().filter(birthdate__month__range=[today.month,week.month],birthdate__day__range=[today.day,week.day]).exclude(postid=70).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
            Employment=employee.objects.all().filter(EmploymentDate__month__range=[today.month,week.month],EmploymentDate__day__range=[today.day,week.day]).exclude(postid=70).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['-EmploymentDate_month','EmploymentDate_day'])
            
            print(allbirth)
            print(today)
            print(week)
            
            

            return render(request,'birth.html',{"allbirth":allbirth,"Employment":Employment})
        elif selectedtime == 'دوهفته':
            today=date.today()
            today1=JalaliDate.today()
            next_month = datetime(year=today.year, month=today.month+1, day=1)
            last_day_month = next_month - timedelta(days=1)
            twoweeks=(today+timedelta(days=14))
            twoweeks1=(today1+timedelta(days=14))
            weekdaylist=14-(last_day_month.day - today.day)
            if (last_day_month.day - today.day) < 14:

                allbirth1=employee.objects.all().filter(birthdate__month=today.month ,birthdate__day__range=[today.day,last_day_month.day]
                ).exclude(postid=70).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
                allbirth2=employee.objects.all().filter(birthdate__month=twoweeks.month ,birthdate__day__range=[1,weekdaylist]
                ).exclude(postid=70).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
                allbirth=list(chain(allbirth1,allbirth2))

                Employment1=employee.objects.all().filter(EmploymentDate__month=today.month ,EmploymentDate__day__range=[today.day,last_day_month.day]
                ).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['EmploymentDate_month','EmploymentDate_day'])
                Employment2=employee.objects.all().filter(EmploymentDate__month=twoweeks.month ,EmploymentDate__day__range=[1,weekdaylist]
                ).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['EmploymentDate_month','EmploymentDate_day'])
                Employment=list(chain(Employment1,Employment2))
                
            else:
            

                allbirth=employee.objects.all().filter(birthdate__month__range=[today.month,twoweeks.month],birthdate__day__range=[today.day,twoweeks.day]).exclude(postid=70).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
                Employment=employee.objects.all().filter(EmploymentDate__month__range=[today.month,twoweeks.month],EmploymentDate__day__range=[today.day,twoweeks.day]).exclude(postid=70).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['-EmploymentDate_month','EmploymentDate_day'])
                
            print(allbirth)
            print(today)
            print(last_day_month)
            print(twoweeks)
            print(twoweeks1)
            
            print(hokm3mah)
            

            return render(request,'birth.html',{"allbirth":allbirth,"Employment":Employment})
        elif selectedtime == 'ماه':
            today=date.today()
            inmonth=(today+timedelta(days=31))
            next_month = datetime(year=today.year, month=today.month+1, day=1)
            last_day_month = next_month - timedelta(days=1)
            monthlist=31-(last_day_month.day - today.day)
            if (last_day_month.day - today.day) < 31:

                allbirth1=employee.objects.all().filter(birthdate__month=today.month ,birthdate__day__range=[today.day,last_day_month.day]
                ).exclude(postid=70).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
                allbirth2=employee.objects.all().filter(birthdate__month=inmonth.month ,birthdate__day__range=[1,monthlist]
                ).exclude(postid=70).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
                allbirth=list(chain(allbirth1,allbirth2))

                Employment1=employee.objects.all().filter(EmploymentDate__month=today.month ,EmploymentDate__day__range=[today.day,last_day_month.day]
                ).exclude(postid=70).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['EmploymentDate_month','EmploymentDate_day'])
                Employment2=employee.objects.all().filter(EmploymentDate__month=inmonth.month ,EmploymentDate__day__range=[1,monthlist]
                ).exclude(postid=70).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['EmploymentDate_month','EmploymentDate_day'])
                Employment=list(chain(Employment1,Employment2))
                
            else:

                allbirth=employee.objects.all().filter(birthdate__month=today.month).exclude(postid=70).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
                Employment=employee.objects.all().filter(EmploymentDate__month=today.month).exclude(postid=70).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['-EmploymentDate_month','EmploymentDate_day'])
                
            print(allbirth)
            print(today)
            print(last_day_month)
            
           
            return render(request,'birth.html',{"allbirth":allbirth,"Employment":Employment})



        elif empbirth =='فروردین':
            start_farvardin=jdatetime.date(1342,1,1).togregorian()
            end_farvardin=jdatetime.date(1342,1,31).togregorian()
            #jalili_date =  jdatetime.date.fromgregorian(day=19,month=5,year=2017) 
            

            end_farvardin2=jdatetime.date.fromgregorian(day=today.day,month=today.month,year=today.year)

            allbirth=employee.objects.all().filter(Q(birthdate__contains='03-21')|Q(birthdate__contains='03-22')|Q(birthdate__contains='03-23')|Q(birthdate__contains='03-24')|Q(birthdate__contains='03-25')
            |Q(birthdate__contains='03-26')|Q(birthdate__contains='03-27')|Q(birthdate__contains='03-28')|Q(birthdate__contains='03-29')|Q(birthdate__contains='03-30')|Q(birthdate__contains='03-31')
            |Q(birthdate__contains='04-01')|Q(birthdate__contains='04-02')|Q(birthdate__contains='04-03')|Q(birthdate__contains='04-04')|Q(birthdate__contains='04-05')|Q(birthdate__contains='04-06')
            |Q(birthdate__contains='04-07')|Q(birthdate__contains='04-08')|Q(birthdate__contains='04-09')|Q(birthdate__contains='04-10')|Q(birthdate__contains='04-11')|Q(birthdate__contains='04-12')
            |Q(birthdate__contains='04-13')|Q(birthdate__contains='04-14')|Q(birthdate__contains='04-15')|Q(birthdate__contains='04-16')|Q(birthdate__contains='04-17')|Q(birthdate__contains='04-18')
            |Q(birthdate__contains='04-19')|Q(birthdate__contains='04-20')).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
   




            Employment=employee.objects.all().filter(Q(EmploymentDate__contains='03-21')|Q(EmploymentDate__contains='03-22')|Q(EmploymentDate__contains='03-23')|Q(EmploymentDate__contains='03-24')|Q(EmploymentDate__contains='03-25')
            |Q(EmploymentDate__contains='03-26')|Q(EmploymentDate__contains='03-27')|Q(EmploymentDate__contains='03-28')|Q(EmploymentDate__contains='03-29')|Q(EmploymentDate__contains='03-30')|Q(EmploymentDate__contains='03-31')
            |Q(EmploymentDate__contains='04-01')|Q(EmploymentDate__contains='04-02')|Q(EmploymentDate__contains='04-03')|Q(EmploymentDate__contains='04-04')|Q(EmploymentDate__contains='04-05')|Q(EmploymentDate__contains='04-06')
            |Q(EmploymentDate__contains='04-07')|Q(EmploymentDate__contains='04-08')|Q(EmploymentDate__contains='04-09')|Q(EmploymentDate__contains='04-10')|Q(EmploymentDate__contains='04-11')|Q(EmploymentDate__contains='04-12')
            |Q(EmploymentDate__contains='04-13')|Q(EmploymentDate__contains='04-14')|Q(EmploymentDate__contains='04-15')|Q(EmploymentDate__contains='04-16')|Q(EmploymentDate__contains='04-17')|Q(EmploymentDate__contains='04-18')
            |Q(EmploymentDate__contains='04-19')|Q(EmploymentDate__contains='04-20')).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['EmploymentDate_month','EmploymentDate_day'])
            print(start_farvardin)
            print(end_farvardin)
            print(Employment)
            
            return render(request,'birth.html',{"allbirth":allbirth,"Employment":Employment})
        elif empbirth =='اردیبهشت':
            start=jdatetime.date(1370,2,1).togregorian()
            end=jdatetime.date(1370,2,31).togregorian()
            allbirth=employee.objects.all().filter(Q(birthdate__contains='04-21')|Q(birthdate__contains='04-22')|Q(birthdate__contains='04-23')|Q(birthdate__contains='04-24')|Q(birthdate__contains='04-25')
            |Q(birthdate__contains='04-26')|Q(birthdate__contains='04-27')|Q(birthdate__contains='04-28')|Q(birthdate__contains='04-29')|Q(birthdate__contains='04-30')|Q(birthdate__contains='05-01')|Q(birthdate__contains='05-02')
            |Q(birthdate__contains='05-03')|Q(birthdate__contains='05-04')|Q(birthdate__contains='05-05')|Q(birthdate__contains='05-06')|Q(birthdate__contains='05-07')|Q(birthdate__contains='05-08')|Q(birthdate__contains='05-09')
            |Q(birthdate__contains='05-10')|Q(birthdate__contains='05-11')|Q(birthdate__contains='05-12')|Q(birthdate__contains='05-13')|Q(birthdate__contains='05-14')|Q(birthdate__contains='05-15')
            |Q(birthdate__contains='05-16')|Q(birthdate__contains='05-17')|Q(birthdate__contains='05-18')|Q(birthdate__contains='05-19')|Q(birthdate__contains='05-20')|Q(birthdate__contains='05-21')).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])


            Employment=employee.objects.all().filter(Q(EmploymentDate__contains='04-21')|Q(EmploymentDate__contains='04-22')|Q(EmploymentDate__contains='04-23')|Q(EmploymentDate__contains='04-24')|Q(EmploymentDate__contains='04-25')
            |Q(EmploymentDate__contains='04-26')|Q(EmploymentDate__contains='04-27')|Q(EmploymentDate__contains='04-28')|Q(EmploymentDate__contains='04-29')|Q(EmploymentDate__contains='04-30')|Q(EmploymentDate__contains='05-01')|Q(EmploymentDate__contains='05-02')
            |Q(EmploymentDate__contains='05-03')|Q(EmploymentDate__contains='05-04')|Q(EmploymentDate__contains='05-05')|Q(EmploymentDate__contains='05-06')|Q(EmploymentDate__contains='05-07')|Q(EmploymentDate__contains='05-08')|Q(EmploymentDate__contains='05-09')
            |Q(EmploymentDate__contains='05-10')|Q(EmploymentDate__contains='05-11')|Q(EmploymentDate__contains='05-12')|Q(EmploymentDate__contains='05-13')|Q(EmploymentDate__contains='05-14')|Q(EmploymentDate__contains='05-15')
            |Q(EmploymentDate__contains='05-16')|Q(EmploymentDate__contains='05-17')|Q(EmploymentDate__contains='05-18')|Q(EmploymentDate__contains='05-19')|Q(EmploymentDate__contains='05-20')).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['EmploymentDate_month','EmploymentDate_day'])
            print(start)
            print(end)
            
            return render(request,'birth.html',{"allbirth":allbirth,"Employment":Employment})
        elif empbirth =='خرداد':
            start=jdatetime.date(1370,3,1).togregorian()
            end=jdatetime.date(1370,3,31).togregorian()
            allbirth=employee.objects.all().filter(Q(birthdate__contains='05-22')|Q(birthdate__contains='05-23')|Q(birthdate__contains='05-24')|Q(birthdate__contains='05-25')
            |Q(birthdate__contains='05-26')|Q(birthdate__contains='05-27')|Q(birthdate__contains='05-28')|Q(birthdate__contains='05-29')|Q(birthdate__contains='05-30')|Q(birthdate__contains='05-31')
            |Q(birthdate__contains='06-01')|Q(birthdate__contains='06-02')|Q(birthdate__contains='06-03')|Q(birthdate__contains='06-04')|Q(birthdate__contains='06-05')|Q(birthdate__contains='06-06')
            |Q(birthdate__contains='06-07')|Q(birthdate__contains='06-08')|Q(birthdate__contains='06-09')|Q(birthdate__contains='06-10')|Q(birthdate__contains='06-11')|Q(birthdate__contains='06-12')
            |Q(birthdate__contains='06-13')|Q(birthdate__contains='06-14')|Q(birthdate__contains='06-15')|Q(birthdate__contains='06-16')|Q(birthdate__contains='06-17')|Q(birthdate__contains='06-18')
            |Q(birthdate__contains='06-19')|Q(birthdate__contains='06-20')|Q(birthdate__contains='06-21')).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])


            Employment=employee.objects.all().filter(Q(EmploymentDate__contains='05-21')|Q(EmploymentDate__contains='05-22')|Q(EmploymentDate__contains='05-23')|Q(EmploymentDate__contains='05-24')|Q(EmploymentDate__contains='05-25')
            |Q(EmploymentDate__contains='05-26')|Q(EmploymentDate__contains='05-27')|Q(EmploymentDate__contains='05-28')|Q(EmploymentDate__contains='05-29')|Q(EmploymentDate__contains='05-30')|Q(EmploymentDate__contains='05-31')
            |Q(EmploymentDate__contains='06-01')|Q(EmploymentDate__contains='06-02')|Q(EmploymentDate__contains='06-03')|Q(EmploymentDate__contains='06-04')|Q(EmploymentDate__contains='06-05')|Q(EmploymentDate__contains='06-06')
            |Q(EmploymentDate__contains='06-07')|Q(EmploymentDate__contains='06-08')|Q(EmploymentDate__contains='06-09')|Q(EmploymentDate__contains='06-10')|Q(EmploymentDate__contains='06-11')|Q(EmploymentDate__contains='06-12')
            |Q(EmploymentDate__contains='06-13')|Q(EmploymentDate__contains='06-14')|Q(EmploymentDate__contains='06-15')|Q(EmploymentDate__contains='06-16')|Q(EmploymentDate__contains='06-17')|Q(EmploymentDate__contains='06-18')
            |Q(EmploymentDate__contains='06-19')|Q(EmploymentDate__contains='06-20')|Q(EmploymentDate__contains='06-21')).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['EmploymentDate_month','EmploymentDate_day'])
            print(start)
            print(end)
            
            return render(request,'birth.html',{"allbirth":allbirth,"Employment":Employment})
        elif empbirth =='تیر':
            start=jdatetime.date(1370,4,1).togregorian()
            end=jdatetime.date(1370,4,31).togregorian()
            allbirth=employee.objects.all().filter(Q(birthdate__contains='06-22')|Q(birthdate__contains='06-23')|Q(birthdate__contains='06-24')|Q(birthdate__contains='06-25')
            |Q(birthdate__contains='06-26')|Q(birthdate__contains='06-27')|Q(birthdate__contains='06-28')|Q(birthdate__contains='06-29')|Q(birthdate__contains='06-30')|Q(birthdate__contains='07-01')|Q(birthdate__contains='07-02')
            |Q(birthdate__contains='07-03')|Q(birthdate__contains='07-04')|Q(birthdate__contains='07-05')|Q(birthdate__contains='07-06')|Q(birthdate__contains='07-07')|Q(birthdate__contains='07-08')|Q(birthdate__contains='07-09')
            |Q(birthdate__contains='07-10')|Q(birthdate__contains='07-11')|Q(birthdate__contains='07-12')|Q(birthdate__contains='07-13')|Q(birthdate__contains='07-14')|Q(birthdate__contains='07-15')
            |Q(birthdate__contains='07-16')|Q(birthdate__contains='07-17')|Q(birthdate__contains='07-18')|Q(birthdate__contains='07-19')|Q(birthdate__contains='07-20')|Q(birthdate__contains='07-21')).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
            
            
            
            Employment=employee.objects.all().filter(Q(EmploymentDate__contains='06-22')|Q(EmploymentDate__contains='06-23')|Q(EmploymentDate__contains='06-24')|Q(EmploymentDate__contains='06-25')
            |Q(EmploymentDate__contains='06-26')|Q(EmploymentDate__contains='06-27')|Q(EmploymentDate__contains='06-28')|Q(EmploymentDate__contains='06-29')|Q(EmploymentDate__contains='06-30')|Q(EmploymentDate__contains='07-01')|Q(EmploymentDate__contains='07-02')
            |Q(EmploymentDate__contains='07-03')|Q(EmploymentDate__contains='07-04')|Q(EmploymentDate__contains='07-05')|Q(EmploymentDate__contains='07-06')|Q(EmploymentDate__contains='07-07')|Q(EmploymentDate__contains='07-08')|Q(EmploymentDate__contains='07-09')
            |Q(EmploymentDate__contains='07-10')|Q(EmploymentDate__contains='07-11')|Q(EmploymentDate__contains='07-12')|Q(EmploymentDate__contains='07-13')|Q(EmploymentDate__contains='07-14')|Q(EmploymentDate__contains='07-15')
            |Q(EmploymentDate__contains='07-16')|Q(EmploymentDate__contains='07-17')|Q(EmploymentDate__contains='07-18')|Q(EmploymentDate__contains='07-19')|Q(EmploymentDate__contains='07-20')|Q(EmploymentDate__contains='07-21')).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['EmploymentDate_month','EmploymentDate_day'])
            print(start)
            print(end)
            
            return render(request,'birth.html',{"allbirth":allbirth,"Employment":Employment})
        elif empbirth =='مرداد':
            start=jdatetime.date(1370,5,1).togregorian()
            end=jdatetime.date(1370,5,31).togregorian()
            allbirth=employee.objects.all().filter(Q(birthdate__contains='07-22')|Q(birthdate__contains='07-23')|Q(birthdate__contains='07-24')|Q(birthdate__contains='07-25')
            |Q(birthdate__contains='07-26')|Q(birthdate__contains='07-27')|Q(birthdate__contains='07-28')|Q(birthdate__contains='07-29')|Q(birthdate__contains='07-30')|Q(birthdate__contains='07-31')|Q(birthdate__contains='08-01')|Q(birthdate__contains='08-02')
            |Q(birthdate__contains='08-03')|Q(birthdate__contains='08-04')|Q(birthdate__contains='08-05')|Q(birthdate__contains='08-06')|Q(birthdate__contains='08-07')|Q(birthdate__contains='08-08')|Q(birthdate__contains='08-09')
            |Q(birthdate__contains='08-10')|Q(birthdate__contains='08-11')|Q(birthdate__contains='08-12')|Q(birthdate__contains='08-13')|Q(birthdate__contains='08-14')|Q(birthdate__contains='08-15')
            |Q(birthdate__contains='08-16')|Q(birthdate__contains='08-17')|Q(birthdate__contains='08-18')|Q(birthdate__contains='08-19')|Q(birthdate__contains='08-20')|Q(birthdate__contains='08-21')|Q(birthdate__contains='08-22')).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
            
            
            Employment=employee.objects.all().filter(Q(EmploymentDate__contains='07-22')|Q(EmploymentDate__contains='07-23')|Q(EmploymentDate__contains='07-24')|Q(EmploymentDate__contains='07-25')
            |Q(EmploymentDate__contains='07-26')|Q(EmploymentDate__contains='07-27')|Q(EmploymentDate__contains='07-28')|Q(EmploymentDate__contains='07-29')|Q(EmploymentDate__contains='07-30')|Q(EmploymentDate__contains='07-31')|Q(EmploymentDate__contains='08-01')|Q(EmploymentDate__contains='08-02')
            |Q(EmploymentDate__contains='08-03')|Q(EmploymentDate__contains='08-04')|Q(EmploymentDate__contains='08-05')|Q(EmploymentDate__contains='08-06')|Q(EmploymentDate__contains='08-07')|Q(EmploymentDate__contains='08-08')|Q(EmploymentDate__contains='08-09')
            |Q(EmploymentDate__contains='08-10')|Q(EmploymentDate__contains='08-11')|Q(EmploymentDate__contains='08-12')|Q(EmploymentDate__contains='08-13')|Q(EmploymentDate__contains='08-14')|Q(EmploymentDate__contains='08-15')
            |Q(EmploymentDate__contains='08-16')|Q(EmploymentDate__contains='08-17')|Q(EmploymentDate__contains='08-18')|Q(EmploymentDate__contains='08-19')|Q(EmploymentDate__contains='08-20')|Q(EmploymentDate__contains='08-21')).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['EmploymentDate_month','EmploymentDate_day'])
            print(start)
            print(end)
         
            return render(request,'birth.html',{"allbirth":allbirth,"Employment":Employment})
        elif empbirth =='شهریور':
            start=jdatetime.date(1370,6,1).togregorian()
            end=jdatetime.date(1370,6,31).togregorian()
            allbirth=employee.objects.all().filter(Q(birthdate__contains='08-22')|Q(birthdate__contains='08-23')|Q(birthdate__contains='08-24')|Q(birthdate__contains='08-25')
            |Q(birthdate__contains='08-26')|Q(birthdate__contains='08-27')|Q(birthdate__contains='08-28')|Q(birthdate__contains='08-29')|Q(birthdate__contains='08-30')|Q(birthdate__contains='08-31')|Q(birthdate__contains='09-01')|Q(birthdate__contains='09-02')
            |Q(birthdate__contains='09-03')|Q(birthdate__contains='09-04')|Q(birthdate__contains='09-05')|Q(birthdate__contains='09-06')|Q(birthdate__contains='09-07')|Q(birthdate__contains='09-08')|Q(birthdate__contains='08-09')
            |Q(birthdate__contains='09-10')|Q(birthdate__contains='09-11')|Q(birthdate__contains='09-12')|Q(birthdate__contains='09-13')|Q(birthdate__contains='09-14')|Q(birthdate__contains='09-15')
            |Q(birthdate__contains='09-16')|Q(birthdate__contains='09-17')|Q(birthdate__contains='09-18')|Q(birthdate__contains='09-19')|Q(birthdate__contains='09-20')|Q(birthdate__contains='09-21')|Q(birthdate__contains='09-22')).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
            
            
            
            Employment=employee.objects.all().filter(Q(EmploymentDate__contains='08-23')|Q(EmploymentDate__contains='08-24')|Q(EmploymentDate__contains='08-25')
            |Q(EmploymentDate__contains='08-26')|Q(EmploymentDate__contains='08-27')|Q(EmploymentDate__contains='08-28')|Q(EmploymentDate__contains='08-29')|Q(EmploymentDate__contains='08-30')|Q(EmploymentDate__contains='08-31')|Q(EmploymentDate__contains='09-01')|Q(EmploymentDate__contains='09-02')
            |Q(EmploymentDate__contains='09-03')|Q(EmploymentDate__contains='09-04')|Q(EmploymentDate__contains='09-05')|Q(EmploymentDate__contains='09-06')|Q(EmploymentDate__contains='09-07')|Q(EmploymentDate__contains='09-08')|Q(EmploymentDate__contains='08-09')
            |Q(EmploymentDate__contains='09-10')|Q(EmploymentDate__contains='09-11')|Q(EmploymentDate__contains='09-12')|Q(EmploymentDate__contains='09-13')|Q(EmploymentDate__contains='09-14')|Q(EmploymentDate__contains='09-15')
            |Q(EmploymentDate__contains='09-16')|Q(EmploymentDate__contains='09-17')|Q(EmploymentDate__contains='09-18')|Q(EmploymentDate__contains='09-19')|Q(EmploymentDate__contains='09-20')|Q(EmploymentDate__contains='09-21')|Q(EmploymentDate__contains='09-22')).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['EmploymentDate_month','EmploymentDate_day'])
            print(start)
            print(end)
           
            return render(request,'birth.html',{"allbirth":allbirth,"Employment":Employment})
        elif empbirth =='مهر':
            start=jdatetime.date(1370,7,1).togregorian()
            end=jdatetime.date(1370,7,30).togregorian()
            allbirth=employee.objects.all().filter(Q(birthdate__contains='09-23')|Q(birthdate__contains='09-24')|Q(birthdate__contains='09-25')
            |Q(birthdate__contains='09-26')|Q(birthdate__contains='09-27')|Q(birthdate__contains='09-28')|Q(birthdate__contains='09-29')|Q(birthdate__contains='09-30')|Q(birthdate__contains='10-01')|Q(birthdate__contains='10-02')
            |Q(birthdate__contains='10-03')|Q(birthdate__contains='11-04')|Q(birthdate__contains='10-05')|Q(birthdate__contains='10-06')|Q(birthdate__contains='10-07')|Q(birthdate__contains='10-08')|Q(birthdate__contains='10-09')
            |Q(birthdate__contains='10-10')|Q(birthdate__contains='10-11')|Q(birthdate__contains='10-12')|Q(birthdate__contains='10-13')|Q(birthdate__contains='10-14')|Q(birthdate__contains='10-15')
            |Q(birthdate__contains='10-16')|Q(birthdate__contains='10-17')|Q(birthdate__contains='10-18')|Q(birthdate__contains='10-19')|Q(birthdate__contains='10-20')|Q(birthdate__contains='10-21')|Q(birthdate__contains='10-22')).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
            
            
            Employment=employee.objects.all().filter(Q(EmploymentDate__contains='09-23')|Q(EmploymentDate__contains='09-24')|Q(EmploymentDate__contains='09-25')
            |Q(EmploymentDate__contains='09-26')|Q(EmploymentDate__contains='09-27')|Q(EmploymentDate__contains='09-28')|Q(EmploymentDate__contains='09-29')|Q(EmploymentDate__contains='09-30')|Q(EmploymentDate__contains='10-01')|Q(EmploymentDate__contains='10-02')
            |Q(EmploymentDate__contains='10-03')|Q(EmploymentDate__contains='11-04')|Q(EmploymentDate__contains='10-05')|Q(EmploymentDate__contains='10-06')|Q(EmploymentDate__contains='10-07')|Q(EmploymentDate__contains='10-08')|Q(EmploymentDate__contains='10-09')
            |Q(EmploymentDate__contains='10-10')|Q(EmploymentDate__contains='10-11')|Q(EmploymentDate__contains='10-12')|Q(EmploymentDate__contains='10-13')|Q(EmploymentDate__contains='10-14')|Q(EmploymentDate__contains='10-15')
            |Q(EmploymentDate__contains='10-16')|Q(EmploymentDate__contains='10-17')|Q(EmploymentDate__contains='10-18')|Q(EmploymentDate__contains='10-19')|Q(EmploymentDate__contains='10-20')|Q(EmploymentDate__contains='10-21')|Q(EmploymentDate__contains='10-22')).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['EmploymentDate_month','EmploymentDate_day'])
            print(start)
            print(end)
          
            return render(request,'birth.html',{"allbirth":allbirth,"Employment":Employment})
        elif empbirth =='آبان':
            start=jdatetime.date(1370,8,1).togregorian()
            end=jdatetime.date(1370,8,30).togregorian()
            allbirth=employee.objects.all().filter(Q(birthdate__contains='10-23')|Q(birthdate__contains='10-24')|Q(birthdate__contains='10-25')
            |Q(birthdate__contains='10-26')|Q(birthdate__contains='10-27')|Q(birthdate__contains='10-28')|Q(birthdate__contains='10-29')|Q(birthdate__contains='10-30')|Q(birthdate__contains='10-31')|Q(birthdate__contains='11-01')|Q(birthdate__contains='11-02')
            |Q(birthdate__contains='11-03')|Q(birthdate__contains='11-04')|Q(birthdate__contains='11-05')|Q(birthdate__contains='11-06')|Q(birthdate__contains='11-07')|Q(birthdate__contains='11-08')|Q(birthdate__contains='11-09')
            |Q(birthdate__contains='11-10')|Q(birthdate__contains='11-11')|Q(birthdate__contains='11-12')|Q(birthdate__contains='11-13')|Q(birthdate__contains='11-14')|Q(birthdate__contains='11-15')
            |Q(birthdate__contains='11-16')|Q(birthdate__contains='11-17')|Q(birthdate__contains='11-18')|Q(birthdate__contains='11-19')|Q(birthdate__contains='11-20')|Q(birthdate__contains='11-21')).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
            
            
            Employment=employee.objects.all().filter(Q(EmploymentDate__contains='10-23')|Q(EmploymentDate__contains='10-24')|Q(EmploymentDate__contains='10-25')
            |Q(EmploymentDate__contains='10-26')|Q(EmploymentDate__contains='10-27')|Q(EmploymentDate__contains='10-28')|Q(EmploymentDate__contains='10-29')|Q(EmploymentDate__contains='10-30')|Q(EmploymentDate__contains='10-31')|Q(EmploymentDate__contains='11-01')|Q(EmploymentDate__contains='11-02')
            |Q(EmploymentDate__contains='11-03')|Q(EmploymentDate__contains='11-04')|Q(EmploymentDate__contains='11-05')|Q(EmploymentDate__contains='11-06')|Q(EmploymentDate__contains='11-07')|Q(EmploymentDate__contains='11-08')|Q(EmploymentDate__contains='11-09')
            |Q(EmploymentDate__contains='11-10')|Q(EmploymentDate__contains='11-11')|Q(EmploymentDate__contains='11-12')|Q(EmploymentDate__contains='11-13')|Q(EmploymentDate__contains='11-14')|Q(EmploymentDate__contains='11-15')
            |Q(EmploymentDate__contains='11-16')|Q(EmploymentDate__contains='11-17')|Q(EmploymentDate__contains='11-18')|Q(EmploymentDate__contains='11-19')|Q(EmploymentDate__contains='11-20')).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['EmploymentDate_month','EmploymentDate_day'])
            print(start)
            print(end)
           
            return render(request,'birth.html',{"allbirth":allbirth,"Employment":Employment})
        elif empbirth =='آذر':
            start=jdatetime.date(1370,9,1).togregorian()
            end=jdatetime.date(1370,9,30).togregorian()
            allbirth=employee.objects.all().filter(Q(birthdate__contains='11-22')|Q(birthdate__contains='11-23')|Q(birthdate__contains='11-24')|Q(birthdate__contains='11-25')
            |Q(birthdate__contains='11-26')|Q(birthdate__contains='11-27')|Q(birthdate__contains='11-28')|Q(birthdate__contains='11-29')|Q(birthdate__contains='11-30')|Q(birthdate__contains='12-01')|Q(birthdate__contains='12-02')
            |Q(birthdate__contains='12-03')|Q(birthdate__contains='12-04')|Q(birthdate__contains='12-05')|Q(birthdate__contains='12-06')|Q(birthdate__contains='12-07')|Q(birthdate__contains='12-08')|Q(birthdate__contains='12-09')
            |Q(birthdate__contains='12-10')|Q(birthdate__contains='12-11')|Q(birthdate__contains='12-12')|Q(birthdate__contains='12-13')|Q(birthdate__contains='12-14')|Q(birthdate__contains='12-15')
            |Q(birthdate__contains='12-16')|Q(birthdate__contains='12-17')|Q(birthdate__contains='12-18')|Q(birthdate__contains='12-19')|Q(birthdate__contains='12-20')|Q(birthdate__contains='12-21')).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
            
            
            Employment=employee.objects.all().filter(Q(EmploymentDate__contains='11-21')|Q(EmploymentDate__contains='11-22')|Q(EmploymentDate__contains='11-23')|Q(EmploymentDate__contains='11-24')|Q(EmploymentDate__contains='11-25')
            |Q(EmploymentDate__contains='11-26')|Q(EmploymentDate__contains='11-27')|Q(EmploymentDate__contains='11-28')|Q(EmploymentDate__contains='11-29')|Q(EmploymentDate__contains='11-30')|Q(EmploymentDate__contains='12-01')|Q(EmploymentDate__contains='12-02')
            |Q(EmploymentDate__contains='12-03')|Q(EmploymentDate__contains='12-04')|Q(EmploymentDate__contains='12-05')|Q(EmploymentDate__contains='12-06')|Q(EmploymentDate__contains='12-07')|Q(EmploymentDate__contains='12-08')|Q(EmploymentDate__contains='12-09')
            |Q(EmploymentDate__contains='12-10')|Q(EmploymentDate__contains='12-11')|Q(EmploymentDate__contains='12-12')|Q(EmploymentDate__contains='12-13')|Q(EmploymentDate__contains='12-14')|Q(EmploymentDate__contains='12-15')
            |Q(EmploymentDate__contains='12-16')|Q(EmploymentDate__contains='12-17')|Q(EmploymentDate__contains='12-18')|Q(EmploymentDate__contains='12-19')|Q(EmploymentDate__contains='12-20')).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['EmploymentDate_month','EmploymentDate_day'])
            print(start)
            print(end)
           
            return render(request,'birth.html',{"allbirth":allbirth,"Employment":Employment})
        elif empbirth =='دی':
            start=jdatetime.date(1370,10,1).togregorian()
            end=jdatetime.date(1370,10,30).togregorian()
            allbirth=employee.objects.all().filter(Q(birthdate__contains='12-22')|Q(birthdate__contains='12-23')|Q(birthdate__contains='12-24')|Q(birthdate__contains='12-25')
            |Q(birthdate__contains='12-26')|Q(birthdate__contains='12-27')|Q(birthdate__contains='12-28')|Q(birthdate__contains='12-29')|Q(birthdate__contains='12-30')|Q(birthdate__contains='12-31')|Q(birthdate__contains='01-01')|Q(birthdate__contains='01-02')
            |Q(birthdate__contains='01-03')|Q(birthdate__contains='01-04')|Q(birthdate__contains='01-05')|Q(birthdate__contains='01-06')|Q(birthdate__contains='01-07')|Q(birthdate__contains='01-08')|Q(birthdate__contains='01-09')
            |Q(birthdate__contains='01-10')|Q(birthdate__contains='01-11')|Q(birthdate__contains='01-12')|Q(birthdate__contains='01-13')|Q(birthdate__contains='01-14')|Q(birthdate__contains='01-15')
            |Q(birthdate__contains='01-16')|Q(birthdate__contains='01-17')|Q(birthdate__contains='01-18')|Q(birthdate__contains='01-19')|Q(birthdate__contains='01-20')).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
            
            
            Employment=employee.objects.all().filter(Q(EmploymentDate__contains='12-21')|Q(EmploymentDate__contains='12-22')|Q(EmploymentDate__contains='12-23')|Q(EmploymentDate__contains='12-24')|Q(EmploymentDate__contains='12-25')
            |Q(EmploymentDate__contains='12-26')|Q(EmploymentDate__contains='12-27')|Q(EmploymentDate__contains='12-28')|Q(EmploymentDate__contains='12-29')|Q(EmploymentDate__contains='12-30')|Q(EmploymentDate__contains='12-31')|Q(EmploymentDate__contains='01-01')|Q(EmploymentDate__contains='01-02')
            |Q(EmploymentDate__contains='01-03')|Q(EmploymentDate__contains='01-04')|Q(EmploymentDate__contains='01-05')|Q(EmploymentDate__contains='01-06')|Q(EmploymentDate__contains='01-07')|Q(EmploymentDate__contains='01-08')|Q(EmploymentDate__contains='01-09')
            |Q(EmploymentDate__contains='01-10')|Q(EmploymentDate__contains='01-11')|Q(EmploymentDate__contains='01-12')|Q(EmploymentDate__contains='01-13')|Q(EmploymentDate__contains='01-14')|Q(EmploymentDate__contains='01-15')
            |Q(EmploymentDate__contains='01-16')|Q(EmploymentDate__contains='01-17')|Q(EmploymentDate__contains='01-18')|Q(EmploymentDate__contains='01-19')).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['-EmploymentDate_month','EmploymentDate_day'])
            print(start)
            print(end)
            
            return render(request,'birth.html',{"allbirth":allbirth,"Employment":Employment})
        elif empbirth =='بهمن':
            start=jdatetime.date(1370,11,1).togregorian()
            end=jdatetime.date(1370,11,30).togregorian()
            allbirth=employee.objects.all().filter(Q(birthdate__contains='01-20')|Q(birthdate__contains='01-21')|Q(birthdate__contains='01-22')|Q(birthdate__contains='01-23')|Q(birthdate__contains='01-24')|Q(birthdate__contains='01-25')
            |Q(birthdate__contains='01-26')|Q(birthdate__contains='01-27')|Q(birthdate__contains='01-28')|Q(birthdate__contains='01-29')|Q(birthdate__contains='01-30')|Q(birthdate__contains='01-31')|Q(birthdate__contains='02-01')|Q(birthdate__contains='02-02')
            |Q(birthdate__contains='02-03')|Q(birthdate__contains='02-04')|Q(birthdate__contains='02-05')|Q(birthdate__contains='02-06')|Q(birthdate__contains='02-07')|Q(birthdate__contains='02-08')|Q(birthdate__contains='02-09')
            |Q(birthdate__contains='02-10')|Q(birthdate__contains='02-11')|Q(birthdate__contains='02-12')|Q(birthdate__contains='02-13')|Q(birthdate__contains='02-14')|Q(birthdate__contains='02-15')
            |Q(birthdate__contains='02-16')|Q(birthdate__contains='02-17')|Q(birthdate__contains='02-18')|Q(birthdate__contains='02-19')).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
            
            
            Employment=employee.objects.all().filter(Q(EmploymentDate__contains='01-21')|Q(EmploymentDate__contains='01-22')|Q(EmploymentDate__contains='01-23')|Q(EmploymentDate__contains='01-24')|Q(EmploymentDate__contains='01-25')
            |Q(EmploymentDate__contains='01-26')|Q(EmploymentDate__contains='01-27')|Q(EmploymentDate__contains='01-28')|Q(EmploymentDate__contains='01-29')|Q(EmploymentDate__contains='01-30')|Q(EmploymentDate__contains='01-31')|Q(EmploymentDate__contains='02-01')|Q(EmploymentDate__contains='02-02')
            |Q(EmploymentDate__contains='02-03')|Q(EmploymentDate__contains='02-04')|Q(EmploymentDate__contains='02-05')|Q(EmploymentDate__contains='02-06')|Q(EmploymentDate__contains='02-07')|Q(EmploymentDate__contains='02-08')|Q(EmploymentDate__contains='02-09')
            |Q(EmploymentDate__contains='02-10')|Q(EmploymentDate__contains='02-11')|Q(EmploymentDate__contains='02-12')|Q(EmploymentDate__contains='02-13')|Q(EmploymentDate__contains='02-14')|Q(EmploymentDate__contains='02-15')
            |Q(EmploymentDate__contains='02-16')|Q(EmploymentDate__contains='02-17')|Q(EmploymentDate__contains='02-18')|Q(EmploymentDate__contains='02-19')).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['EmploymentDate_month','EmploymentDate_day'])
            print(start)
            print(end)
           
            return render(request,'birth.html',{"allbirth":allbirth,"Employment":Employment})
        elif empbirth =='اسفند':
            start=jdatetime.date(1370,12,1).togregorian()
            end=jdatetime.date(1370,12,30).togregorian()
            allbirth=employee.objects.all().filter(Q(birthdate__contains='02-20')|Q(birthdate__contains='02-21')|Q(birthdate__contains='02-22')|Q(birthdate__contains='02-23')|Q(birthdate__contains='02-24')|Q(birthdate__contains='02-25')
            |Q(birthdate__contains='02-26')|Q(birthdate__contains='02-27')|Q(birthdate__contains='02-28')|Q(birthdate__contains='02-29')|Q(birthdate__contains='02-30')|Q(birthdate__contains='02-31')|Q(birthdate__contains='03-01')|Q(birthdate__contains='03-02')
            |Q(birthdate__contains='03-03')|Q(birthdate__contains='03-04')|Q(birthdate__contains='03-05')|Q(birthdate__contains='03-06')|Q(birthdate__contains='03-07')|Q(birthdate__contains='02-08')|Q(birthdate__contains='02-09')
            |Q(birthdate__contains='03-10')|Q(birthdate__contains='03-11')|Q(birthdate__contains='03-12')|Q(birthdate__contains='03-13')|Q(birthdate__contains='03-14')|Q(birthdate__contains='02-15')
            |Q(birthdate__contains='03-16')|Q(birthdate__contains='03-17')|Q(birthdate__contains='03-18')|Q(birthdate__contains='03-19')|Q(birthdate__contains='03-20')).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
            
            
            Employment=employee.objects.all().filter(Q(EmploymentDate__contains='02-20')|Q(EmploymentDate__contains='02-21')|Q(EmploymentDate__contains='02-22')|Q(EmploymentDate__contains='02-23')|Q(EmploymentDate__contains='02-24')|Q(EmploymentDate__contains='02-25')
            |Q(EmploymentDate__contains='02-26')|Q(EmploymentDate__contains='02-27')|Q(EmploymentDate__contains='02-28')|Q(EmploymentDate__contains='02-29')|Q(EmploymentDate__contains='02-30')|Q(EmploymentDate__contains='02-31')|Q(EmploymentDate__contains='03-01')|Q(EmploymentDate__contains='03-02')
            |Q(EmploymentDate__contains='03-03')|Q(EmploymentDate__contains='03-04')|Q(EmploymentDate__contains='03-05')|Q(EmploymentDate__contains='03-06')|Q(EmploymentDate__contains='03-07')|Q(EmploymentDate__contains='02-08')|Q(EmploymentDate__contains='02-09')
            |Q(EmploymentDate__contains='03-10')|Q(EmploymentDate__contains='03-11')|Q(EmploymentDate__contains='03-12')|Q(EmploymentDate__contains='03-13')|Q(EmploymentDate__contains='03-14')|Q(EmploymentDate__contains='02-15')
            |Q(EmploymentDate__contains='03-16')|Q(EmploymentDate__contains='03-17')|Q(EmploymentDate__contains='03-18')|Q(EmploymentDate__contains='03-19')|Q(EmploymentDate__contains='03-20')).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['EmploymentDate_month','EmploymentDate_day'])
            print(start)
            print(end)
            
            return render(request,'birth.html',{"allbirth":allbirth,"Employment":Employment})
        elif empbirth == ' ':
            allbirth=employee.objects.all()
            Employment=employee.objects.all()
            return render(request,'birth.html',{"allbirth":allbirth,"Employment":Employment})

            
      

        
          
    print(today)
        

   
    return render(request,'birth.html',{"allbirth":allbirth,"Employment":Employment})


def choosepath(request):
    if request.user.is_authenticated and request.user.has_perm('lotus_cooperators.is_manager') :
        return render(request,'choosepath.html')
    else:
        return redirect('/event/birthday/')

# def sms(request):
#     today=date.today()
         
#     dt = datetime.today().strftime('%A')     
#     week=(today+timedelta(days=7))
#     if dt =='saturday':
        

#         allbirth=employee.objects.all().filter(birthdate__month__range=[today.month,week.month],birthdate__day__range=[today.day,week.day]).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
#         Employment=employee.objects.all().filter(EmploymentDate__month__range=[today.month,week.month],EmploymentDate__day__range=[today.day,week.day]).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['-EmploymentDate_month','EmploymentDate_day'])
#     print(dt)
    
#     return HttpResponse('helooooo')
 




def test(request):

    
 
    
    sdate=date.today()
    edate = sdate+timedelta(days=7)   # end date

    delta = edate - sdate       # as timedelta

    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        print(day)


    alltest=employee.objects.all().filter(birthdate__month__contains=day.month).filter(birthdate__day__contains=day.day)
    alltest1=employee.objects.all().filter(birthdate__contains='1400')
    print(alltest)
    print(alltest1)
    print([sdate.month,edate.month])
    print([sdate.day,edate.day])

 
    return render(request,'testev.html')


from rest_framework.decorators import api_view
import requests
import re

def validate_mobile(value):
    if len(value) != 11:
        return False
    rule = re.compile(r'^(?:\+?44)?[07]\d{9,13}$')
    return rule.search(value)

from requests import Session
from requests.auth import HTTPBasicAuth # or HTTPDigestAuth, or OAuth1, etc.
from zeep import Client, wsdl
from zeep.transports import Transport
import requests




def send_sms(mobile):
        
    # credentials
    username = "lotusco"
    password = "ZIkEPhzvVDiJUKpc"
    domain = "magfa"

    # session
   
    session = Session()
    # basic auth
    session.auth =(username, password)

    # # soap
   
    url = 'https://sms.magfa.com/api/soap/sms/v1/server?wsdl'
    client = Client(wsdl=url, transport=Transport(session=session))


    
    # # data
    stringArray = client.get_type('ns1:ArrayOf_xsd_string');
    longArray = client.get_type('ns1:ArrayOf_xsd_long');
    intArray = client.get_type('ns1:ArrayOf_xsd_int');

    # data
    plain_string = "سلام.در این چند روز تاریخ تولد یا استخدام وجود دارد.لطفا پنل خود را بررسی نمائید."
    unicode_string = "تست ارسال پيامک. Sample Text for test."
    
    
    
    # # call

    resp=client.service.enqueue(
    domain=domain,
    messageBodies=stringArray([ plain_string]),
    recipientNumbers=stringArray([str(mobile)]),
    senderNumbers=stringArray(["300008656"]),
    encodings=stringArray([0]),
    udhs=stringArray([""]),
    messageClasses=intArray([1]),
    priorities=intArray([0]),
    checkingMessageIds=longArray([200,201]),
        
    );

    print(resp)
    requests.get(url, verify=False)
    return (resp,VerifiedHTTPSConnection==False)

    
    #resp=requests.get('resp1',timeout=None,auth=None,verify=False)
   
   
from rest_framework.response import Response
from datetime import date, datetime,timedelta


from rest_framework import status
@login_required(login_url='/event/login/')
@api_view(['GET'])
def mobile(request,format=None):
    if request.method=='GET':
    
        mobile = request.GET.get('mobile', '-')
        period = request.GET.get('period', 0)
    if validate_mobile(mobile):
        today=date.today()
        days=(today+timedelta(days=int(period)))
        next_month = datetime(year=today.year, month=today.month+1, day=1)
        last_day_month = next_month - timedelta(days=1)
       
        days=(today+timedelta(days=int(period)))

        daylist=(int(period))-(last_day_month.day - today.day)
        if (last_day_month.day - today.day) < (int(period)):

            allbirth1=employee.objects.all().filter(birthdate__month=today.month ,birthdate__day__range=[today.day,last_day_month.day]
            ).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
            allbirth2=employee.objects.all().filter(birthdate__month=days.month ,birthdate__day__range=[1,daylist]
            ).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
            allbirth=list(chain(allbirth1,allbirth2))

            Employment1=employee.objects.all().filter(EmploymentDate__month=today.month ,EmploymentDate__day__range=[today.day,last_day_month.day]
            ).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['EmploymentDate_month','EmploymentDate_day'])
            Employment2=employee.objects.all().filter(EmploymentDate__month=days.month ,EmploymentDate__day__range=[1,daylist]
            ).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['EmploymentDate_month','EmploymentDate_day'])
            Employment=list(chain(Employment1,Employment2))
        else:
            

            allbirth=employee.objects.all().filter(birthdate__month__range=[today.month,days.month],birthdate__day__range=[today.day,days.day]).extra(select={ 'birth_date_month': 'MONTH(birthdate)','birth_date_day': 'DAY(birthdate)' },order_by=['birth_date_month','birth_date_day'])
            Employment=employee.objects.all().filter(EmploymentDate__month__range=[today.month,days.month],EmploymentDate__day__range=[today.day,days.day]).extra(select={ 'EmploymentDate_month': 'MONTH(EmploymentDate)','EmploymentDate_day': 'DAY(EmploymentDate)' },order_by=['-EmploymentDate_month','EmploymentDate_day'])
            print(allbirth)
            print(today)
            print(last_day_month)
            print(days)


            
        if allbirth :

            resp =send_sms(mobile)
            
        elif Employment:
            resp =send_sms(mobile)
        else:
            return HttpResponse('هیچ تاریخ تولد یا استخدامی در تاریخ ذکر شده وجود ندارد')

        print(resp)
        if resp:
            content = {'message': 'sms did sent',

                        'period': period}
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {'message': 'sms did not sent!!!'}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        content = {'message': 'please enter mobile'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)




def testev(request):

    allbirth=employee.objects.all()
    Employment=employee.objects.all()
    return render(request,'testev.html',{"allbirth":allbirth,"Employment":Employment})

   
 






    
    

