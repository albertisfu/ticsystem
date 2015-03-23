from django.db import models
from encrypted_fields import EncryptedCharField

class Status(models.Model):
  name = models.CharField(max_length=255)
  def __unicode__(self):
    return self.name

class HostingPackage(models.Model):
  name = models.CharField(max_length = 255)
  description = models.TextField()
  trimestralprice = models.FloatField(blank=True, null=True)
  semestralprice = models.FloatField(blank=True, null=True)
  anualprice = models.FloatField(blank=True, null=True)
  bianualprice = models.FloatField(blank=True, null=True)
  
  def __unicode__(self):
    return self.name


class HostingService(models.Model):
  name = models.CharField(max_length = 255)
  user = models.ForeignKey('customers.Customer', to_field='user')
  trimestral = 1
  semestral = 2
  anual = 3
  bianual = 4
  cycle_options = (
      (trimestral, 'Trimestral'),
      (semestral, 'Semestral'),
      (anual, 'Anual'),
      (bianual, 'Bianual'),
  )
  billingcycle = models.IntegerField(choices=cycle_options, default=anual)
  cycleprice = models.FloatField(blank=True, null=True)
  hostingpackage = models.ForeignKey(HostingPackage)
  status = models.ForeignKey(Status)
  created_at = models.DateTimeField(auto_now_add=True)
  last_renew = models.DateTimeField()
  next_renew = models.DateTimeField()
  hosting_panel = models.CharField(max_length = 600)
  hosting_password = EncryptedCharField(max_length = 10, blank=True, null=True)
  webmail = models.CharField(max_length = 600)
  ftp_server = models.CharField(max_length = 600)
  ftp_port = models.CharField(max_length = 600)
  ftp_password = EncryptedCharField(max_length = 10, blank=True, null=True)

  def __unicode__(self):
    return self.name




