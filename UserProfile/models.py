from __future__ import unicode_literals
from django.conf import settings

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from allauth import app_settings as allauth_app_settings

class UserProfile(models.Model):
	BLANK = ''
	FEMALE = 'Female'
	MALE = 'Male'
	SEX = (
		(BLANK, ''),
		(FEMALE, 'Female'),
		(MALE, 'Male'),
	)
	AMINDIAN_NALASKAN = 'Am. Indian, N. Alaskan'
	ASIAN = 'Asian'
	BLACK_AA = 'Black'
	PACIFIC_ISLANDER = 'Pacific Islander'
	WHITE = 'White'
	TWO_OR_MORE = 'Two or more'
	OTHER = 'Other'
	
	HISPANIC_OR_LATINO = 'Hispanic or Latino'
	
	RACE = (
		(BLANK, ''),
		(AMINDIAN_NALASKAN, 'Native American or Alaskan Native'),
		(ASIAN, 'Asian'),
		(BLACK_AA, 'Black or African American'),
		(PACIFIC_ISLANDER, 'Native Hawaiian or other Pacific Islander'),
		(WHITE, 'White'),
		(TWO_OR_MORE, 'Two or more races'),
		(OTHER, 'Other'),
	)
	
	ETHNICITY = (
		(BLANK, ''),
		(HISPANIC_OR_LATINO, 'Hispanic or Latino'),
		('Not Hispanic or Latino', 'Not Hispanic or Latino'),
	)
	user = models.OneToOneField(User)
	
	birthday = models.DateField(blank=True, null=True )
	sex = models.CharField(choices=SEX, max_length=50, default=BLANK, blank=True)
	gender_identity = models.CharField(max_length=50, blank=True)
	ethnicity = models.CharField(choices=ETHNICITY, max_length=25, default=BLANK, blank=True)
	race = models.CharField(choices=RACE, max_length=50, default=BLANK, blank=True)
	about = models.TextField(max_length=1000, blank=True, verbose_name="Tell the community about yourself")
	
	def get_absolute_url(self):
		return reverse('user_profile:profile', args=[request.user.user_name])
	
	def __str__(self):
		return self.user
	
	class Meta:
		db_table = 'UserProfile'


STATES_OF_BEING = (
	('excellent', 'excellent'),
	('good', 'good'),
	('neutral', 'neutral'),
	('poor', 'poor'),
	('abysmal', 'abysmal'),
)

class DailyCheckIn(models.Model):
	status = models.CharField(max_length=20, choices=STATES_OF_BEING)
	status_detail = models.CharField(max_length=1000, blank=True)

	pub_date = models.DateTimeField(
		auto_now_add=True)
	
	user = models.ForeignKey(User)
	
	class Meta:
		db_table = 'userprofile.dailycheckin'

from django.db.models.signals import post_save

# when a user signs up, a UserProfile is automatically created for them
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		new_user_profile = UserProfile.objects.create(user=instance)
post_save.connect(create_user_profile, sender=User)


		
'''
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		profile, new = UserProfile.objects.get_or_create(user=instance)
'''
