from django.db import models
from customers.models import Customer
from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
import datetime


class Type(models.Model):
  name = models.CharField(max_length=255)
  def __unicode__(self):
    return self.name

class Status(models.Model):
  name = models.CharField(max_length=255)
  def __unicode__(self):
    return self.name

class Package(models.Model):
  name = models.CharField(max_length = 255)
  description = models.CharField(max_length = 255)
  totalprice = models.FloatField(blank=True, null=True)
  featureds = models.ManyToManyField('Featured')
  #services
  #def save(self, *args, **kwargs):
      #self.totalprice = 10
      #featuredins = self.featureds
      #print featuredins
      #print "guardado"
      #super(Package, self).save(*args, **kwargs)

  def __unicode__(self):
    return self.name


class Proyect(models.Model):
  name = models.CharField(max_length = 255)
  description = models.CharField(max_length = 140)
  user = models.ForeignKey('customers.Customer', to_field='user') #se vincula la relacion hacia el campo que apunta al user_id de customer y a su vez de User ya que de otra forma se revuelven las consultas
  #feature = models.ForeignKey('features.Featured')
  #customer = models.ForeignKey('customers.Customer')
  #developer = models.ForeignKey('developers.Developer')
  #content = models.ForeignKey('contents.Content')
  progress = models.PositiveIntegerField()
  mount = models.FloatField()
  advancepayment = models.FloatField()
  remaingpayment = models.FloatField()
  #type1 = models.ForeignKey(Type)
  package = models.ForeignKey(Package)
  status = models.ForeignKey(Status)
  pub_date = models.DateTimeField(default=datetime.datetime.now)
  def __unicode__(self):
    return self.name


class Featured(models.Model):
  name = models.CharField(max_length = 255)
  description = models.CharField(max_length = 255)
  price = models.FloatField()
  #alternative 
  proyect = models.ForeignKey(Proyect, blank=True, null=True)
  #proyect = models.ForeignKey('proyects.Proyect')
  def __unicode__(self):
    return self.name


def post_save_mymodel(sender, instance, *args, **kwargs):

    currentinstanceid = instance.id
    currentinstance = Package.objects.get(id=currentinstanceid)
    featuredins = currentinstance.featureds.all()
    print currentinstance.featureds.all()
    total = 0

    for featured in currentinstance.featureds.all():
      price = featured.price
      total = total + price
      print total
    totalinstance = Package.objects.get(id=currentinstanceid)
    totalinstance.totalprice=total
    totalinstance.save()
     #if action == 'post_add' and not reverse:
        #for e in instance.my_m2mfield.all():
            # Query including "e""" #Modificar deacuerdo a las acciones
m2m_changed.connect(post_save_mymodel, sender=Package.featureds.through)








