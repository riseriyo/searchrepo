# stdlib python
from __future__ import unicode_literals
import pdb
import json
from itertools import chain

# django core
# core django imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.http import Http404
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.http import HttpResponse

# 3rd party plugins
from haystack.query import SearchQuerySet
from django.core.paginator import Paginator, InvalidPage
from haystack.query import EmptySearchQuerySet

# author code

from .formsuploadssearch import UploadsHaystackForm
from .models import Filetype, Submission, Revision
from profiles.models import UserProfile
from profiles.formsprofilessearch import ProfilesAutoCompleteForm

import logging
logger = logging.getLogger(__name__)

'''
def getSearchResults(request):

	#	 Template:: ``search/search.html``
	#	Context::
	#	* form
	#	An instance of the ``form_class``. (default: ``ModelSearchForm``)
	#	* page
	#	The current page of search results.
	#	* paginator
	#	A paginator instance for the results.
	#	* query
	#	The query received by the form.

	
	if request.method == "GET": 
		print 'inside GET'
		#form = UploadsHaystackForm(request.GET)
		form = ProfilesAutoCompleteForm(request.GET)

		print "GET %s " %request.GET
		if form.is_valid():
			#sqs = SearchQuerySet.using('default').filter(content__contains=AutoQuery(query)).highlight()
			#suggestions = []
			#sqs = form.search()#, userauto, stateauto,titleauto,tagauto) = form.search()
			(sqs, userauto, stateauto, titleauto, tagnameauto) = form.search()
			results_per_page = None

			if sqs.count():
				print "in else form.search %s " %sqs
				paginator = Paginator(sqs, results_per_page or RESULTS_PER_PAGE)
				print "paginator %s " %paginator
				try:
					page = paginator.page(int(request.GET.get('page', 1)))
					print "page %s "% page
				except InvalidPage:
					raise Http404("No such page of results!")

				context = {'form': form, 'page': page,'paginator': paginator,'query': form.cleaned_data['q'],'suggestion': None, 'sqs': sqs,}

				return render_to_response('search/search.html', context, context_instance=RequestContext(request))
			else:
				sqs = EmptySearchQuerySet()
				paginator = Paginator(sqs, results_per_page or RESULTS_PER_PAGE)
				try:
					page = paginator.page(int(request.GET.get('page', 1)))
				except InvalidPage:
					raise Http404("No such page of results!")

				context = {'form': form, 'page': page,'paginator': paginator,'query': form.cleaned_data['q'],'suggestion': None, 'sqs': sqs,}
				return render_to_response('search/search.html', context, context_instance=RequestContext(request) )
		else:
			pass
	else:
		pass


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


from django.conf.urls import patterns, include, url

from haystack.views import SearchView, search_view_factory
from haystack.forms import ModelSearchForm

from .formsprofilessearch import ProfilesAutoCompleteForm
from .viewsprofilessearch import autocompleteSearch


urlpatterns = patterns('haystack.views',
    url(r'^$', search_view_factory(
        view_class=SearchView,
        #template='search/search.html',
        #searchqueryset=sqs,
        form_class=UploadsHaystackForm
    ), name='termsearch'),
)




urlpatterns = patterns('haystack.views',
    url(r'^$', search_view_factory(
        view_class=autocompleteSearch,
        searchqueryset=sqs,
        form_class=ProfilesAutoCompleteForm,
    ), name='acsearch'),
)



#urlpatterns = patterns('',
#	url(r'^$', 'uploads.viewsuploadssearch.termSearch', name='termsearch'),
#)
'''