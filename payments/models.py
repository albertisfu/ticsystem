from django.db import models
from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from proyects.models import Proyect
from servicios.models import *
import datetime


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




