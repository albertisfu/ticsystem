
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
		for hosting in hostings:
			print hosting
			next = hosting.next_renew
			print next
			current_date = datetime.now()
			print current_date
			days = next - current_date
			print days.days
			hosting.days_left=days.days
			hosting.save()
		print "hello"


