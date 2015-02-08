from django.db import models
from postman.models import *
from fileupload.models import *


class Attachment(models.Model):
	message = models.ForeignKey(Message)
	attachment = models.ForeignKey(Picture)

	def __unicode__(self):
		return str(self.message) + self.attachment.__unicode__()


