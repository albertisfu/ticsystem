from django.db import models
from fileupload.models import *
from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField


class Content(models.Model):
  empresa = models.CharField(max_length=250)
  giro = models.CharField(max_length=2000)
  proyect = models.ForeignKey('proyects.Proyect')
  numbersections = models.CharField(max_length=1000)
  def __unicode__(self):
    return self.empresa

class LogoUpload(models.Model):
  content = models.ForeignKey(Content)
  attachment = models.ForeignKey(Picture)

  def __unicode__(self):
    return str(self.content) + self.attachment.__unicode__()




class Section(models.Model):
  name = models.CharField(max_length=250)
  text = RichTextField(config_name='text', blank=True, null=True)
  #archivos
  content = models.ForeignKey(Content)
  coment = models.TextField(max_length=255, blank=True, null=True)
  #custom field donde se pueda agregar titulo del contenido
  def __unicode__(self):
    return self.name

class FilesUpload(models.Model):
  section = models.ForeignKey(Section)
  attachment = models.ForeignKey(Picture)

  def __unicode__(self):
    return str(self.id) + self.attachment.__unicode__()



@receiver(post_save, sender=Content)
def proyect_mount(sender, instance,  **kwargs):
    currentinstanceid = instance.id
    f = Content.objects.get(id=currentinstanceid)
    p,created = Section.objects.get_or_create(name='Principal', content=instance)
    if created:
        p.save()

        