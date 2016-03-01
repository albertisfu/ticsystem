from django import forms
from contents.models import *
from fileupload.models import *

class ContentForm(forms.ModelForm):
	file_ids = forms.CharField(required=False,widget=forms.HiddenInput(attrs={'class' : 'id_file_ids'}))
	dominio= forms.ChoiceField(widget=forms.Select(attrs={'class':'selector'}), choices=[(1, 'Si, ya cuento con dominio'), (2, 'No, deseo registrar un nuevo dominio')])
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
