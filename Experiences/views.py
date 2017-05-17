from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.utils import timezone

import django_comments

from Experiences.forms import ExperienceForm, DoseForm, SymptomForm, ExperienceUpdateForm, ExperienceSearchForm
from Experiences.models import Experience, Dose, Symptom, ExperienceUpdate
from UserProfile.models import UserProfile

# functions use lowercase convention with underscore separations

def experiences(request):
	experiences = Experience.objects.order_by('-pub_date')[:5]
	experience_search = ExperienceSearchForm()
	context = {
		'experiences': experiences,
		'experience_search': experience_search,
	}
	return render(request, 'Experiences/experiences.html', context)

def share_experience(request):
	experience_form = ExperienceForm(request.POST or None)
	dose_form = DoseForm(request.POST or None)
	SymptomFormSet = modelformset_factory(Symptom, form=SymptomForm, max_num=10, can_delete=True)
	
	if request.method == 'POST':
		symptom_formset = SymptomFormSet(request.POST)
		if dose_form.is_valid() and symptom_formset.is_valid() and experience_form.is_valid():
			valid_experience_form = experience_form.save(commit=False)
			valid_experience_form.user = request.user
			valid_experience_form.save()
	
			valid_dose = dose_form.save(commit=False)
			valid_dose.experience = valid_experience_form
			valid_dose.save()

			symptom_instances = symptom_formset.save(commit=False)
			for instance in symptom_instances:
				instance.experience = valid_experience_form
				instance.save()
			# TODO: redirect to/render experiences:detail with banner: 'update or edit at anytime'
			return HttpResponseRedirect(reverse('experiences:experience_detail_slug', args=[valid_experience_form.id, valid_experience_form.slug]))

	symptom_formset = SymptomFormSet(queryset=Symptom.objects.none())
	context = {
		'experience_form': experience_form,
		'dose_form': dose_form,
		'symptom_formset': symptom_formset,
	}
	return render(request, 'Experiences/add.html', context)

# could combine with add_experience with get_object_or_404: need to consider that experience exists already
def edit_experience(request, id=None):

	experience = get_object_or_404(Experience, id=id)
	# I believe this shortcuts necessitates blank doses for each experience
	doses = get_list_or_404(Dose, experience=experience)

	if experience.user == request.user: # only owner may edit
		experience_form = ExperienceForm(request.POST or None, instance=experience)	
		dose_form = DoseForm(request.POST or None, instance=doses[0])
		
		SymptomFormSet = modelformset_factory(Symptom, form=SymptomForm, max_num=10, can_delete=True, extra=1)

		if request.method == 'POST':
			symptom_formset = SymptomFormSet(request.POST)
			# check if all forms are valid
			if dose_form.is_valid() and symptom_formset.is_valid() and experience_form.is_valid():
				valid_experience_form = experience_form.save()
				valid_dose_form = dose_form.save()
				
				# objects not deleted automatically with commit=False
				valid_symptom_formset = symptom_formset.save(commit=False)
				
				for symptom in symptom_formset.deleted_objects:
					symptom.delete()
				for symptom in symptom_formset.new_objects:				
					symptom.experience = valid_experience_form
				
				for symptom in valid_symptom_formset:
					symptom.save()
				
				return HttpResponseRedirect(reverse('experiences:experience_detail_slug', args=[valid_experience_form.id, valid_experience_form.slug]))
		else:
			formset_length = len(Symptom.objects.filter(experience=experience))
			symptom_formset = SymptomFormSet(queryset=Symptom.objects.filter(experience=experience))
			
			experience_update_form = ExperienceUpdateForm()
			context = {
				'experience': experience,
				'dose_form': dose_form,
				'symptom_formset': symptom_formset,
				'experience_form': experience_form,
				'experience_update_form': experience_update_form,
			}
			return render(request, 'Experiences/edit.html', context)
	else:
		return HttpResponseRedirect(reverse('experiences:experience_detail_slug', args=[experience.id, experience.slug]))

