from django.db import models
from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages

from servicios.models import *
import datetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.contrib.admin.models import LogEntry

#Elimnar metodos OJO
class Method(models.Model):
  name = models.CharField(max_length=255)
  def __unicode__(self):
    return unicode(self.name)

#####Pagos Proyectos
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



class PaymentNuevo(models.Model): ##relacionarse con proyecto, domain y hosting
  name = models.CharField(max_length=255)
  description = models.CharField(max_length = 140)
  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey('content_type', 'object_id')
  user = models.ForeignKey('customers.Customer', to_field='user')
  mount = models.FloatField()
  bank = 1
  transfer = 2
  card = 3
  oxxo = 4
  paypal = 5
  payment_options = (
      (bank, 'Deposito'),
      (transfer, 'Trasferencia'),
      (card, 'Tarjeta'),
      (oxxo, 'Oxxo'),
      (paypal, 'Paypal'),
  )
  method = models.IntegerField(choices=payment_options, default=bank)
  pending = 1
  verified = 2
  conflict = 3
  cancel = 4
  refund = 5
  status_options = (
      (pending, 'Pendiente'), #en formas de pago como deposito o trasferencia, la comprobacion del pago es manual
      (verified, 'Verificado'), #cuando la comprobacion manual se realiza por el administrador o por el sistema de forma automatica
      (conflict, 'Conflicto'), #cuanto el pago no se pudo verificar o bien existe algun problema con el metodo de pago, tambien cuando solicitan alguna devolucion y no se concreta aun
      (cancel, 'Cancelado'),# cuando no se deposita el pago a la cuenta ya sea trasferencia, deposito o metodo automatico
      (refund, 'Rembolsado'), #cuando se devulve el dinero
  )
  status = models.IntegerField(choices=status_options, default=pending)
  date = models.DateTimeField(default=datetime.datetime.now)
  def __unicode__(self):
    return unicode(self.name)
    
from proyects.models import Proyect
@receiver(post_save, sender=PaymentNuevo)
def nuevo_pago_proyect2(sender, instance,  **kwargs):
  if isinstance(sender, LogEntry):
      return
  else:      
      if instance.content_type_id==11:
        tmount = 0
        payments = PaymentNuevo.objects.filter(content_type_id=11,object_id=instance.object_id, status=2)
        for pay in payments:
          tmount = tmount + pay.mount
        print tmount
        proyect = Proyect.objects.get(id=instance.object_id)
        #print instance.status
        #if instance.status == 2: #guardamos pago al verificar y restamos del saldo pendiente
        print "paso"
        currentinstanceid = proyect.id
        newadvance = tmount
        newremaing = proyect.mount - newadvance
        paymentinstance = proyect #es el proyecto vinculado al pago
        paymentinstance.advancepayment=newadvance
        paymentinstance.remaingpayment=newremaing
        if instance.status == 2:
          paymentinstance.status=2         
        #print newremaing
        paymentinstance.save()

      if instance.content_type_id==29:
        service = HostingService.objects.get(id=instance.object_id)
        print service
        print "pago hosting"
        if instance.status == 2: #guardamos pago al verificar y restamos del saldo pendiente
          currentinstanceid = service.id
          paymentinstance.status=2
          print newremaing
          if newremaing<=0:
            paymentinstance.status=3
          paymentinstance.save()
        if instance.status == 3:  #en caso de marcar conflicto se descuenta el saldo del ultimo pago
          currentinstanceid = service.id
          newadvance = proyect.advancepayment - instance.mount
          newremaing = proyect.mount - newadvance
          paymentinstance = proyect
          paymentinstance.advancepayment=newadvance
          paymentinstance.remaingpayment=newremaing
          print paymentinstance.remaingpayment
          if newremaing>0:
            paymentinstance.status=2
          if newremaing<=0:
            paymentinstance.status=3
          paymentinstance.save() 

      if instance.content_type_id==31:
        print "pago dominio"

#######ojooo
##OJJJJO quitar los pagos individuales y verificaciones

class VerifiedPaymentNuevo(models.Model):
  payment = generic.GenericRelation(PaymentNuevo)
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
def nuevo_pago_proyect(sender, instance,  **kwargs):
  if instance.status == 2: #guardamos pago al verificar y restamos del saldo pendiente
    currentinstanceid = instance.payment.proyect.id
    newadvance = instance.payment.proyect.advancepayment + instance.payment.mount
    newremaing = instance.payment.proyect.mount - newadvance
    paymentinstance = Proyect.objects.get(id=currentinstanceid)
    paymentinstance.advancepayment=newadvance
    paymentinstance.remaingpayment=newremaing
    paymentinstance.status=2
    print newremaing
    if newremaing<=0:
      paymentinstance.status=3
    paymentinstance.save()
  if instance.status == 3:  #en caso de marcar conflicto se descuenta el saldo del ultimo pago
    currentinstanceid = instance.payment.proyect.id
    newadvance = instance.payment.proyect.advancepayment - instance.payment.mount
    newremaing = instance.payment.proyect.mount - newadvance
    paymentinstance = Proyect.objects.get(id=currentinstanceid)
    paymentinstance.advancepayment=newadvance
    paymentinstance.remaingpayment=newremaing
    print paymentinstance.remaingpayment
    if newremaing>0:

      paymentinstance.status=2
    if newremaing<=0:
      paymentinstance.status=3
    paymentinstance.save()

######Pago Hospedaje
class PaymentHosting(models.Model):
  name = models.CharField(max_length=255)
  description = models.CharField(max_length = 140)
  service = models.ForeignKey('servicios.HostingService')
  user = models.ForeignKey('customers.Customer', to_field='user')
  mount = models.FloatField()
  method = models.ForeignKey(Method)
  date = models.DateTimeField(default=datetime.datetime.now)
  def __unicode__(self):
    return unicode(self.name)


class VerifiedPaymentHosting(models.Model):
  payment = models.OneToOneField(PaymentHosting)
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

@receiver(post_save, sender=VerifiedPaymentHosting)
def nuevo_pago_hosting(sender, instance,  **kwargs):
  if instance.status == 2: #si se verifica el pago
    pricehosting = instance.payment.service.cycleprice
    mountpay = instance.payment.mount
    currentinstanceid = instance.payment.service.id
    if pricehosting == mountpay: #verificamos el pago coincida con el monto del ciclo de pago entonces lo activamos
      paymentinstance = HostingService.objects.get(id=currentinstanceid)
      paymentinstance.status=2
      paymentinstance.save()




#Pago Dominio

class PaymentDomain(models.Model):
  name = models.CharField(max_length=255)
  description = models.CharField(max_length = 140)
  service = models.ForeignKey('servicios.DomainService')
  user = models.ForeignKey('customers.Customer', to_field='user')
  mount = models.FloatField()
  method = models.ForeignKey(Method)
  date = models.DateTimeField(default=datetime.datetime.now)
  def __unicode__(self):
    return unicode(self.name)


class VerifiedPaymentDomain(models.Model):
  payment = models.OneToOneField(PaymentDomain)
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

@receiver(post_save, sender=VerifiedPaymentDomain)
def nuevo_pago_domain(sender, instance,  **kwargs):
  if instance.status == 2: #si se verifica el pago
    pricedomain = instance.payment.service.cycleprice
    mountpay = instance.payment.mount
    currentinstanceid = instance.payment.service.id
    if pricedomain == mountpay: #verificamos el pago coincida con el monto del ciclo de pago entonces lo activamos
      paymentinstance = DomainService.objects.get(id=currentinstanceid)
      paymentinstance.status=2
      paymentinstance.save()




