from django.db import models

class Content(models.Model):
  name = models.CharField(max_length=250)
  proyect = models.ForeignKey('proyects.Proyect')
  def __unicode__(self):
    return self.name



class Section(models.Model):
  name = models.CharField(max_length=250)
  text = models.TextField(max_length=2000)
  #archivos
  content = models.ForeignKey(Content)
  coment = models.TextField(max_length=255)
  def __unicode__(self):
    return self.name