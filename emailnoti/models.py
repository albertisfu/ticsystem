from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.


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
def payments_noti(sender, instance, created, **kwargs):
	if instance.status == 1:
		notify.send(instance, recipient=instance.user.user, verb='Pago Pendiente')
	if instance.status == 2:
		notify.send(instance, recipient=instance.user.user, verb='Pago Verificado')

post_save.connect(payments_noti, sender=PaymentNuevo)