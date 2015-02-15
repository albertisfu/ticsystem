from django.db import models
from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from proyects.models import Proyect
import datetime


class Method(models.Model):
  name = models.CharField(max_length=255)
  def __unicode__(self):
    return unicode(self.name)

class Payment(models.Model):
  name = models.CharField(max_length=255)
  description = models.CharField(max_length = 140)
  proyect = models.ForeignKey('proyects.Proyect')
  user = models.ForeignKey('customers.Customer', to_field='user')
  mount = models.FloatField()
  method = models.ForeignKey(Method)
  date = models.DateTimeField(default=datetime.datetime.now)
  def __unicode__(self):
    return unicode(self.name)

        #def es_popular(self):  con un metodo se puede hacer la verificacion
        #return self.votos > 10
        #es_popular.boolean = True

class VerifiedPayment(models.Model):
  payment = models.OneToOneField(Payment)
  revision = 1
  verified = 2
  conflict = 3
  status_options = (
      (revision, 'En Revision'),
      (verified, 'Verificado'),
      (conflict, 'Conflicto'),
  )
  status = models.IntegerField(choices=status_options, default=revision)
  date = models.DateTimeField(default=datetime.datetime.now)
  def __unicode__(self):
    return unicode(self.payment)

@receiver(post_save, sender=VerifiedPayment)
def nuevo_pago(sender, instance,  **kwargs):
  if instance.status == 2:
    currentinstanceid = instance.payment.proyect.id
    newadvance = instance.payment.proyect.advancepayment + instance.payment.mount
    newremaing = instance.payment.proyect.mount - newadvance
    paymentinstance = Proyect.objects.get(id=currentinstanceid)
    paymentinstance.advancepayment=newadvance
    paymentinstance.remaingpayment=newremaing
    paymentinstance.save()

  #print '%s' % newadvance + '  ' + '%s' % newremaing

###
#def create_badge(sender, instance, created, **kwargs):
    #print "Post save emited for", instance

#signals.post_save.connect(create_badge, sender=VerifiedPayment)

