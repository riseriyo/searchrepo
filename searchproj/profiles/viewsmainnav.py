# stdlib imports

# core django imports
from django.views.generic import TemplateView

# 3rd party imports
from uploads.models import Submission

# project imports


# main navigation pages
class Home(TemplateView):
	'''MFB homepage'''
	
	template_name = 'index.html'
	
	def get_context_data(self):
		return {'title':'Home'}
	
home = Home.as_view()

def getTags(submissions):
	'''get all tags ordered by most recent'''
	tlist = []
	templist = []
	taglist = []
	for obj in submissions:
		tlist = obj.tags.split(',')
		for tags in tlist:
			templist.append(tags.lstrip())
	for tag in templist:
		if tag != '':
			taglist.append(tag)
	#print taglist
	return taglist
	
class Gallery(TemplateView):
	'''Login page'''
	
	template_name = 'gallery.html'
	
	# 0 - False; 1 = True
	def get_context_data(self):
		if Submission.objects.count() and Submission.objects.all().filter(vidstaffpick=True).count():
			submissions = Submission.objects.all().order_by('-id')
			#taglist = getTags(submissions)
			staffpicks = Submission.objects.all().filter(vidstaffpick=True).order_by('created')
			return { 'title': 'Gallery', 'recent':True,'stafffaves':False,'staffpicks': staffpicks, 'submissions': submissions, 'taglist': taglist, }
		else:
			return { 'title': 'Gallery', 'recent':False,'stafffaves':True,'staffpicks': None, 'submissions': None, 'taglist': taglist, }
	
gallery = Gallery.as_view()

# main navigation pages
class About(TemplateView):
	'''MFB homepage'''
	
	template_name = 'about.html'
	
	def get_context_data(self):
		return {'title':'About'}
	
about = About.as_view()
