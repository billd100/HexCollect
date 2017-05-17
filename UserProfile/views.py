from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import csrf

from Experiences.models import Experience, Dose, Symptom
from UserProfile.models import UserProfile, DailyCheckIn
from UserProfile.forms import GeneralProfileForm, DailyCheckInForm

@login_required(redirect_field_name=None)
def update_profile(request):
	user_profile = get_object_or_404(UserProfile, user=request.user)

	if request.method == 'POST':
		general_form = GeneralProfileForm(request.POST, instance=user_profile)
		if general_form.is_valid():
			general_form.save()
			return HttpResponseRedirect(reverse('userprofile:profile', args=[request.user.username]))

	general_profile_form = GeneralProfileForm(initial={'birthday':user_profile.birthday, 'sex':user_profile.sex, 'gender_identity': user_profile.gender_identity, 'ethnicity': user_profile.ethnicity, 'race':user_profile.race, 'about':user_profile.about})
	
	context = {
		'form': general_profile_form,
	}
	return render(request, 'UserProfile/update_profile.html', context)

import json
def condition(request):
	if request.method == 'POST':
		condition = request.POST.get('condition')
		response_data = {}
		
		condition_list = HealthProfileForm({'conditions': condition})

		response_data['condition'] = condition.conditions
		
		return HttpResponse(json.dumps(reponse_data), content_type="application/json")
		
	else:
		return HttpResponse(json.dumps({"Unable to add" : "Could not add condition"}), content_type="application/json")

def profile(request, user_name):
	# check if requested user has registered an account
	if User.objects.filter(username=user_name).exists():
		current_user = User.objects.get(username=user_name)
		user_profile = UserProfile.objects.get(user=current_user)
		
		# specific user's experiences
		experiences = Experience.objects.filter(user=current_user).order_by('-pub_date')[:5]
		daily_check_ins = DailyCheckIn.objects.filter(user=current_user).order_by('-pub_date')[:5]
		
		
		# if the user has provided a birthday, calculate their age
		if user_profile.birthday:
			user_age = calculate_age(user_profile.birthday)
		else:
			user_age = None
		context = {
			'user_profile': user_profile,
			'user_name': user_name,
			'experiences': experiences,
			'user_age': user_age,
			'daily_check_ins': daily_check_ins,
		}
	
	# user does not exist: profile.html displays '{{ url_user }} DNE'
	else:
		context = {
			'url_user': user_name,
		}
	return render(request, 'UserProfile/profile.html', context)

def journal(request, username):
	check_in_form = DailyCheckInForm(request.POST or None)
	if check_in_form.is_valid():
		valid_form = check_in_form.save(commit=False)
		valid_form.user = request.user
		valid_form.save()
		return HttpResponseRedirect(reverse('hexcollect:hexcollect'))
	
	current_user = get_object_or_404(User, username=username)
	user_profile = UserProfile.objects.get(user=current_user)
	daily_check_ins = DailyCheckIn.objects.filter(user=current_user).order_by('-pub_date')
	context = {
		'user_profile': user_profile,
		'check_in_form': check_in_form,
		'daily_check_ins': daily_check_ins,
	}

	return render(request, 'UserProfile/journal.html', context)

# calculate users age from their given birthday
from datetime import date
def calculate_age(birthday):
	today = date.today()
	return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
