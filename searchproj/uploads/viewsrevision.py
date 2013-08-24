'''
Created on Jan 3, 2013

@author: rise
'''
# stdlib imports
#import datetime
import sys
import traceback
#import pdb

# core django imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
#from django.utils.timezone import utc
from django.contrib import messages

# 3rd party imports

# project imports
from .formsrevision import SubmissionForm
from .formsrevision import RevisionForm
from .formsrevision import FiletypeForm
from .models import Submission
from .models import Revision
from .models import Filetype
from profiles.models import UserProfile

FILETYPES = [
				('10', '.blend (Blender)'),
				('20', '.ma/.mb (Maya)'),
				('30', '.c4d (Cinema 4D)'),
				('40', '.max/.3ds (3DS Max)'),
				('50', '.dae (Collada)'),
				('60', '.x3d (Web 3D)'),
				('70', '.ai (Illustrator)'), 
				('80', '.psd/.eps (Photoshop)'),
				('90', 'Other file format')
				]

def user_can_upload(user):
	return user.is_authenticated() and user.is_active

def handle_uploaded_sourcefile():
	pass

def getLatestRev(pkVid):
	#latestRevPK_for_sub = Submission.objects.get(pk=pkVid).revision_set.reverse()[:1][0].pk
	latestRev = Submission.objects.get(pk=pkVid).revision_set.all()[Submission.objects.get(pk=pkVid).revision_set.count()-1]
	return latestRev

def getSubInfo(request, subPk, revPk):
	'''display detailed editable information for given revision object'''
	selected_revision = Revision.objects.get(pk=revPk)
	submissionPk = selected_revision.submission.pk
	if subPk == submissionPk:
		print("Submission PKs match")
	selected_submission = Submission.objects.get(pk=submissionPk)
	submissions = Submission.objects.filter(user=selected_submission.user)
	
	if request.method == 'POST':
		pass
		
	else:
		#subform = SubmissionForm(instance=selected_submission)
		#revform = Revision(instance=selected_revision)
		revExt = str(selected_submission.filetype)
		vidCount = Submission.objects.filter(user=selected_submission.user).count()
		context = { 'vidCount': vidCount, 'submissions': submissions,'selected_submission': selected_submission, 'username': selected_submission.user, 'title': selected_submission.title, 'pdb': selected_submission.pdb,
			'filetype': selected_submission.filetype, 'description': selected_submission.description, 'revmodified': selected_revision.modified,
			'sourcefile': selected_revision.sourcefile, 'selected_revision': selected_revision, 'comments': selected_revision.comments, 'timestamp': selected_revision.modified, 'subpk': subPk, 'revpk':revPk, 
			}

		return render_to_response('accounts/submission_info.html', context, context_instance=RequestContext(request))
	
def getRevInfo(request, revPk):
	'''display detailed editable information for given revision object'''
	selected_revision = Revision.objects.get(pk=revPk)
	submissionPk = selected_revision.submission.pk
	selected_submission = Submission.objects.get(pk=submissionPk)
	
	if request.method == 'POST':
		pass
		
	else:
		#subform = SubmissionForm(instance=selected_submission)
		#revform = Revision(instance=selected_revision)
		revExt = str(selected_submission.filetype)
		vidCount = Submission.objects.filter(user=selected_submission.user).count()
		context = { 'vidCount': vidCount, 'selected_submission': selected_submission, 'username': selected_submission.user, 'title': selected_submission.title, 'pdb': selected_submission.pdb,
			'filetype': selected_submission.filetype,'description': selected_submission.description, 'revmodified': selected_revision.modified,
			'sourcefile': selected_revision.sourcefile, 'selected_revision': selected_revision, 'comments': selected_revision.comments, 'timestamp': selected_revision.modified 
			}
		#context = { 'selected_submission': selected_submission, 'selected_revision': selected_revision, title': selected_submission.title, 'latestRevExt': revExt, 'revPk': revPk }

		return render_to_response('accounts/revision_info.html', context, context_instance=RequestContext(request))

