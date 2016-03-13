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
	activo = models.BooleanField(default=False)
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
	domain = models.CharField(max_length = 600, blank=True, null=True)
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
	def save(self, *args, **kwargs):
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

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

##Signals
#Signal billing cycle price update Hosting
@receiver(post_save, sender=HostingService)
def billingcycle_hosting(sender, instance, created, **kwargs):
	currentinstanceid = instance.id
	cycle_option = instance.billingcycle

	if cycle_option == 1:
		cycleprice = instance.hostingpackage.trimestralprice
		textd = 'Trimestral'
	elif cycle_option == 2:
		cycleprice = instance.hostingpackage.semestralprice
		textd = 'Semestral'
	elif cycle_option == 3:
		cycleprice = instance.hostingpackage.anualprice
		textd = 'Anual'
	elif  cycle_option == 4:
		cycleprice = instance.hostingpackage.bianualprice
		textd = 'Bianual'

	HostingService.objects.filter(id=currentinstanceid).update(cycleprice=cycleprice) #el precio se actualiza al cambiar el ciclo de pago
	
	paymentsa = PaymentNuevo.objects.filter(content_type_id=21,object_id=instance.id)

	nameh = instance.name
	namehl = nameh.split("-")  
	index = len(namehl)
	detect = namehl[index-1]
	#print detect

	if paymentsa or detect == 'proyect' : #existen pagos ya de este Hosting y verificamos si es un hosting de proyecto no creamos pago puesto que esta incluido
		pass
	else:
		now = timezone.now()
		string = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)
		payname=instance.user.user.username + '_'  + string
		hosting = instance.hostingpackage.name
		description = 'Pago'+' '+hosting+' '+textd
		customer = get_object_or_404(Customer, user = instance.user.user)
		print cycleprice
		mount = float(cycleprice)
		payment = PaymentNuevo.objects.create(name=payname, description=description, user=customer, mount=mount, status=1, content_type_id=21, object_id=instance.id)

	#email Admin New Service or Proyect purchase, no send on proyect hosting
	if created == True and detect != 'proyect':
		username = instance.user.name
		mount = float(cycleprice)
		description = instance.hostingpackage.name
		reference = instance.name
		pk = instance.pk
		htmlnewadmin = get_template('emailnewadminhosting.html')
		d = Context({ 'username': username, 'mount': mount, 'description': description, 'pk':pk, 'reference':reference })
		html_content = htmlnewadmin.render(d)
		msg = EmailMultiAlternatives(
			subject="Nuevo Service Hosting",
			body="Un nuevo Hospedaje Solicitado",
			from_email="Ticsup <contacto@serverticsup.com>",
			to=["Admin"+" "+"<ventas@ticsup.com>"],
			headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
		)
		msg.attach_alternative(html_content, "text/html")
		msg.send()





#Signal billing cycle price update Domain
@receiver(post_save, sender=DomainService)
def billingcycle_domain(sender, instance, created,  **kwargs):
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
	if created:
		if cycle_option == 1:
			last_renewnow = timezone.now()
			next_renew = last_renewnow + timedelta(days = 365) #verificar que la renovacion se haga en base a la fecha de ultima renovacion o bien del dia del pago si es nuevo servicio
		elif cycle_option == 2:
			last_renewnow = timezone.now()
			next_renew = last_renewnow + timedelta(days = 2*365)
		elif cycle_option == 3:
			last_renewnow = timezone.now()
			next_renew = last_renewnow + timedelta(days = 3*365)
		elif  cycle_option == 4:
			last_renewnow = timezone.now()
			next_renew = last_renewnow + timedelta(days = 4*365)
		DomainService.objects.filter(id=currentinstanceid).update(next_renew=next_renew, status = 2)





