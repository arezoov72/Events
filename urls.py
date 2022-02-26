from django.urls import path,include
from . import views
from django.contrib import auth
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView,LogoutView



app_name='Events'
urlpatterns = [

#path('',views.home,name='home'),
path('',views.event_page,name='event_page'),
path('test/',views.testev,name='testen'),

path('adminp/',views.adminpanel,name='admin'),
path('birthday/',views.birthdayreminder,name='birthday'),
path('testmobile/',views.testmobile,name='testmobile'),
path('sms/',views.mobile,name='sms'),
path('choosepath/',views.choosepath,name='choosepath'),
path('login/',LoginView.as_view(template_name='registration/event_login.html'),name='login_event' ),
path('logout/',LogoutView.as_view(template_name='registration/event_logout.html'),name='logout_event' ),
#path('event/', auth_views.LoginView.as_view(), {'template_name': 'registration/login.html'}, name = 'login'),

#authentication,login,pass and reser pass
#path('event/', include('django.contrib.auth.urls')),

 


]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


