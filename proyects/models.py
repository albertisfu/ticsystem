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
  progress = models.PositiveIntegerField(blank=True, null=True)
  mount = models.FloatField(blank=True, null=True)
  advancepayment = models.FloatField(blank=True, null=True)
  remaingpayment = models.FloatField(blank=True, null=True)
  #type1 = models.ForeignKey(Type)
  package = models.ForeignKey(Package)
  #status = models.ForeignKey(Status)
  pendiente = 1
  proceso = 2
  terminado = 3
  cancelado = 4
  status_options = (
    (pendiente, 'Pendiente'),
    (proceso, 'Proceso'),
    (terminado, 'Terminado'),
    (cancelado, 'Cancelado'),
  )
  status = models.IntegerField(choices=status_options, default=pendiente)
  pub_date = models.DateTimeField(auto_now_add=True)
  def __unicode__(self):
    return self.name
#al guardar el modelo se tiene que agregar 0 en los campos mount, advance y remain

class Featured(models.Model):
  name = models.CharField(max_length = 255)
  description = models.CharField(max_length = 255)
  price = models.FloatField()
  #alternative 
  #proyect = models.ForeignKey(Proyect, blank=True, null=True)
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


@receiver(post_save, sender=Proyect)
def proyect_mount(sender, instance,  **kwargs):
    currentinstanceid = instance.id
    totalmount =  instance.package.totalprice
    remaingmount =  instance.package.totalprice - instance.advancepayment
    print totalmount
    print instance.advancepayment 
    Proyect.objects.filter(id=currentinstanceid).update(mount=totalmount) #se llama al atributo update para no usar el metodo save que volveria a activar la senal
    Proyect.objects.filter(id=currentinstanceid).update(remaingpayment=remaingmount)
#al guardar el modelo se tiene que agregar 0 en los campos mount, advance y remain



