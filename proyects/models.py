from django.db import models
from customers.models import Customer
from django.db.models import signals
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
import datetime

from django.utils import timezone

from django.shortcuts import get_object_or_404



class Type(models.Model):
  name = models.CharField(max_length=255)
  def __unicode__(self):
    return self.name

class Status(models.Model):
  name = models.CharField(max_length=255)
  def __unicode__(self):
    return self.name

class Package(models.Model):
  name = models.CharField(max_length = 255)
  description = models.CharField(max_length = 255)
  totalprice = models.FloatField(blank=True, null=True)
  featureds = models.ManyToManyField('Featured')
  hosting = models.ForeignKey('servicios.HostingPackage', blank=True, null=True)
  activation = models.BooleanField(default=False)
  #services
  #def save(self, *args, **kwargs):
      #self.totalprice = 10
      #featuredins = self.featureds
      #print featuredins
      #print "guardado"
      #super(Package, self).save(*args, **kwargs)

  def __unicode__(self):
    return self.name


#the next receiver update the total price of package instance based on their features and hosting package
def post_save_mymodel(sender, instance, *args, **kwargs):
    currentinstanceid = instance.id
    currentinstance = Package.objects.get(id=currentinstanceid)
    featuredins = currentinstance.featureds.all()
    total = 0
    for featured in currentinstance.featureds.all():
      price = featured.price
      total = total + price
    #if currentinstance.hosting:
     # hostingprice = currentinstance.hosting.anualprice #add price anual of hosting
      #total = total + hostingprice
    totalinstance = Package.objects.get(id=currentinstanceid)
    totalinstance.totalprice=total
    totalinstance.save()
     #if action == 'post_add' and not reverse:
        #for e in instance.my_m2mfield.all():
            # Query including "e""" #Modificar deacuerdo a las acciones
m2m_changed.connect(post_save_mymodel, sender=Package.featureds.through)



class Proyect(models.Model):
  name = models.CharField(max_length = 255)
  description = models.CharField(max_length = 140)
  domain = models.CharField(max_length = 300, blank=True, null=True)
  user = models.ForeignKey('customers.Customer', to_field='user') #se vincula la relacion hacia el campo que apunta al user_id de customer y a su vez de User ya que de otra forma se revuelven las consultas
  progress = models.PositiveIntegerField(blank=True, null=True)
  independent = models.BooleanField(default=False)
  mount = models.FloatField(blank=True, null=True)
  deposit = models.IntegerField(default=35)
  advancepayment = models.FloatField(blank=True, null=True)
  remaingpayment = models.FloatField(blank=True, null=True)
  package = models.ForeignKey(Package)
  active = models.BooleanField(default=False)
  pendiente = 1
  proceso = 2
  terminado = 3
  cancelado = 4
  status_options = (
    (pendiente, 'Pendiente'),
    (proceso, 'Proceso'),
    (terminado, 'Terminado'),
    (cancelado, 'Cancelado'),
  )
  status = models.IntegerField(choices=status_options, default=pendiente)
  pub_date = models.DateTimeField(auto_now_add=True)
  def __unicode__(self):
    return self.name
#al guardar el modelo se tiene que agregar 0 en los campos mount, advance y remain

class Featured(models.Model):
  name = models.CharField(max_length = 255)
  description = models.CharField(max_length = 255)
  price = models.FloatField()
  #alternative 
  #proyect = models.ForeignKey(Proyect, blank=True, null=True)
  def __unicode__(self):
    return self.name

from payments.models import PaymentNuevo

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

