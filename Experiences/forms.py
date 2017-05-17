from django import forms
from django.forms import ModelForm, Textarea, ChoiceField
from Experiences.models import Dose, Symptom, Experience, ExperienceUpdate, ExperienceSearch
	
class ExperienceForm(ModelForm):
	class Meta:
		model = Experience
		fields = (
			'intervention',
			'brand',
			'purpose',
			'details',
			'effectiveness',
		)
		
		help_texts = {
			# 'name': ('A supplement name could be "vitamin D" or "probiotic"'),
		}
		widgets = {
			'details': forms.Textarea(attrs={'cols': 10, 'rows': 8}),
			'effectiveness': forms.NumberInput(attrs={'placeholder': '0-100'}),
		}

class DoseForm(ModelForm):
	class Meta:
		model = Dose
		fields = (
			'dose_value',
			'dose_unit',
			'dose_frequency',
			'dose_frequency_unit',
			'dose_duration',
			'dose_duration_unit',
		)

class SymptomForm(ModelForm):
	class Meta:
		model = Symptom
		fields = (
			'symptom_name',
			'pre_intervention',
			'post_intervention',
		)

		widgets = {
			'symptom_name': forms.TextInput(attrs={'placeholder': 'Symptom'}),
			'pre_intervention': forms.NumberInput(attrs={'placeholder': '0-100'}),
			'post_intervention': forms.NumberInput(attrs={'placeholder': '0-100'}),
		}

class ExperienceUpdateForm(ModelForm):
	class Meta:
		model = ExperienceUpdate
		fields = (
			'update',
		)
		widgets = {
			'update': forms.Textarea(attrs={'rows': 4})
		}

class ExperienceSearchForm(ModelForm):
	class Meta:
		model = ExperienceSearch
		fields = (
			'search_terms',
		)
		widgets = {
			'search_terms': forms.TextInput(attrs={'placeholder': 'Search Experiences'})
		}
