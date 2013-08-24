'''
Created on Nov 21, 2012

@author: rise
'''
# stdlib imports
#import pdb

# core django imports
#from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test

# 3rd party imports
#from easy_thumbnails.files import get_thumbnailer

# project imports
from uploads.models import Submission
from profiles.models import UserProfile

def user_can_upload(user):
	return user.is_authenticated() and user.is_active

@user_passes_test(user_can_upload, login_url="/login/")
def uploadsManager(request):	
	'''Display a list of animation submissions for an authenticated user'''
	try: 
		#pdb.set_trace()
		logged_in_user = UserProfile.objects.get(user=request.user)
		vidCount = Submission.objects.filter(user=logged_in_user).count()
		logged_in_user_submissions = Submission.objects.filter(user=logged_in_user).order_by('-id')
		#latestSub = logged_in_user_submissions.latest('id')
		#latestRev = Submission.objects.get(pk=latestSub.pk).revision_set.reverse()[:1][0].published
		return render_to_response('accounts/uploads_manager.html', { 'vidCount': vidCount, 'vids': logged_in_user_submissions }, context_instance=RequestContext(request)) #, 'latestRev': latestRev 
	except Exception as e: 
		print e
		import traceback, sys
		traceback.print_exc(file=sys.stdout)
