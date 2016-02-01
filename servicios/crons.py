
from servicios.models  import HostingService, DomainService
from datetime import datetime
from django_cron import CronJobBase, Schedule
from django.shortcuts import render_to_response,get_object_or_404, render
from emailnoti.models import EmailTemplate
from django.core.mail import EmailMultiAlternatives

from django.template.loader import get_template
from django.template import Context

from django.utils import timezone


class ComputeDate(CronJobBase):
	RUN_EVERY_MINS = 1 # every 2 hours

	schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
	code = 'servicios.computer_date'    # a unique code

	def do(self): #do something, the cron must be call after set schedule time 
		hostings =  HostingService.objects.filter()
		domains =  DomainService.objects.filter()
		for hosting in hostings:
			next = hosting.next_renew
			current_date = timezone.now()
			days = next - current_date
			hosting.days_left=days.days
			hosting.save()

		for domain in domains:
			nextd = domain.next_renew
			current_dated = timezone.now()
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
		html30 = get_template('email.html')
		html15 = get_template('email15.html')
		html5 = get_template('email5.html')
		html1 = get_template('email1.html')
		html_10 = get_template('email-10.html')
		for hosting in hostings:	
			days_left = hosting.days_left
			usermail = hosting.user.email
			username = hosting.user.name
			description = hosting.name
			vigency = hosting.next_renew
			days = hosting.days_left
			cycle = hosting.billingcycle
			if cycle == 1:
				cycle ="Trimestral"
			elif  cycle == 2:
				cycle = "Semestral"
			elif cycle == 3:
				cycle = "Anual"
			elif cycle ==4:
				cycle = "Bianual"
			price = hosting.cycleprice
			plan = hosting.hostingpackage.name
			pk = hosting.pk
			d = Context({ 'username': username, 'description': description, 'vigency': vigency, 'days': days, 'cycle': cycle, 'price': price, 'plan': plan, 'pk':pk })
			print username
			print usermail
			print days_left
			if days_left == 30:
				html_content = html30.render(d)
				msg = EmailMultiAlternatives(
				subject="Renovacion - Su servicio vence en 30 dias",
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
				html_content = html15.render(d)
				msg = EmailMultiAlternatives(
				subject="Renovacion - Su servicio vence en 15 dias",
				body="Su servicio vence en 15 dias",
				from_email="Ticsup <contacto@serverticsup.com>",
				to=[username+" "+"<"+usermail+">"],
				headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
				)
				msg.attach_alternative(html_content, "text/html")
				# Optional Mandrill-specific extensions:
				# Send it:
				msg.send()
				print "15"

			elif days_left == 5:
				html_content = html5.render(d)
				msg = EmailMultiAlternatives(
				subject="Renovacion - Su servicio vence en 5 dias",
				body="Su servicio vence en 5 dias",
				from_email="Ticsup <contacto@serverticsup.com>",
				to=[username+" "+"<"+usermail+">"],
				headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
				)
				msg.attach_alternative(html_content, "text/html")
				# Optional Mandrill-specific extensions:
				# Send it:
				msg.send()
				print "5"

			elif days_left == 1:
				html_content = html1.render(d)
				msg = EmailMultiAlternatives(
				subject="Renovacion - Su servicio vence en 1 dia",
				body="Su servicio vence en 1 dia",
				from_email="Ticsup <contacto@serverticsup.com>",
				to=[username+" "+"<"+usermail+">"],
				headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
				)
				msg.attach_alternative(html_content, "text/html")
				# Optional Mandrill-specific extensions:
				# Send it:
				msg.send()
				print "1"

			elif days_left == -10:
				html_content = html_10.render(d)
				msg = EmailMultiAlternatives(
				subject="Servicio Expirado - Aun puede renovar",
				body="Su servicio tiene 10 dias de vencido, aun puede renovar",
				from_email="Ticsup <contacto@serverticsup.com>",
				to=[username+" "+"<"+usermail+">"],
				headers={'Reply-To': "Ticsup <contacto@serverticsup.com>"} # optional extra headers
				)
				msg.attach_alternative(html_content, "text/html")
				# Optional Mandrill-specific extensions:
				# Send it:
				msg.send()
				print "-10"


