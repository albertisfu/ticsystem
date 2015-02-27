from django.db import models
from fileupload.models import *
from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver


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
  text = models.TextField(max_length=2000, blank=True, null=True)
  #archivos
  content = models.ForeignKey(Content)
  coment = models.TextField(max_length=255, blank=True, null=True)
  #custom field donde se pueda agregar titulo del contenido
  def __unicode__(self):
    return self.name



@receiver(post_save, sender=Content)
def proyect_mount(sender, instance,  **kwargs):
    currentinstanceid = instance.id
    f = Content.objects.get(id=currentinstanceid)
    sections = [x for x in f.numbersections.split(',') if x]
    for section in sections:
        a = Section(name=section, content=instance)
        a.save()
        print a