def update_experience(request, id=None):
	experience = get_object_or_404(Experience, id=id)
	if experience.user == request.user:
		experience_form = ExperienceForm(instance=experience)
		experience_update_form = ExperienceUpdateForm(request.POST or None)
		if experience_update_form.is_valid():
			valid_form = experience_update_form.save(commit=False)
			valid_form.experience = experience
			valid_form.user = request.user
			valid_form.save()
			return HttpResponseRedirect(reverse('experiences:experience_detail_slug', args=[experience.id, experience.slug]))
			
		context = {
			'experience_update_form': experience_update_form,
		}
		return render(request, 'Experiences/edit.html', context)
	else:
		return HttpResponseRedirect(reverse('experiences:experience_detail_slug', args=[experience.id, experience.slug]))


from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
def activity(request, page=None):
	exp_list = Experience.objects.order_by('-pub_date')[5:85]
	paginator = Paginator(exp_list, 8) # 8 exps/page

	try:
		experiences = paginator.page(page)
	except PageNotAnInteger:
		experiences = paginator.page(1)
	except EmptyPage:
		# page out of range, deliver last page
		experiences = paginator.page(paginator.num_pages)
	return render(request, 'EXPERIENCES/activity.html', {'experiences': experiences})
	
def experience_detail(request, id=None, slug=None):
	experience = get_object_or_404(Experience, id=id)
	# calculate time elapsed since post
	time_elapsed = calculate_time_elapsed(experience.pub_date)

	# if there are no updates, template will not render update elements
	if ExperienceUpdate.objects.filter(experience=experience).exists():
		experience_updates = ExperienceUpdate.objects.filter(experience=experience)
	else:
		experience_updates = False
	# if there are no updates, update div will not appear in detail view	

	context = {
		'experience': experience,
		'experience_updates': experience_updates,
		'time_elapsed': time_elapsed,
	}
	return render(request, 'Experiences/detail.html', context)

from django.db.models import Q
def experience_search(request):
	experiences = Experience.objects.filter(
		Q(intervention__contains=request.GET['search_terms']) 
		| Q(purpose__contains=request.GET['search_terms']) 
		| Q(symptoms__contains=request.GET['search_terms']))
	context = {
		'experiences': experiences,
	}
	return render(request, 'Experiences/search.html', context)


@login_required
def delete_own_comment(request, message_id):
	comment = get_object_or_404(django_comments.get_model(), pk=message_id)
	experience = get_object_or_404(Experience, pk=comment.object_pk)
	if comment.user == request.user:
		comment.is_removed = True
		comment.save()
	return HttpResponseRedirect(reverse('experiences:experience_detail_slug', args=[experience.id, experience.slug]))


from datetime import datetime
def calculate_time_elapsed(pub_date):
	time = timezone.now()
	elapsed = time - pub_date
	
	# 1 day to 1 year, return days
	if elapsed.days < 1:
		if elapsed.seconds < 60:
			if elapsed.seconds == 1:
				return '1 second ago'
			else:
				return '%s seconds ago' % (int(elapsed.seconds))
		elif elapsed.seconds < 3600: # 1 hour
			if elapsed.seconds < 120:
				return '1 minute ago'
			else:
				return '%s minutes ago' % (int(elapsed.seconds/60))
		else:
			if elapsed.seconds < 7200: # 2 hours
				if elapsed.seconds/60%60 == 1:
					return '1 hour, 1 minute ago'
				else:
					return '1 hour, %s minutes ago' % (int(elapsed.seconds/60%60))
			elif elapsed.seconds/60%60 == 1:
				return '%s hours, 1 minute ago' % (int(elapsed.seconds/3600))
			else:
				return '%s hours, %s minutes ago' % (int(elapsed.seconds/3600), int(elapsed.seconds/60%60))
		
	elif elapsed.days > 0 and elapsed.days < 365:
		if elapsed.days == 1:
			return '1 day ago'
		else:
			return '%s days ago' % (int(elapsed.days))
	elif elapsed.days > 364:
		if elapsed.days == 365:
			return '1 year ago'
		elif elapsed.days%365 == 1:
			return '%s years, 1 day ago' % (int(elapsed.days/365))
		else:
			return '%s years, %s days ago' % (int(elapsed.days/365), int(elapsed.days%365))
