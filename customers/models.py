from django.db import models
import django_filters
from django.contrib.auth.models import User

class Customer(models.Model):
  user = models.OneToOneField(User)  
  name = models.CharField(max_length = 255, blank=True, null=True)
  phone = models.CharField(max_length = 50, blank=True, null=True)
  movil = models.CharField(max_length = 50, blank=True, null=True)
  email = models.CharField(max_length = 255)
  #pagos
  #soporte
  def __unicode__(self):
    return unicode(self.user)


from django.http import HttpResponse, HttpResponseRedirect
def CustomerExist(request, user):
  print 'entro funcion customer'
  try:
    customer= Customer.objects.get(user = user)
    return False
  except:
    return True





#class ProyectFilter(django_filters.FilterSet):
    #class Meta:
        #model = Proyect
        #fields = {'progress': ['lt', 'gt'],
        		  #'pub_date': ['lt', 'gt'],
        		  #'mount': ['lt', 'gt'], 
        		  #'remaingpayment': ['lt', 'gt'], 
        		  #'type1': ['exact'],
        		  #'status':['exact'],
        		 # }