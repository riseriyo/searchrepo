'''
Created on Nov 21, 2012

@author: rise
'''
# stdlib imports
#import pdb
import os
import traceback
import sys
import logging
import pdb

# core django imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test

# 3rd party apps

# project's imports
from .formssubmission import SubmissionForm
from .formssubmission import FiletypeForm
from .formssubmission import DefaultRevisionForm
from .models import Submission
from .models import Revision
from .models import Filetype
from profiles.models import UserProfile

VALIDMIMES = [
			'text/plain',
			'application/octet-stream',
			'application/xml',
			'application/pdf',
			'application/zip',
			'inode/directory',
			'application/vnd.openxmlformats-officedocument.presentationml.presentation',
			'text/plain',
			'image/x-xcf',
			'application/postscript',
			'image/vnd.adobe.photoshop',
			'video/quicktime',
			'video/mp4',
			'video/x-msvideo',
			'video/x-ms-asf',
			'video/avi',
			'video/mov',
]

def user_can_upload(user):
	return user.is_authenticated() and user.is_active
				
@user_passes_test(user_can_upload, login_url="/login/")
def createSubmission(request):	
	'''create new Submission and default Revision objects'''
	new_submission = Submission()
	default_revision = Revision()
	if request.method == 'POST': #and request.is_ajax():
		#pdb.set_trace()
		# create 3 form instances for 3 model objects, collect POST data for each object; 
		# bound data to form instances
		subform = SubmissionForm(request.POST, instance=new_submission) 
		ftform = FiletypeForm(request.POST)
		revform = DefaultRevisionForm(request.POST, request.FILES)
		logging.info("%s POST and %s FILES" %(request.POST, request.FILES))
		logged_in_user = UserProfile.objects.get(user=request.user)
		
		# is_valid() checks to see if data is clean for both form instance and model instance and saves data to instances
		if subform.is_valid() and ftform.is_valid() and revform.is_valid(): # 
			#pdb.set_trace()
			try:
				default_revision.save() # save instance Revision object in db
				new_submission = subform.save(commit=False)
				new_submission.user = logged_in_user
				new_submission.filetype= ftform.cleaned_data['filetype'] #already cleaned in formsubmission.py
				new_submission.save()
				# save uploaded files into revision object, db and locally to "uploaded_to" designation
				#default_revision.save() # save to db, for saving uploads to local file system path
				#revform.save()
				
				# submission object always has 
				# FK in Revision, related to Submission instance and UserProfile instance
				default_revision.submission = new_submission
				default_revision.user = logged_in_user
				default_revision.comments = ''
				
				# checked file size, mime types in header not sent by browser, and included extension.
				# NOTE: ImageField automatically validates if file is a valid image file
				default_revision.sourcefile=revform.cleaned_data['sourcefile'] #request.FILES['sourcefile']
				
				# user does not upload video nor thumbnail file; for thumbnail use generic filetype
				if request.FILES.get('vidanimation') is None:
					default_revision.vidanimation = None
				else:
					default_revision.vidanimation=request.FILES['vidanimation']
				if request.FILES.get('vidpic') is None:
					try:
						logging.info(Filetype.objects.get(pk=request.POST.get('filetype')).filetype.split('.')[2])
						extension = Filetype.objects.get(pk=request.POST.get('filetype')).filetype.split('.')[2]
					except:
						logging.info(Filetype.objects.get(pk=request.POST.get('filetype')).filetype.split('.')[1])
						extension = Filetype.objects.get(pk=request.POST.get('filetype')).filetype.split('.')[1]
					default_revision.vidpic = os.path.join('icons','generic-icon-1024x576-' + extension + '.png')
				else:
					default_revision.vidpic=request.FILES['vidpic']
				default_revision.save()
				
			except Exception as e: 
				print e
				traceback.print_exc(file=sys.stdout)
			finally:
				# get number of and list of submissions for current user
				#logged_in_user = UserProfile.objects.get(user=request.user)
				vidCount = Submission.objects.filter(user=logged_in_user).count()
				logged_in_user_submissions = Submission.objects.filter(user=logged_in_user).order_by('-id')
				# view all revisions for a given submission
				#latestSub = logged_in_user_submissions.latest('id')
				#latestRev = Submission.objects.get(pk=latestSub.pk).revision_set.reverse()[:1][0].published
				context = { 'vidCount': vidCount, 'vids': logged_in_user_submissions } #, 'latestRev': latestRev }
				return render_to_response('accounts/uploads_manager.html', context, context_instance=RequestContext(request))

		else:
			# form not valid, try again
			context = { 'subform': subform, 'ftform': ftform, 'revform': revform  } #'ontforms': ontforms, 
			return render_to_response('accounts/submission_form.html', context, context_instance=RequestContext(request))
		
	else:
		'''user is not submitting the form, show them a blank registration form'''
		# unbound form, it cannot do validation, renders a blank form as HTML
		subform = SubmissionForm(instance=new_submission)
		ftform  = FiletypeForm()
		revform = DefaultRevisionForm(instance=default_revision)

		# add form to context
		context = { 'subform': subform, 'ftform': ftform, 'revform': revform, 'user': request.user }
		return render_to_response('accounts/submission_form.html', context, context_instance=RequestContext(request))
