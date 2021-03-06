# -*- encoding: utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from payments.models import PaymentNuevo
from django.utils import timezone


class EmailTemplate(models.Model):
  name = models.CharField(max_length = 255)
  description = models.TextField()
  text = RichTextField(config_name='text')
  
  def __unicode__(self):
    return self.name

from django.db.models.signals import post_save
from notifications.signals import notify
from servicios.models import HostingService
from payments.models import PaymentNuevo


from proyects.models import Proyect
from django.conf import settings

#signal to send notify
#And send emails too
def payments_noti(sender, instance, created, **kwargs):
	htmlpending = get_template('emailpending.html')
	htmlnewadmin = get_template('emailnewadmin.html')
	htmlverified = get_template('emailverified.html')
	htmlverifiedadmin = get_template('emailverifiedadmin.html')
	htmlactivehosting = get_template('emailactivehosting.html')
	username = instance.user.name
	usermail = instance.user.email
	mount = instance.mount
	description = instance.description
	reference = instance.name
	pk = instance.pk
	if instance.status == 1:#email New Payment Order to Customer
		if created ==True:
			d = Context({ 'username': username, 'mount': mount, 'description': description, 'pk':pk, 'reference':reference })
			html_content = htmlpending.render(d)
			msg = EmailMultiAlternatives(
					subject="Nueva Orden de Pago/Compra",
					body="Hemos recibido tu nueva orden de compra/pago",
					from_email="Ticsup <contacto@serverticsup.com>",
					to=[username+" "+"<"+usermail+">"],
					headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
			)
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			notify.send(instance, recipient=instance.user.user, verb='Pago Pendiente')

		try:
			key = instance.description.split(' ')[0].encode('utf-8')
			print key
			if key == "Renovación":
			#email Admin New Service or Proyect purchase
				d = Context({ 'username': username, 'mount': mount, 'description': description, 'pk':pk, 'reference':reference })
				html_content = htmlnewadmin.render(d)
				msg = EmailMultiAlternatives(
						subject="Nueva Orden de Pago/Compra",
						body="Se ha recibido tu nueva orden de compra/pago",
						from_email="Ticsup <contacto@serverticsup.com>",
						to=["Admin"+" "+"<ventas@ticsup.com>"],
						headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
				)
				msg.attach_alternative(html_content, "text/html")
				msg.send()
		except Exception as ex:
			pass
			print 'exception'
		


	if instance.status == 2: #if payment is verified
		notify.send(instance, recipient=instance.user.user, verb='Pago Verificado')
		if instance.content_type_id==settings.HOSTINGID: #check if instance payment is a hosting service
			hosting = HostingService.objects.get(id=instance.object_id) #send mail Payment Verified and Activation when hosting is not active
			if hosting.activo==False:
				hosting = HostingService.objects.get(id=instance.object_id)
				pk = hosting.pk
				d = Context({ 'username': username, 'mount': mount, 'description': description, 'pk':pk, 'reference':reference })
				html_content = htmlactivehosting.render(d)
				msg = EmailMultiAlternatives(
						subject="Pago Verificado/Activacion",
						body="Hemos Verificado su pago, Gracias! ",
						from_email="Ticsup <contacto@serverticsup.com>",
						to=[username+" "+"<"+usermail+">"],
						headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
				)
				msg.attach_alternative(html_content, "text/html")
				msg.send()

			if hosting.activo==True: #When Hosting is active only send verified payment mail, for renovation only
				d = Context({ 'username': username, 'mount': mount, 'description': description, 'pk':pk, 'reference':reference })
				html_content = htmlverified.render(d)
				msg = EmailMultiAlternatives(
						subject="Pago Verificado",
						body="Hemos Verificado su pago, Gracias! ",
						from_email="Ticsup <contacto@serverticsup.com>",
						to=[username+" "+"<"+usermail+">"],
						headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
				)
				msg.attach_alternative(html_content, "text/html")
				msg.send()

		if instance.content_type_id==settings.DOMAINID: #send mail verified payment for Domains Renew
				d = Context({ 'username': username, 'mount': mount, 'description': description, 'pk':pk, 'reference':reference })
				html_content = htmlverified.render(d)
				msg = EmailMultiAlternatives(
						subject="Pago Verificado",
						body="Hemos Verificado su pago, Gracias! ",
						from_email="Ticsup <contacto@serverticsup.com>",
						to=[username+" "+"<"+usermail+">"],
						headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
				)
				msg.attach_alternative(html_content, "text/html")
				msg.send()


		if instance.content_type_id == settings.PROYECTID: #In proyects with 2 or more payments, it means is a "abono payment", only send verified payment mail 
			print 'verified proyect'
			payments = PaymentNuevo.objects.filter(content_type_id=settings.PROYECTID, object_id=instance.object_id, status=2).count()
			print 'payments emailnoti'
			print payments
			if payments >= 2: #verified if is second payment or major
				d = Context({ 'username': username, 'mount': mount, 'description': description, 'pk':pk, 'reference':reference })
				html_content = htmlverified.render(d)
				msg = EmailMultiAlternatives(
						subject="Pago Verificado",
						body="Hemos Verificado su pago, Gracias! ",
						from_email="Ticsup <contacto@serverticsup.com>",
						to=[username+" "+"<"+usermail+">"],
						headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
				)
				msg.attach_alternative(html_content, "text/html")
				msg.send()


		#email Admin Verified Payment
		d = Context({ 'username': username, 'mount': mount, 'description': description, 'pk':pk, 'reference':reference })
		html_content = htmlverifiedadmin.render(d)
		msg = EmailMultiAlternatives(
				subject="Nuevo Pago Verificado",
				body="Se ha recibido un nuevo pago",
				from_email="Ticsup <contacto@serverticsup.com>",
				to=["Admin"+" "+"<ventas@ticsup.com>"],
				headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
		)
		msg.attach_alternative(html_content, "text/html")
		msg.send()


post_save.connect(payments_noti, sender=PaymentNuevo)


