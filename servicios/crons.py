
from servicios.models  import HostingService, DomainService
from datetime import datetime
from django_cron import CronJobBase, Schedule
from django.shortcuts import render_to_response,get_object_or_404, render
from emailnoti.models import EmailTemplate
from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template
from django.template import Context

class ComputeDate(CronJobBase):
	RUN_EVERY_MINS = 1 # every 2 hours

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'servicios.computer_date'    # a unique code

	def do(self): #do something, the cron must be call after set schedule time 
		hostings =  HostingService.objects.filter()
		domains =  DomainService.objects.filter()
		for hosting in hostings:
			next = hosting.next_renew
			current_date = datetime.now()
			days = next - current_date
			hosting.days_left=days.days
			hosting.save()

		for domain in domains:
			nextd = domain.next_renew
			current_dated = datetime.now()
			daysd = nextd - current_dated
			domain.days_left=daysd.days
			domain.save()

		print "hello"


class NotifyEmail(CronJobBase):
	RUN_EVERY_MINS = 1 # one minute
	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'servicios.notify_email'    # a unique code
	def do(self):
		hostings =  HostingService.objects.filter()
		domains =  DomainService.objects.filter()
		print "entro"
		#text30 = get_object_or_404(EmailTemplate, pk = 1)
		#html30 = text30.text
		htmly = get_template('email.html')
		for hosting in hostings:
			print "entrofor"
			days_left = hosting.days_left
			usermail = hosting.user.email
			username = hosting.user.name
			d = Context({ 'username': username })
			html_content = htmly.render(d)
			print username
			print usermail
			print days_left
			if days_left == 30:
				msg = EmailMultiAlternatives(
				subject="Renovacion Servicio",
				body="Su servicio vence en 30 dias",
				from_email="Ticsup <contacto@serverticsup.com>",
				to=[username+" "+"<"+usermail+">"],
				headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
				)
				msg.attach_alternative(html_content, "text/html")
				# Optional Mandrill-specific extensions:
				# Send it:
				msg.send()
				print "30"


			elif days_left == 15:
				msg = EmailMultiAlternatives(
				subject="Renovacion Servicio",
				body="Su servicio vence en 15 dias",
				from_email="Ticsup <contacto@serverticsup.com>",
				to=[username+" "+"<"+usermail+">"],
				headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
				)
				msg.attach_alternative("<p>Su servicio vence en 15 dias</p>", "text/html")
				# Optional Mandrill-specific extensions:
				# Send it:
				msg.send()
				print "15"

			elif days_left == 5:
				msg = EmailMultiAlternatives(
				subject="Renovacion Servicio",
				body="Su servicio vence en 5 dias",
				from_email="Ticsup <contacto@serverticsup.com>",
				to=[username+" "+"<"+usermail+">"],
				headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
				)
				msg.attach_alternative("<p>Su servicio vence en 5 dias</p>", "text/html")
				# Optional Mandrill-specific extensions:
				# Send it:
				msg.send()
				print "5"

			elif days_left == 1:
				msg = EmailMultiAlternatives(
				subject="Renovacion Servicio",
				body="Su servicio vence en 1 dia",
				from_email="Ticsup <contacto@serverticsup.com>",
				to=[username+" "+"<"+usermail+">"],
				headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
				)
				msg.attach_alternative("<p>Su servicio vence en 1 dias</p>", "text/html")
				# Optional Mandrill-specific extensions:
				# Send it:
				msg.send()
				print "1"

			elif days_left == -10:
				msg = EmailMultiAlternatives(
				subject="Renovacion Servicio",
				body="Su servicio tiene 10 dias de vencido, aun puede renovar",
				from_email="Ticsup <contacto@serverticsup.com>",
				to=[username+" "+"<"+usermail+">"],
				headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
				)
				msg.attach_alternative("<p>Su servicio tiene 10 dias de vencido, aun puede renovar</p>", "text/html")
				# Optional Mandrill-specific extensions:
				# Send it:
				msg.send()
				print "-10"


