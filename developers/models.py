from django.db import models

class Developer(models.Model):
  name = models.CharField(max_length = 255)
  phone = models.CharField(max_length = 50)
  movil = models.CharField(max_length = 50)
  email = models.CharField(max_length = 255)
  proyect = models.ForeignKey('proyects.Proyect')
  #pagos
  #soporte
  def __unicode__(self):
    return self.name
