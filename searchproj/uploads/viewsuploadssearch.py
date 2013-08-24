from django.shortcuts import render_to_response

from .formsuploadssearch import UploadsSearchForm

from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from .models import Filetype, Submission, Revision

'''
class FiletypeList(ListView):
	paginate_by = 10
	model = Filetype

	def get_queryset(self):
		term = self.request.REQUEST.get('search')

		if term:
			return self.model.objects.filter(text_icontains=term)
		else:
			return self.model.objects.all()


class SubmissionList(ListView):
	paginate_by = 10
	model = Submission

	def get_queryset(self):
		term = self.request.REQUEST.get('search')

		if term:
			return self.model.objects.filter(text_icontains=term)
		else:
			return self.model.objects.all()


class RevisionList(ListView):
	paginate_by = 10
	model = Revision

	def get_queryset(self):
		term = self.request.REQUEST.get('search')

		if term:
			return self.model.objects.filter(text_icontains=term)
		else:
			return self.model.objects.all()
'''

'''
def filetypessearch(request):
	form = UploadsSearchForm(request.GET)
	filetypes = form.search()
	return render_to_response("search.html", {"filetypes": filetypes})
	
def revisionssearch(request):
	form = UploadsSearchForm(request.GET)
	revisions = form.search()
	return render_to_response("search.html", {"revisions": revisions})

def submissionssearch(request):
	form = UploadsSearchForm(request.GET)
	submissions = form.search()
	return render_to_response("search.html", {"submissions":submissions})
'''
