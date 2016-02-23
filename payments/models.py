from django.db import models
from django.db.models import signals
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages

import datetime
from django.utils import timezone

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.contrib.admin.models import LogEntry

from datetime import datetime, timedelta
from django.shortcuts import render_to_response,get_object_or_404, render

#####Pagos Unificados
from django.utils import timezone


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
  date = models.DateTimeField(default=timezone.now)
  def __unicode__(self):
    return unicode(self.name)

from proyects.models import Proyect
from servicios.models import DomainService, HostingService

from notifications.models import Notification

@receiver(post_save, sender=PaymentNuevo)
def nuevo_pago_proyect2(sender, instance,  **kwargs):
  if isinstance(sender, LogEntry):
      return
  else:      
      print instance.content_type_id
      if instance.content_type_id==11: #################   Proyect     ##############
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
          print 'notification proyect' 
          actorid = str(instance.pk) #pk of payment instance
          actorob = 13 #pk of payment content type
          useractor = instance.user.user.pk #pk of user
          #Mark notification as unread when payment is verified
          Notification.objects.filter(recipient_id=useractor, actor_content_type=actorob, actor_object_id=actorid).update(unread=0)
          #instance.user.user.notifications.unread().mark_all_as_read()
          paymentinstance.status=2 #set proyect as process         
        paymentinstance.save()

      if instance.content_type_id==21: #################      Hosting         ##############
        service = HostingService.objects.get(id=instance.object_id)
        payments = PaymentNuevo.objects.filter(content_type_id=21,object_id=instance.object_id, status=2)
        tmount = 0
        for pay in payments:
          tmount = tmount + pay.mount #calculas el total sumando todos los pagos relacionados al servicio en caso de haber
        print service
        print "pago hosting"
        print instance.status
        if instance.status == 2: #Pago verificado
          actorid = str(instance.pk) #pk of payment instance
          actorob = 13 #pk of payment content type
          useractor = instance.user.user.pk #pk of user
          #Mark notification as unread when payment is verified
          Notification.objects.filter(recipient_id=useractor, actor_content_type=actorob, actor_object_id=actorid).update(unread=0)
          if tmount >= service.cycleprice: #precio coincide con pago
            if service.status ==1: #servicio pendiente
              print "service pendiente"
              try:
                  key, cycle = instance.description.split('-')
                  print key
                  if key == "renovar":
                    cycle_option = int(cycle)
                    hosting = get_object_or_404(HostingService, id=instance.object_id)
                    print hosting.pk
                    hosting.billingcycle = cycle_option
                    hosting.save()
                  else: 
                    cycle_option = service.billingcycle

              except Exception as ex:
                  template = "An exception of type {0} occured. Arguments:\n{1!r}"
                  message = template.format(type(ex).__name__, ex.args)
                  cycle_option = service.billingcycle
                  print message
              if cycle_option == 1:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 3*365/12) #verificar que la renovacion se haga en base a la fecha de ultima renovacion o bien del dia del pago si es nuevo servicio
              elif cycle_option == 2:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 6*365/12)
              elif cycle_option == 3:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 365)
              elif  cycle_option == 4:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 2*365)

              print next_renew
              HostingService.objects.filter(id=instance.object_id).update(next_renew=next_renew,last_renew=last_renewnow,status=2)

            elif service.status ==2: #service active
              print "service active"
              try:
                  key, cycle = instance.description.split('-')
                  print key
                  if key == "renovar":
                    cycle_option = int(cycle)
                    hosting = get_object_or_404(HostingService, id=instance.object_id)
                    print hosting.pk
                    hosting.billingcycle = cycle_option
                    hosting.save()
                  else: 
                    cycle_option = service.billingcycle

              except Exception as ex:
                  template = "An exception of type {0} occured. Arguments:\n{1!r}"
                  message = template.format(type(ex).__name__, ex.args)
                  cycle_option = service.billingcycle
                  print message
              print cycle_option
              next = service.next_renew
              if cycle_option == 1:
                last_renewnow = timezone.now()
                next_renew = next + timedelta(days = 3*365/12) #verificar que la renovacion se haga en base a la fecha de ultima renovacion o bien del dia del pago si es nuevo servicio
              elif cycle_option == 2:
                last_renewnow = timezone.now()
                next_renew = next + timedelta(days = 6*365/12)
              elif cycle_option == 3:
                last_renewnow = timezone.now()
                next_renew = next + timedelta(days = 365)
              elif  cycle_option == 4:
                last_renewnow = timezone.now()
                next_renew = next + timedelta(days = 2*365)
              print next_renew
              HostingService.objects.filter(id=instance.object_id).update(next_renew=next_renew,last_renew=last_renewnow, status=2)

            elif service.status ==3: #service expired
              print "service expired"
              try:
                  key, cycle = instance.description.split('-')
                  print key
                  if key == "renovar":
                    cycle_option = int(cycle)
                    hosting = get_object_or_404(HostingService, id=instance.object_id)
                    print hosting.pk
                    hosting.billingcycle = cycle_option
                    hosting.save()
                  else: 
                    cycle_option = service.billingcycle

              except Exception as ex:
                  template = "An exception of type {0} occured. Arguments:\n{1!r}"
                  message = template.format(type(ex).__name__, ex.args)
                  cycle_option = service.billingcycle
                  print message
              if cycle_option == 1:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 3*365/12) #verificar que la renovacion se haga en base a la fecha de ultima renovacion o bien del dia del pago si es nuevo servicio
              elif cycle_option == 2:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 6*365/12)
              elif cycle_option == 3:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 365)
              elif  cycle_option == 4:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 2*365)

              print next_renew
              HostingService.objects.filter(id=instance.object_id).update(next_renew=next_renew,last_renew=last_renewnow,status=2)

            elif service.status ==4: #service conflict
              print "conflict service"
              try:
                  key, cycle = instance.description.split('-')
                  print key
                  if key == "renovar":
                    cycle_option = int(cycle)
                    hosting = get_object_or_404(HostingService, id=instance.object_id)
                    print hosting.pk
                    hosting.billingcycle = cycle_option
                    hosting.save()
                  else: 
                    cycle_option = service.billingcycle

              except Exception as ex:
                  template = "An exception of type {0} occured. Arguments:\n{1!r}"
                  message = template.format(type(ex).__name__, ex.args)
                  cycle_option = service.billingcycle
                  print message
              if cycle_option == 1:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 3*365/12) #verificar que la renovacion se haga en base a la fecha de ultima renovacion o bien del dia del pago si es nuevo servicio
              elif cycle_option == 2:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 6*365/12)
              elif cycle_option == 3:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 365)
              elif  cycle_option == 4:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 2*365)

              print next_renew
              HostingService.objects.filter(id=instance.object_id).update(next_renew=next_renew,last_renew=last_renewnow,status=2)

            #else if service.status ==4: #service cancel

          else: #si el pago es menor al precio del paquete
            #print "no corresponde "
            HostingService.objects.filter(id=instance.object_id).update(status=4)

        if instance.status == 3: # a continuacion checamos si el pago esta conflicto
          if service.status ==3: #si el servicio esta en expirado
            HostingService.objects.filter(id=instance.object_id).update(status=4)

        if instance.status == 4: #pago cancelado
          if service.status ==3: #si el servicio esta en expirado
            HostingService.objects.filter(id=instance.object_id).update(status=4)

        if instance.status == 5: #pago rembolsado
          print "rembolso"
          if service.status ==3: #si el servicio esta en expirado
            print "rembolso1"
            HostingService.objects.filter(id=instance.object_id).update(status=4)
          elif service.status ==2: #si el servicio esta activo
            print "rembolso2"
            HostingService.objects.filter(id=instance.object_id).update(status=4)


      if instance.content_type_id==23: #id de dominio #################         Domain         ##############
        print "pago dominio"
        service = DomainService.objects.get(id=instance.object_id)
        payments = PaymentNuevo.objects.filter(content_type_id=23,object_id=instance.object_id, status=2)
        tmount = 0
        for pay in payments:
          tmount = tmount + pay.mount #calculas el total sumando todos los pagos relacionados al servicio en caso de haber
        print service
        print "pago hosting"
        print instance.status
        if instance.status == 2: #Pago verificado
          actorid = str(instance.pk) #pk of payment instance
          actorob = 13 #pk of payment content type
          useractor = instance.user.user.pk #pk of user
          #Mark notification as unread when payment is verified
          Notification.objects.filter(recipient_id=useractor, actor_content_type=actorob, actor_object_id=actorid).update(unread=0)
          if tmount >= service.cycleprice: #precio coincide con pago
            if service.status ==1: #servicio pendiente
              print "service pendiente"
              try:
                  key, cycle = instance.description.split('-')
                  print key
                  if key == "renovar":
                    cycle_option = int(cycle)
                    hosting = get_object_or_404(DomainService, id=instance.object_id)
                    print hosting.pk
                    hosting.billingcycle = cycle_option
                    hosting.save()
                  else: 
                    cycle_option = service.billingcycle

              except Exception as ex:
                  template = "An exception of type {0} occured. Arguments:\n{1!r}"
                  message = template.format(type(ex).__name__, ex.args)
                  cycle_option = service.billingcycle
                  print message
              if cycle_option == 1:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days =365) #verificar que la renovacion se haga en base a la fecha de ultima renovacion o bien del dia del pago si es nuevo servicio
              elif cycle_option == 2:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 2*365)
              elif cycle_option == 3:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 3*365)
              elif  cycle_option == 4:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 4*365)

              print next_renew
              DomainService.objects.filter(id=instance.object_id).update(next_renew=next_renew,last_renew=last_renewnow,status=2)

            elif service.status ==2: #service active
              print "service active"
              try:
                  key, cycle = instance.description.split('-')
                  print key
                  if key == "renovar":
                    cycle_option = int(cycle)
                    hosting = get_object_or_404(DomainService, id=instance.object_id)
                    print hosting.pk
                    hosting.billingcycle = cycle_option
                    hosting.save()
                  else: 
                    cycle_option = service.billingcycle

              except Exception as ex:
                  template = "An exception of type {0} occured. Arguments:\n{1!r}"
                  message = template.format(type(ex).__name__, ex.args)
                  cycle_option = service.billingcycle
                  print message
              next = service.next_renew
              if cycle_option == 1:
                last_renewnow = timezone.now()
                next_renew = next + timedelta(days = 365) #verificar que la renovacion se haga en base a la fecha de ultima renovacion o bien del dia del pago si es nuevo servicio
              elif cycle_option == 2:
                last_renewnow = timezone.now()
                next_renew = next + timedelta(days = 2*365)
              elif cycle_option == 3:
                last_renewnow = timezone.now()
                next_renew = next + timedelta(days = 3*365)
              elif  cycle_option == 4:
                last_renewnow = timezone.now()
                next_renew = next + timedelta(days = 4*365)
              print next_renew
              DomainService.objects.filter(id=instance.object_id).update(next_renew=next_renew,last_renew=last_renewnow, status=2)

            elif service.status ==3: #service expired
              print "service expired"
              try:
                  key, cycle = instance.description.split('-')
                  print key
                  if key == "renovar":
                    cycle_option = int(cycle)
                    hosting = get_object_or_404(DomainService, id=instance.object_id)
                    print hosting.pk
                    hosting.billingcycle = cycle_option
                    hosting.save()
                  else: 
                    cycle_option = service.billingcycle

              except Exception as ex:
                  template = "An exception of type {0} occured. Arguments:\n{1!r}"
                  message = template.format(type(ex).__name__, ex.args)
                  cycle_option = service.billingcycle
                  print message
              if cycle_option == 1:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 365) #verificar que la renovacion se haga en base a la fecha de ultima renovacion o bien del dia del pago si es nuevo servicio
              elif cycle_option == 2:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 2*365)
              elif cycle_option == 3:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 3*365)
              elif  cycle_option == 4:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 4*365)

              print next_renew
              DomainService.objects.filter(id=instance.object_id).update(next_renew=next_renew,last_renew=last_renewnow,status=2)

            elif service.status ==4: #service conflict
              print "conflict service"
              try:
                  key, cycle = instance.description.split('-')
                  print key
                  if key == "renovar":
                    cycle_option = int(cycle)
                    hosting = get_object_or_404(DomainService, id=instance.object_id)
                    print hosting.pk
                    hosting.billingcycle = cycle_option
                    hosting.save()
                  else: 
                    cycle_option = service.billingcycle

              except Exception as ex:
                  template = "An exception of type {0} occured. Arguments:\n{1!r}"
                  message = template.format(type(ex).__name__, ex.args)
                  cycle_option = service.billingcycle
                  print message
              if cycle_option == 1:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 365) #verificar que la renovacion se haga en base a la fecha de ultima renovacion o bien del dia del pago si es nuevo servicio
              elif cycle_option == 2:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 2*365)
              elif cycle_option == 3:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 3*365)
              elif  cycle_option == 4:
                last_renewnow = timezone.now()
                next_renew = last_renewnow + timedelta(days = 4*365)

              print next_renew
              DomainService.objects.filter(id=instance.object_id).update(next_renew=next_renew,last_renew=last_renewnow,status=2)

            #else if service.status ==4: #service cancel

          else: #si el pago es menor al precio del paquete
            #print "no corresponde "
            DomainService.objects.filter(id=instance.object_id).update(status=4)

        if instance.status == 3: # a continuacion checamos si el pago esta conflicto
          if service.status ==3: #si el servicio esta en expirado
            DomainService.objects.filter(id=instance.object_id).update(status=4)

        if instance.status == 4: #pago cancelado
          if service.status ==3: #si el servicio esta en expirado
            DomainService.objects.filter(id=instance.object_id).update(status=4)

        if instance.status == 5: #pago rembolsado
          print "rembolso"
          if service.status ==3: #si el servicio esta en expirado
            print "rembolso1"
            DomainService.objects.filter(id=instance.object_id).update(status=4)
          elif service.status ==2: #si el servicio esta activo
            print "rembolso2"
            DomainService.objects.filter(id=instance.object_id).update(status=4)








