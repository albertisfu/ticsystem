# -*- encoding: utf-8 -*-
from django.db import models
from encrypted_fields import EncryptedCharField
from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
#Models Hosting
class Status(models.Model):
  name = models.CharField(max_length=255)
  def __unicode__(self):
    return self.name

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
	status = models.ForeignKey(Status)
	created_at = models.DateTimeField(auto_now_add=True)
	last_renew = models.DateTimeField(blank=True, null=True)
	next_renew = models.DateTimeField(blank=True, null=True)
	hosting_panel = models.CharField(max_length = 600)
	hosting_password = EncryptedCharField(max_length = 10, blank=True, null=True)
	webmail = models.CharField(max_length = 600)
	ftp_server = models.CharField(max_length = 600)
	ftp_port = models.CharField(max_length = 600)
	ftp_password = EncryptedCharField(max_length = 10, blank=True, null=True)

	def save(self):
		if not self.id:
			self.last_renew = datetime.now()
			self.next_renew = datetime.now()
		super(HostingService, self).save()
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
	status = models.ForeignKey(Status)
	created_at = models.DateTimeField(auto_now_add=True)
	last_renew = models.DateTimeField(blank=True, null=True)
	next_renew = models.DateTimeField(blank=True, null=True)
	dns1 = models.CharField(max_length = 450, blank=True, null=True)
	dns2 = models.CharField(max_length = 450, blank=True, null=True)
	def save(self):
		if not self.id:
			print 'nada'
			self.last_renew = datetime.now()
			self.next_renew = datetime.now()
		super(DomainService, self).save()
	def __unicode__(self):
		return self.name


##Signals
#Signal billing cycle price update Hosting
@receiver(post_save, sender=HostingService)
def billingcycle_hosting(sender, instance,  **kwargs):
	currentinstanceid = instance.id
	cycle_option = instance.billingcycle
	last_renew = instance.last_renew
	next_renewnow = instance.next_renew
	if cycle_option == 1:
		cycleprice = instance.hostingpackage.trimestralprice
		next_renew = next_renewnow + timedelta(days = 3*365/12)
		last_renewnow = datetime.now()
	elif cycle_option == 2:
		cycleprice = instance.hostingpackage.semestralprice
		next_renew = next_renewnow + timedelta(days = 6*365/12)
		last_renewnow = datetime.now()
	elif cycle_option == 3:
		cycleprice = instance.hostingpackage.anualprice
		next_renew = next_renewnow + timedelta(days = 365)
		last_renewnow = datetime.now()
	elif  cycle_option == 4:
		cycleprice = instance.hostingpackage.bianualprice
		next_renew = next_renewnow + timedelta(days = 2*365)
		last_renewnow = datetime.now()
	HostingService.objects.filter(id=currentinstanceid).update(next_renew=next_renew)
	HostingService.objects.filter(id=currentinstanceid).update(last_renew=last_renewnow )
	HostingService.objects.filter(id=currentinstanceid).update(cycleprice=cycleprice)


#Signal billing cycle price update Domain
@receiver(post_save, sender=DomainService)
def billingcycle_domain(sender, instance,  **kwargs):
	currentinstanceid = instance.id
	cycle_option = instance.billingcycle 
	last_renew = instance.last_renew
	next_renewnow = instance.next_renew
	if cycle_option == 1:
		cycleprice = instance.domain.anualprice
		next_renew = next_renewnow + timedelta(days = 365)
		last_renewnow = datetime.now()
	elif cycle_option == 2:
		cycleprice = instance.domain.bianualprice
		next_renew = next_renewnow + timedelta(days = 2*365)
		last_renewnow = datetime.now()
	elif cycle_option == 3:
		cycleprice = instance.domain.trianualprice
		next_renew = next_renewnow + timedelta(days = 3*365)
		last_renewnow = datetime.now()
	elif  cycle_option == 4:
		cycleprice = instance.domain.quadanualprice
		next_renew = next_renewnow + timedelta(days = 4*365)
		last_renewnow = datetime.now()
	DomainService.objects.filter(id=currentinstanceid).update(next_renew=next_renew)
	DomainService.objects.filter(id=currentinstanceid).update(last_renew=last_renewnow )
	DomainService.objects.filter(id=currentinstanceid).update(cycleprice=cycleprice)





