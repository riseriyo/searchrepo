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
from profiles.viewsmainnav import getTags

def browseRecent(request):	
	'''query all submissions and return sorted list by most recent date'''
	try: 
		if Submission.objects.all():
			submissions = Submission.objects.all().order_by('-id')
			taglist = getTags(submissions)
			staffpicks = Submission.objects.all().filter(vidstaffpick=True).order_by('created')
			context={ 'title': 'Gallery', 'recent': True, 'stafffaves':False,'staffpicks': staffpicks, 'submissions': submissions, 'taglist': taglist }
			return render_to_response('gallery.html', context, context_instance=RequestContext(request))
		else:
			context={ 'title': 'Gallery', 'recent': True, 'stafffaves':False, 'staffpicks': None, 'submissions': None, 'taglist': None }
			return render_to_response('gallery.html', context, context_instance=RequestContext(request))
	except Exception as e: 
		print e
		import traceback, sys
		traceback.print_exc(file=sys.stdout)
		
def browseStaffPicks(request):	
	'''query all submissions and return sorted list by most recent date'''
	try: 
		if Submission.objects.all():
			submissions = Submission.objects.all().order_by('-id')
			taglist = getTags(submissions)
			staffpicks = Submission.objects.all().filter(vidstaffpick=True).order_by('-created')
			#revpic = Submission.objects.get(vidstaffpick=True).revision_set.order_by('-id')
			context={ 'title': 'Gallery', 'recent':False,'stafffaves':True,'staffpicks': staffpicks, 'submissions': submissions, 'taglist': taglist }
			return render_to_response('library.html', context, context_instance=RequestContext(request))
		else:
			context={ 'title': 'Gallery', 'recent':False,'stafffaves':True,'staffpicks': None, 'submissions': None, 'taglist': None }
			return render_to_response('gallery.html', context, context_instance=RequestContext(request))
	except Exception as e: 
		print e
		import traceback, sys
		traceback.print_exc(file=sys.stdout)
		