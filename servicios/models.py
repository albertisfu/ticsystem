from django.db import models


class Status(models.Model):
  name = models.CharField(max_length=255)
  def __unicode__(self):
    return self.name

class HostingPackage(models.Model):
  name = models.CharField(max_length = 255)
  description = models.CharField(max_length = 255)
  trimestralprice = models.FloatField(blank=True, null=True)
  semestralprice = models.FloatField(blank=True, null=True)
  anualprice = models.FloatField(blank=True, null=True)

  
  def __unicode__(self):
    return self.name


class HostingService(models.Model):
  name = models.CharField(max_length = 255)
  user = models.ForeignKey('customers.Customer', to_field='user') #se vincula la relacion hacia el campo que apunta al user_id de customer y a su vez de User ya que de otra forma se revuelven las consultas
  billingcycle = #choices
  cycleprice = models.FloatField(blank=True, null=True)
  hostingpackage = models.ForeignKey(HostingPackage)
  status = models.ForeignKey(Status)
  created_at = models.DateTimeField(auto_now_add=True)
  last_renew = models.DateTimeField()
  next_renew = models.DateTimeField()
  hosting_panel = models.CharField(max_length = 600)
  webmail = models.CharField(max_length = 600)
  ftp_server = models.CharField(max_length = 600)
  ftp_port = models.CharField(max_length = 600)
  ftp_port = models.CharField(max_length = 600)

  def __unicode__(self):
    return self.name




