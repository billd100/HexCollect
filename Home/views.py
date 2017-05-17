from datetime import timedelta
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone

from Experiences.models import Experience
from UserProfile.models import DailyCheckIn
from UserProfile.forms import DailyCheckInForm

def home_page(request):
	# false by default: if registered and no recent check-ins, serve check-in form
	check_in_form = False

	if request.user.is_authenticated():
		# filter by user, pub_date in last 12hrs
		recent_check_in = DailyCheckIn.objects.filter(user=request.user).filter(pub_date__gte=(timezone.now()-timedelta(0.5))).order_by('-pub_date')

		if not recent_check_in:
			# user has checked-in in last 12hrs, do not serve form
			check_in_form = DailyCheckInForm()

	experiences = Experience.objects.order_by('-pub_date')[:5]
	explorers = User.objects.order_by('-date_joined')[:5]
	date = timezone.now()
	
	context = {
		'check_in_form': check_in_form,
		'date': date,
		'experiences': experiences,
		'explorers': explorers,
	}
	return render(request, 'HexCollect/HexCollect.html', context)

def about(request):
	return render(request, 'HexCollect/about.html')
	
def user_agreement(request):
	return render(request, 'HexCollect/user_agreement.html')