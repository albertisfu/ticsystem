from django import forms
from models import *
from fileupload.models import *
from ckeditor.widgets import CKEditorWidget

class ContentForm(forms.ModelForm):
	file_ids = forms.CharField(required=False,widget=forms.HiddenInput())
	class Meta:
		model = Content
		exclude = ('proyect',)
		fields = ('empresa', 'giro', 'numbersections', 'file_ids')


	def save(self, commit=True):
		media = super(ContentForm, self).save(commit=False)
		if commit:
			media.save()
		#print self.instance.pk
		inst = self.instance
		file_ids = [x for x in self.cleaned_data.get('file_ids').split(',') if x]
		#print file_ids
		for file_id in file_ids:
			#print file_id  
			f = Picture.objects.get(id=file_id)
			a = LogoUpload(content=inst,attachment=f)
			a.save()
		return media



class SectionForm(forms.ModelForm):
	file_ids = forms.CharField(required=False,widget=forms.HiddenInput(attrs={'class' : 'id_file_ids'}))
	
	class Meta:
		model = Section
		exclude = ('content',)
		fields = ('name', 'text', 'content', 'coment', 'file_ids')
	text = forms.CharField(widget=CKEditorWidget(config_name='text'))

	def save(self, commit=True):
		media = super(SectionForm, self).save(commit=False)
		if commit:
			media.save()
		#print self.instance.pk
		inst = self.instance
		file_ids = [x for x in self.cleaned_data.get('file_ids').split(',') if x]
		#print file_ids
		for file_id in file_ids:
			print file_id  
			f = Picture.objects.get(id=file_id)
			a = FilesUpload(section=inst,attachment=f)
			a.save()
		return media

