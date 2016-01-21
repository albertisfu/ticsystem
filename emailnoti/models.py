from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.


class EmailTemplate(models.Model):
  name = models.CharField(max_length = 255)
  description = models.TextField()
  text = RichTextField(config_name='text')
  
  def __unicode__(self):
    return self.name