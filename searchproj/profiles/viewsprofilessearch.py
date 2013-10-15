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
from .models import UserProfile
from .formsprofilessearch import ProfilesAutoCompleteForm, UploadsHaystackForm

import logging
logger = logging.getLogger(__name__)


def autocompleteSearch(request):
	"""create a SQS and set the content_auto to what is inside the POST array"""
	#pdb.set_trace()
	print"inside autocompleteSearch"
	#print request.GET
	RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)

	if request.is_ajax():
		print 'inside is_ajax'
		if request.method == "GET":
			print 'inside GET %s'%request.GET
			form = ProfilesAutoCompleteForm(request.GET)
			
			if form.is_valid():
				#pdb.set_trace()
				print "inside is_valid"
				suggestions = []
				sqs = form.search()

				for result in sqs:
					if result.user_auto is not None and request.GET['q'] in result.user_auto.lower():
						suggestions.append(result.user_auto)
					if result.state_auto is not None and request.GET['q'] in result.state_auto.lower():
						suggestions.append(result.state_auto)
					if result.title_auto is not None and request.GET['q'] in result.title_auto.lower():
						suggestions.append(result.title_auto)
					if result.tagname_auto is not None and request.GET['q'] in result.tagname_auto.lower():
						suggestions.append(result.tagname_auto)


				print 'suggestions: %s' %suggestions
				suggestions = sorted(list(set(suggestions)))

				print "final suggestions: %s"%suggestions
				if not suggestions:
					the_data = json.dumps({})
					print "the_data %s"%the_data
					return HttpResponse(the_data, content_type='application/json')
				else:
					
					the_data = json.dumps({'results':suggestions})
					print "the_data %s"%the_data
					return HttpResponse(the_data,content_type='application/json')
				
			else: # is_valid
				pass
		else:  # is GET
			pass
	else: # not ajax

		'''
			 Template:: ``search/search.html``
			Context::
			* form
			An instance of the ``form_class``. (default: ``ModelSearchForm``)
			* page
			The current page of search results.
			* paginator
			A paginator instance for the results.
			* query
			The query received by the form.
		'''	

		if request.method == "GET": 
			print 'inside GET'
			form = UploadsHaystackForm(request.GET)

			print "GET %s " %request.GET
			if form.is_valid():
				sqs = form.search()
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
		