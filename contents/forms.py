from django import forms
from models import *
from fileupload.models import *
from ckeditor.widgets import CKEditorWidget

class ContentForm(forms.ModelForm):
	file_ids = forms.CharField(required=False,widget=forms.HiddenInput(attrs={'class' : 'id_file_ids'}))
	dominio= forms.ChoiceField(required=False,widget=forms.Select(attrs={'class':'selector'}), choices=[(1, 'Si, ya cuento con dominio'), (2, 'No, deseo registrar un nuevo dominio')])
	class Meta:
		model = Content
		exclude = ('proyect',)
		fields = ('empresa', 'giro', 'file_ids')
		labels = {
            'empresa': ('Nombre de su Empresa o Proyecto'),
            'giro': ('Giro de su Empresa'),
        }

	def save(self, commit=True):
		media = super(ContentForm, self).save(commit=False)
		if commit:
			media.save()
			print self.instance.pk
			inst = self.instance
			file_ids = [x for x in self.cleaned_data.get('file_ids').split(',') if x]
			print file_ids
			if self.instance.pk:
				for file_id in file_ids:
					print file_id  
					f = Picture.objects.get(id=file_id)
					a = LogoUpload(content=inst,attachment=f)
					a.save()
		return media



class SectionForm(forms.ModelForm):
	file_ids = forms.CharField(required=False,widget=forms.HiddenInput(attrs={'class' : 'id_file_ids'}))
	
	class Meta:
		model = Section
		exclude = ('content',)
		fields = ('name', 'text', 'coment', 'file_ids')
		labels = {
            'name': ('Seccion'),
            'text': ('Contenido'),
            'coment': ('Comentarios para el desarrollador'),
        }
	text = forms.CharField(widget=CKEditorWidget(config_name='text'), label="Contenido", required=False)

	def save(self, commit=True):
		media = super(SectionForm, self).save(commit=False)
		if commit:
			media.save()
			print self.instance.pk
			inst = self.instance
			file_ids = [x for x in self.cleaned_data.get('file_ids').split(',') if x]
			print file_ids
			for file_id in file_ids:
				print file_id  
				f = Picture.objects.get(id=file_id)
				a = FilesUpload(section=inst,attachment=f)
				a.save()
		return media

