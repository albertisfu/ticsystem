from django.db import models
from proyects.models import Proyect

class Featured(models.Model):
  name = models.CharField(max_length = 255)
  description = models.CharField(max_length = 255)
  price = models.FloatField()
  #alternative 
  proyect = models.ForeignKey(Proyect)
  #proyect = models.ForeignKey('proyects.Proyect')
  def __unicode__(self):
    return self.name