#the next receiver update the totalmount and remaingmount of a proyect instance based on it package
@receiver(post_save, sender=Proyect)  
def proyect_mount(sender, instance,  **kwargs):
  currentinstanceid = instance.id
  if instance.independent == False:
    print "no independent"
    totalmount =  instance.package.totalprice
    #print totalmount
    Proyect.objects.filter(id=currentinstanceid).update(mount=totalmount) #se llama al atributo update para no usar el metodo save que volveria a activar la senal
    payments = PaymentNuevo.objects.filter(content_type_id=11,object_id=instance.id, status=2)
    tmount =0
    for pay in payments:
          tmount = tmount + pay.mount
    remaingmount =  instance.package.totalprice - tmount
    advanced = tmount
    Proyect.objects.filter(id=currentinstanceid).update(remaingpayment=remaingmount, advancepayment = advanced)

    paymentsa = PaymentNuevo.objects.filter(content_type_id=11,object_id=instance.id)

    if paymentsa:
      pass
    else:
      now = timezone.now()
      string = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)
      name = instance.user.user.username
      payname = name + '_'+string
      package = instance.package.name
      description = 'Pago adelanto'+' '+package
      customer = get_object_or_404(Customer, user = instance.user.user)
      mount = totalmount * (float(instance.deposit)/100)
      payment = PaymentNuevo.objects.create(name=payname, description=description, user=customer, mount=mount, status=1, content_type_id=11, object_id=instance.id)

  if instance.independent == True:
    remaingmount =  instance.mount - instance.advancepayment
    Proyect.objects.filter(id=currentinstanceid).update(remaingpayment=remaingmount)

    """ if instance.status==2 and instance.active == False: #mail to active proyect
           print instance.active
           print 'mail'
           htmlverified = get_template('emailactiveproyect.html')
           username = instance.user.name
           usermail = instance.user.email
           mount = instance.mount
           description = instance.description
           reference = instance.name
           pk = instance.pk
           d = Context({ 'username': username, 'mount': mount, 'description': description, 'pk':pk, 'reference':reference })
           html_content = htmlverified.render(d)
           msg = EmailMultiAlternatives(
               subject="Pago Verificado/Activacion",
               body="Hemos Verificado su pago, Gracias! ",
               from_email="Ticsup <contacto@serverticsup.com>",
               to=[username+" "+"<"+usermail+">"],
               headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
           )
           msg.attach_alternative(html_content, "text/html")
           msg.send()
           """


@receiver(pre_save, sender=Proyect)
def activation_mails(sender, instance, **kwargs):
  if instance.id:
    proyect = Proyect.objects.get(pk=instance.id)
    old_status = proyect.status
    print'old'
    print old_status
    new_status = instance.status
    print'new'
    print new_status
    print 'active'
    print instance.active
    package = instance.package
    activation = package.activation
    #send mail after verified payment and activation link.
    if old_status == 1  and new_status == 2 and instance.active == False and activation == True:
      print 'new proyect'
      print instance.active
      print 'mail'
      payments = PaymentNuevo.objects.filter(content_type_id=11,object_id=instance.id, status=2).count()
      print payments
      if payments == 1:
        payment = PaymentNuevo.objects.get(content_type_id=11,object_id=instance.id, status=2)
        htmlverified = get_template('emailactiveproyect.html')
        username = instance.user.name
        usermail = instance.user.email
        mount =  payment.mount
        description = payment.description
        reference = payment.name
        pk = instance.pk
        d = Context({ 'username': username, 'mount': mount, 'description': description, 'pk':pk, 'reference':reference })
        html_content = htmlverified.render(d)
        msg = EmailMultiAlternatives(
             subject="Pago Verificado/Activacion",
             body="Hemos Verificado su pago, Gracias! ",
             from_email="Ticsup <contacto@serverticsup.com>",
             to=[username+" "+"<"+usermail+">"],
             headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
         )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        #send mail after verified payment without activation link
    if old_status == 1  and new_status == 2 and instance.active == False and activation == False:
      print 'new proyect without activation'
      print instance.active
      print 'only mail verified'
      payments = PaymentNuevo.objects.filter(content_type_id=11,object_id=instance.id, status=2)
      if payments:
        payment = PaymentNuevo.objects.get(content_type_id=11,object_id=instance.id, status=2)
        htmlverified = get_template('emailverified.html')
        username = instance.user.name
        usermail = instance.user.email
        mount =  payment.mount
        description = payment.description
        reference = payment.name
        pk = payment.pk
        d = Context({ 'username': username, 'mount': mount, 'description': description, 'pk':pk, 'reference':reference })
        html_content = htmlverified.render(d)
        msg = EmailMultiAlternatives(
             subject="Pago Verificado",
             body="Hemos Verificado su pago, Gracias! ",
             from_email="Ticsup <contacto@serverticsup.com>",
             to=[username+" "+"<"+usermail+">"],
             headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
         )
        msg.attach_alternative(html_content, "text/html")
        msg.send()





#al guardar el modelo se tiene que agregar 0 en los campos mount, advance y remain



