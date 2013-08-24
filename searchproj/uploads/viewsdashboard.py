'''
Created on Nov 21, 2012

@author: rise
'''
# stdlib imports

# core django imports
from django.shortcuts import render_to_response
from django.template import RequestContext

# 3rd party imports

# project imports
from .models import Submission
from profiles.models import UserProfile

def getDashboard(request):	
	'''navigate to dashboard after user authenticates into site'''
	try: 
		# get number of submissions by logged in user
		logged_in_user = UserProfile.objects.get(user=request.user)
		logged_in_user_submissions = Submission.objects.all().order_by('-id').filter(user=logged_in_user)
		#recentSub = logged_in_user_submissions.latest('id').revision_set.all().latest('modified').modified
		return render_to_response('accounts/dashboard_master.html', { 'vids': logged_in_user_submissions }, context_instance=RequestContext(request)) 
	except Exception as e: 
		print e
		import traceback, sys
		traceback.print_exc(file=sys.stdout)
		