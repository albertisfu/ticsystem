from django.db import models
from customers.models import Customer


class Type(models.Model):
  name = models.CharField(max_length=255)
  def __unicode__(self):
    return self.name

class Status(models.Model):
  name = models.CharField(max_length=255)
  def __unicode__(self):
    return self.name

class Proyect(models.Model):
  name = models.CharField(max_length = 255)
  description = models.CharField(max_length = 140)
  user = models.ForeignKey('customers.Customer', to_field='user') #se vincula la relacion hacia el campo que apunta al user_id de customer y a su vez de User ya que de otra forma se revuelven las consultas
  #feature = models.ForeignKey('features.Featured')
  #customer = models.ForeignKey('customers.Customer')
  #developer = models.ForeignKey('developers.Developer')
  #content = models.ForeignKey('contents.Content')
  progress = models.PositiveIntegerField()
  mount = models.FloatField()
  advancepayment = models.FloatField()
  remaingpayment = models.FloatField()
  type1 = models.ForeignKey(Type)
  status = models.ForeignKey(Status)
  pub_date = models.DateTimeField('Fecha Creacion')
  def __unicode__(self):
    return self.name
