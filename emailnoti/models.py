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


#signal to send notify
#And send emails too
def payments_noti(sender, instance, created, **kwargs):
	htmlpending = get_template('emailpending.html')
	htmlverified = get_template('emailverified.html')
	htmlactivehosting = get_template('emailactivehosting.html')
	username = instance.user.name
	usermail = instance.user.email
	mount = instance.mount
	description = instance.description
	reference = instance.name
	pk = instance.pk
	if instance.status == 1:
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

	if instance.status == 2:
		notify.send(instance, recipient=instance.user.user, verb='Pago Verificado')
		if instance.content_type_id==21:
			hosting = HostingService.objects.get(id=instance.object_id)
			pk = hosting.pk
			d = Context({ 'username': username, 'mount': mount, 'description': description, 'pk':pk, 'reference':reference })
			html_content = htmlactivehosting.render(d)
			msg = EmailMultiAlternatives(
					subject="Pago Verificado",
					body="Hemos Verificado su pago, Gracias! ",
					from_email="Ticsup <contacto@serverticsup.com>",
					to=[username+" "+"<"+usermail+">"],
					headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
			)
			msg.attach_alternative(html_content, "text/html")
			msg.send()






post_save.connect(payments_noti, sender=PaymentNuevo)