# -*- encoding: utf-8 -*-
from django.db import models
from encrypted_fields import EncryptedCharField
from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from customers.models import Customer
from django.shortcuts import get_object_or_404

from notifications.signals import notify


from django.contrib.auth.models import User

from django.utils import timezone



#Models Hosting
class HostingPackage(models.Model):
  name = models.CharField(max_length = 255)
  description = models.TextField()
  trimestralprice = models.FloatField(blank=True, null=True)
  semestralprice = models.FloatField(blank=True, null=True)
  anualprice = models.FloatField(blank=True, null=True)
  bianualprice = models.FloatField(blank=True, null=True)
  
  def __unicode__(self):
    return self.name


class HostingService(models.Model):
	name = models.CharField(max_length = 255)
	user = models.ForeignKey('customers.Customer', to_field='user')
	trimestral = 1
	semestral = 2
	anual = 3
	bianual = 4
	cycle_options = (
		(trimestral, 'Trimestral'),
		(semestral, 'Semestral'),
		(anual, 'Anual'),
		(bianual, 'Bianual'),
	)
	billingcycle = models.IntegerField(choices=cycle_options, default=anual)
	cycleprice = models.FloatField(blank=True, null=True)
	hostingpackage = models.ForeignKey(HostingPackage)
	pending = 1
	active = 2
	expired = 3
	conflict = 4
	status_options = (
		(pending, 'Pendiente'),
		(active, 'Activo'),
		(expired, 'Terminado'),
		(conflict, 'Conflicto'),
		#agregar un estado conflicto que servira cuando un pago pase de verificado a otro estado diferente
	)
	status = models.IntegerField(choices=status_options, default=pending)
	created_at = models.DateTimeField(auto_now_add=True)
	last_renew = models.DateTimeField(blank=True, null=True)
	next_renew = models.DateTimeField(blank=True, null=True)
	days_left = models.IntegerField(blank=True, null=True)
	hosting_panel = models.CharField(max_length = 600, blank=True, null=True)
	hosting_password = EncryptedCharField(max_length = 10, blank=True, null=True)
	webmail = models.CharField(max_length = 600, blank=True, null=True )
	ftp_server = models.CharField(max_length = 600, blank=True, null=True)
	ftp_port = models.CharField(max_length = 600, blank=True, null=True)
	ftp_password = EncryptedCharField(max_length = 10, blank=True, null=True)

	def save(self, *args, **kwargs):
		if not self.id: ##valores default crear servicio
			print "actualizo"
			self.last_renew = timezone.now()
			self.next_renew = timezone.now()
		if self.pk is not None: ##revisamos si ha cambiado el ciclo de pago
			orig = HostingService.objects.get(pk=self.pk)
			if orig.billingcycle != self.billingcycle:
				self.status = 1 ##si cambia se pone en pendiente
		super(HostingService, self).save(*args, **kwargs)
	def __unicode__(self):
		return self.name

#Models Domains

class Domain(models.Model):
  tdl = models.CharField(max_length = 255)
  anualprice = models.FloatField(blank=True, null=True)
  bianualprice = models.FloatField(blank=True, null=True)
  trianualprice = models.FloatField(blank=True, null=True)
  quadanualprice = models.FloatField(blank=True, null=True)
  
  def __unicode__(self):
    return self.tdl

class DomainService(models.Model):
	name = models.CharField(max_length = 400)
	user = models.ForeignKey('customers.Customer', to_field='user')
	anual = 1
	bianual = 2
	trianual = 3
	quadanual = 4
	cycle_options = (
		(anual, '1 año'),
		(bianual, '2 años'),
		(trianual, '3 años'),
		(quadanual, '4 años'),
	)
	billingcycle = models.IntegerField(choices=cycle_options, default=anual)
	cycleprice = models.FloatField(blank=True, null=True)
	domain = models.ForeignKey(Domain)
	pending = 1
	active = 2
	expired = 3
	conflict = 4
	status_options = (
		(pending, 'Pendiente'),
		(active, 'Activo'),
		(expired, 'Terminado'),
		(conflict, 'Conflicto'),
	)
	status = models.IntegerField(choices=status_options, default=pending)
	created_at = models.DateTimeField(auto_now_add=True)
	last_renew = models.DateTimeField(blank=True, null=True)
	next_renew = models.DateTimeField(blank=True, null=True)
	days_left = models.IntegerField(blank=True, null=True)
	dns1 = models.CharField(max_length = 450, blank=True, null=True)
	dns2 = models.CharField(max_length = 450, blank=True, null=True)
	def save(self):
		if not self.id:
			self.last_renew = timezone.now()
			self.next_renew = timezone.now()
		if self.pk is not None: ##revisamos si ha cambiado el ciclo de pago
			orig = DomainService.objects.get(pk=self.pk)
			if orig.billingcycle != self.billingcycle:
				self.status = 1 #si cambia se pone en pendiente			
		super(DomainService, self).save()
	def __unicode__(self):
		return self.name

from payments.models import PaymentNuevo

##Signals
#Signal billing cycle price update Hosting
@receiver(post_save, sender=HostingService)
def billingcycle_hosting(sender, instance,  **kwargs):
	currentinstanceid = instance.id
	cycle_option = instance.billingcycle

	if cycle_option == 1:
		cycleprice = instance.hostingpackage.trimestralprice
	elif cycle_option == 2:
		cycleprice = instance.hostingpackage.semestralprice
	elif cycle_option == 3:
		cycleprice = instance.hostingpackage.anualprice
	elif  cycle_option == 4:
		cycleprice = instance.hostingpackage.bianualprice

	HostingService.objects.filter(id=currentinstanceid).update(cycleprice=cycleprice) #el precio se actualiza al cambiar el ciclo de pago
	
	paymentsa = PaymentNuevo.objects.filter(content_type_id=21,object_id=instance.id)

	if paymentsa:
		pass
	else:
		now = timezone.now()
		string = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)
		name = instance.user.name
		payname = name + '_' + "hosting"+string
		customer = get_object_or_404(Customer, user = instance.user.user)
		print cycleprice
		mount = float(cycleprice)
		payment = PaymentNuevo.objects.create(name=payname, description=payname, user=customer, mount=mount, status=1, content_type_id=21, object_id=instance.id)


#Signal billing cycle price update Domain
@receiver(post_save, sender=DomainService)
def billingcycle_domain(sender, instance,  **kwargs):
	currentinstanceid = instance.id
	cycle_option = instance.billingcycle 
	last_renew = instance.last_renew
	next_renewnow = instance.next_renew
	lastcycle = instance.billingcycle
	status = instance.status
	if cycle_option == 1:
		cycleprice = instance.domain.anualprice
	elif cycle_option == 2:
		cycleprice = instance.domain.bianualprice
	elif cycle_option == 3:
		cycleprice = instance.domain.trianualprice
	elif  cycle_option == 4:
		cycleprice = instance.domain.quadanualprice
	DomainService.objects.filter(id=currentinstanceid).update(cycleprice=cycleprice)





