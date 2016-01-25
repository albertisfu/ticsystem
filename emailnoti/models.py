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


def my_handler(sender, instance, created, **kwargs):
    notify.send(instance, recipient=instance.user.user,verb='was saved')

post_save.connect(my_handler, sender=HostingService)