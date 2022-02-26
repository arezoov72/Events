from os import path
from django.db import models
from django.contrib.auth.models import User
import datetime
from django_jalali.db import models as jmodels






# Create your models here.


class Event(models.Model):
    objects = jmodels.jManager()
    id=models.AutoField(primary_key=True)
    username=models.ForeignKey(User,on_delete=models.CASCADE,max_length=30,null=True,to_field='username')
    title=models.CharField(max_length=500)
    picture=models.ImageField(upload_to='upload/',blank=True,null=True)
    event=models.TextField(null=True)
    information=models.TextField(null=True)
    date=jmodels.jDateField(null=True)
    tousers=models.ForeignKey(User,on_delete=models.CASCADE,max_length=30,null=True,related_name='tousers2',to_field='username',db_column='tousers')





    
   
 
    



