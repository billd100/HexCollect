from __future__ import unicode_literals
from django import forms
from django.forms import Textarea
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.utils.text import slugify

BLANK = ''

DAY = 'day'
WEEK = 'week'
MONTH = 'month'
YEAR = 'year'

MINUTES = 'minutes'
HOURS = 'hours'

COLONY_FORMING_UNIT = 'CFU'
FLUID_OUNCE = 'fl oz'
GRAM = 'g'
INTERNATIONAL_UNIT = 'IU'
MICROGRAM = 'ug'
MILLIGRAM = 'mg'
MILLILITER = 'mL'
OUNCE = 'oz'
TEASPOON = 'tsp'
TABLESPOON = 'Tbsp'


FREQUENCY_TIME_UNITS = (
	(BLANK, ''),
	(DAY, 'per day'),
	(WEEK, 'per week'),
	(MONTH, 'per month'),
	(YEAR, 'per year'),
)

DURATION_TIME_UNITS = (
	(BLANK, ''),
	(DAY, 'days'),
	(WEEK, 'weeks'),
	(MONTH, 'months'),
	(YEAR, 'years'),
)

EXERCISE_TIME_UNITS = (
	(BLANK, ''),
	(MINUTES, 'minutes'),
	(HOURS, 'hours'),
)

DOSAGE_UNITS = (
	(BLANK, ''),
	(COLONY_FORMING_UNIT, 'CFU'),
	(FLUID_OUNCE, 'fl oz'),
	(GRAM, 'g'),
	(INTERNATIONAL_UNIT, 'IU'),
	(MICROGRAM, 'ug'),
	(MILLIGRAM, 'mg'),
	(MILLILITER, 'mL'),
	(OUNCE, 'oz'),
	(TABLESPOON, 'Tbsp'),
	(TEASPOON, 'tsp'),
)

class Experience(models.Model):

	intervention = models.CharField(max_length=30, verbose_name="Name of Intervention")
	
	brand = models.CharField(max_length=30, verbose_name='Is this intervention associated with a particular brand?', blank=True)

	purpose = models.CharField(max_length=100, verbose_name="Purpose of Intervention")

	details = models.CharField(max_length=5000)
	
	effectiveness = models.PositiveSmallIntegerField(verbose_name="Overall effectiveness")

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	
	slug = models.SlugField(max_length=30, unique=False)
	
	pub_date = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	# check first if slug field exists (in case of updating/edit)
	def save(self, *args, **kwargs):
		if not self.slug or self.slug != slugify(self.intervention):
			self.slug = slugify(self.intervention)
		super(Experience, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('experiences:experience_detail_slug', args=[self.id, self.slug])

	def __str__(self):
		return self.intervention + ' by ' + self.user.username

	class Meta:
		db_table = 'experiences'
		
	# table already exists: db_table name cannot conflict with app name!
	
class Dose(models.Model):

	dose_value = models.CharField(max_length= 15, verbose_name='What dosage did you take?', blank=True)
	
	dose_unit = models.CharField(max_length=5, choices=DOSAGE_UNITS, default=BLANK, verbose_name='Dosage unit', blank=True)
	
	dose_frequency = models.PositiveSmallIntegerField(verbose_name='How often was the dosage above taken?', blank=True, null=True)
	
	dose_frequency_unit = models.CharField(max_length=9, choices=FREQUENCY_TIME_UNITS, default=BLANK, verbose_name='Dosage frequency unit', blank=True)
	
	dose_duration = models.PositiveSmallIntegerField(verbose_name='How long did you take the product?', blank=True, null=True)
	
	dose_duration_unit = models.CharField(max_length=5, choices=DURATION_TIME_UNITS, default=BLANK, verbose_name='Duration unit', blank=True)
	
	experience = models.ForeignKey(Experience, related_name="doses")
	
	def __str__(self):
		return 'dose_information'

class Symptom(models.Model):
	
	symptom_name = models.CharField(max_length=20, verbose_name="What symptoms were you addressing?", blank=True)
	pre_intervention = models.PositiveSmallIntegerField(verbose_name="before", blank=True, null=True)
	post_intervention = models.PositiveSmallIntegerField(verbose_name="after", blank=True, null=True)
	
	experience = models.ForeignKey(Experience, related_name="symptoms")

	def __str__(self):
		return self.symptom_name

class ExperienceUpdate(models.Model):
	update = models.CharField(max_length=1000)
	experience = models.ForeignKey(Experience)
	user = models.ForeignKey(User)

	pub_date = models.DateTimeField(auto_now_add=True)

class ExperienceSearch(models.Model):
	search_terms = models.CharField(max_length=100)
	
	user = models.ForeignKey(User)
	