
from servicios.models  import HostingService, DomainService
from datetime import datetime
from django_cron import CronJobBase, Schedule
from django.shortcuts import render_to_response,get_object_or_404, render
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