@user_passes_test(user_can_upload, login_url="/login/")
def createRevision(request, pkVid):
	'''submit a revision for a submission object'''

	selected_submission = Submission.objects.get(pk=pkVid)
	new_revision = Revision() #create and save to db
	latestRev = getLatestRev(pkVid)
	
	if request.method == 'POST':
		#pdb.set_trace()
		# create form instances for each model object
		subform = SubmissionForm(request.POST, instance=selected_submission)
		ftform = FiletypeForm(request.POST)
		revform = RevisionForm(request.POST, request.FILES) 
		
		# check if bound data is clean for form instances and model instances
		if subform.is_valid() and ftform.is_valid() and revform.is_valid():
			try:
				# save any modified data to existing Submission object 
				subform.save()
				new_revision.save()
				new_revision.user = selected_submission.user
				new_revision.submission = selected_submission
				new_revision.sourcefile = request.FILES['sourcefile']
				rev_set = selected_submission.revision_set.all()
				revCt = rev_set.count()
				print(revCt)
				if request.FILES.get('vidanimation') is None:
					print('in request.FILES.GET(vidanimation)')
					if rev_set[revCt-1].vidanimation is None:
						new_revision.vidanimation = request.FILES['vidanimation']
					else:
						new_revision.vidanimation = rev_set[revCt-1].vidanimation # forward populate
				else:
					new_revision.vidanimation = request.FILES['vidanimation']
					
				if request.FILES.get('vidpic') is None:
					print('in request.FILES.get(vidpic)')
					if rev_set[revCt-1].vidpic is None:
						new_revision.vidpic = request.FILES['vidpic']
					else:
						new_revision.vidpic = rev_set[revCt-1].vidpic # forward populate
				else:
					new_revision.vidpic = request.FILES['vidpic']
				new_revision.comments = request.POST['comments']
				new_revision.save()
				
				selected_submission.revision_set.add(new_revision)
				selected_submission.filetype= ftform.cleaned_data['filetype']
				selected_submission.save()
				
				messages.add_message(request, messages.SUCCESS, (u"Revision and Submission object revised and saved."))
			except Exception as e: 
				new_revision.delete()
				print e
				traceback.print_exc(file=sys.stdout)
			else: 
				print('in else')
				logged_in_user = UserProfile.objects.get(user=request.user)
				# get number of submissions by logged in user and latest revision for that submission object
				vidCount = Submission.objects.filter(user=logged_in_user).count()
				context = { 'vidCount': vidCount, 'username': selected_submission.user, 'title': selected_submission.title, 'pdb': selected_submission.pdb,
							'filetype': selected_submission.filetype, 'description': selected_submission.description, 'latestRev': new_revision.modified, 
							'sourcefile': new_revision.sourcefile, 'new_revision': new_revision, 'comments': new_revision.comments 
							}
				return render_to_response('accounts/revision_success.html', context, context_instance=RequestContext(request))
		else:
			# form submitted and not valid, try again
			print("User form is bound:{0} errors:{1}").format(subform.is_bound, subform.errors)
			print("User form is bound:{0} errors:{1}").format(revform.is_bound, revform.errors)
			context = { 'subform': subform, 'ftform': ftform, 'revform': revform, 'latestRev': latestRev, 'pkVid': pkVid }
			return render_to_response('accounts/revision_form.html', context, context_instance=RequestContext(request))
		
	else:
		'''user is not submitting the form, show them a blank revision form with selected populated fields'''
		# unbound form, not used as fallback values, create form to edit existing Submission obj and create a new revision obj for this Submission object
		subform = SubmissionForm(instance=selected_submission)
		ftform  = FiletypeForm()
		revform = RevisionForm(instance=new_revision)
		revExt = str(selected_submission.filetype)
		context = { 'subform': subform, 'ftform': ftform, 'revform': revform, 'title': selected_submission.title, 'latestRev': latestRev, 'latestRevExt': revExt, 'pkVid': pkVid }

		return render_to_response('accounts/revision_form.html', context, context_instance=RequestContext(request))
	