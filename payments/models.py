from django.db import models
from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages

from servicios.models import *
import datetime
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.contrib.admin.models import LogEntry

from datetime import datetime, timedelta


#####Pagos Unificados


class PaymentNuevo(models.Model): ##relacionarse con proyecto, domain y hosting
  name = models.CharField(max_length=255)
  description = models.CharField(max_length = 140)
  content_type = models.ForeignKey(ContentType)
  object_id = models.PositiveIntegerField()
  content_object = GenericForeignKey('content_type', 'object_id')
  user = models.ForeignKey('customers.Customer', to_field='user')
  mount = models.FloatField()
  bank = 1
  transfer = 2
  card = 3
  oxxo = 4
  paypal = 5
  payment_options = (
      (bank, 'Deposito'),
      (transfer, 'Trasferencia'),
      (card, 'Tarjeta'),
      (oxxo, 'Oxxo'),
      (paypal, 'Paypal'),
  )
  method = models.IntegerField(choices=payment_options, default=bank)
  pending = 1
  verified = 2
  conflict = 3
  cancel = 4
  refund = 5
  status_options = (
      (pending, 'Pendiente'), #en formas de pago como deposito o trasferencia, la comprobacion del pago es manual
      (verified, 'Verificado'), #cuando la comprobacion manual se realiza por el administrador o por el sistema de forma automatica
      (conflict, 'Conflicto'), #cuanto el pago no se pudo verificar o bien existe algun problema con el metodo de pago, tambien cuando solicitan alguna devolucion y no se concreta aun
      (cancel, 'Cancelado'),# cuando no se deposita el pago a la cuenta ya sea trasferencia, deposito o metodo automatico
      (refund, 'Rembolsado'), #cuando se devulve el dinero
  )
  status = models.IntegerField(choices=status_options, default=pending)
  date = models.DateTimeField(default=datetime.now)
  def __unicode__(self):
    return unicode(self.name)

from proyects.models import Proyect


@receiver(post_save, sender=PaymentNuevo)
def nuevo_pago_proyect2(sender, instance,  **kwargs):
  if isinstance(sender, LogEntry):
      return
  else:      
      print instance.content_type_id
      if instance.content_type_id==11:
        tmount = 0
        payments = PaymentNuevo.objects.filter(content_type_id=11,object_id=instance.object_id, status=2)
        for pay in payments:
          tmount = tmount + pay.mount
        print tmount
        proyect = Proyect.objects.get(id=instance.object_id)
        #print instance.status
        #if instance.status == 2: #guardamos pago al verificar y restamos del saldo pendiente
        print "paso"
        newadvance = tmount
        newremaing = proyect.mount - newadvance
        paymentinstance = proyect #es el proyecto vinculado al pago
        paymentinstance.advancepayment=newadvance
        paymentinstance.remaingpayment=newremaing
        if instance.status == 2: #pago verified
          paymentinstance.status=2 #set proyect as process         
        paymentinstance.save()

      if instance.content_type_id==21: #id de hosting
        service = HostingService.objects.get(id=instance.object_id)
        payments = PaymentNuevo.objects.filter(content_type_id=21,object_id=instance.object_id, status=2)
        tmount = 0
        for pay in payments:
          tmount = tmount + pay.mount #calculas el total sumando todos los pagos relacionados al servicio en caso de haber
        print service
        print "pago hosting"
        print instance.status
        if instance.status == 2: #pago verified service
          print tmount
          if tmount == service.cycleprice:
            if service.status ==1:
              print "service pendiente"
              cycle_option = service.billingcycle
              last_renew = service.last_renew
              next_renewnow = service.next_renew
              if cycle_option == 1:
                last_renewnow = datetime.now()
                next_renew = last_renewnow + timedelta(days = 3*365/12) #verificar que la renovacion se haga en base a la fecha de ultima renovacion o bien del dia del pago si es nuevo servicio
              elif cycle_option == 2:
                last_renewnow = datetime.now()
                next_renew = last_renewnow + timedelta(days = 6*365/12)
              elif cycle_option == 3:
                last_renewnow = datetime.now()
                next_renew = last_renewnow + timedelta(days = 365)
              elif  cycle_option == 4:
                last_renewnow = datetime.now()
                next_renew = last_renewnow + timedelta(days = 2*365)

              print next_renew
              HostingService.objects.filter(id=instance.object_id).update(next_renew=next_renew,last_renew=last_renewnow)

            #print "coincide" #verificamos que el precio pagado  corresponda al precio del paquete
            HostingService.objects.filter(id=instance.object_id).update(status=2)
            #service.status=2 #set service as active #se quito el save puesto que al dejarlo no hacia el update
            #service.save()
          else:
            #print "no corresponde"
            service.status=4 #set service as conflict
            service.save()

        if instance.status == 1 or instance.status == 3 or instance.status == 4 or instance.status == 5: 
          service.status=4 #en caso de marcar conflicto 
          service.save() 

      if instance.content_type_id==23: #id de dominio
        print "pago dominio"








