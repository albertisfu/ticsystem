from django import forms
from models import *
from fileupload.models import *


class ContentForm(forms.ModelForm):
	file_ids = forms.CharField(required=False,widget=forms.HiddenInput())
	class Meta:
		model = Content
		exclude = ('proyect',)
		fields = ('empresa', 'giro', 'numbersections', 'file_ids')


	def save(self):
		media = super(ContentForm, self).save(commit=False)
		media.save()

		print self.instance.pk
		inst = self.instance
		file_ids = [x for x in self.cleaned_data.get('file_ids').split(',') if x]
		print file_ids
		for file_id in file_ids:
			print file_id  
			f = Picture.objects.get(id=file_id)
			a = LogoUpload(content=inst,attachment=f)
			a.save()


