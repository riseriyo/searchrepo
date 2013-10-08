# stdlib python
from __future__ import unicode_literals
import pdb
import json

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
from .formsprofilessearch import ProfilesAutoCompleteForm

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
				(sqs, userauto, stateauto, titleauto, tagsauto) = form.search()

				# creates haystack objects
				#sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q',''))
				if userauto:
					suggestions = [result.user_auto for result in sqs]

				elif stateauto:
					suggestions = [result.state_auto for result in sqs]

				elif titleauto:
					suggestions = [result.title_auto for result in sqs]

				elif tagsauto:
					suggestions = [result.tags_auto for result in sqs]

				else:
					#suggestions = [result.body for result in sqs]
					pass

				print "suggestions: %s"%suggestions
				if not suggestions:
					the_data = json.dumps({})
					#return render_to_response('search/search.html', context=sqs, context_instance=RequestContext(request))
					return HttpResponse(the_data, content_type='application/json')
				else:
					
					the_data = json.dumps({'results':suggestions})
					print the_data
					return HttpResponse(the_data,content_type='application/json')
				
			else: # is_valid
				pass
		else:  # is GET
			pass
	else: # not ajax
		"""
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
		"""

		if request.method == "GET": 
			print 'inside GET'
			form = ProfilesAutoCompleteForm(request.GET)
			if form.is_valid():
				#sqs = SearchQuerySet.using('default').filter(content__contains=AutoQuery(query)).highlight()
				#suggestions = []
				(sqs, userauto, stateauto,titleauto,tagsauto) = form.search()
				results_per_page = None

				if sqs.count():
					print "in else form.search %s " %sqs
					paginator = Paginator(sqs, results_per_page or RESULTS_PER_PAGE)
					try:
						page = paginator.page(int(request.GET.get('page', 1)))
					except InvalidPage:
						raise Http404("No such page of results!")

					context = {'form': form, 'page': page,'paginator': paginator,'query': sqs,'suggestion': None,}

					return render_to_response('search/search.html', context, context_instance=RequestContext(request))
				else:
					sqs = EmptySearchQuerySet()
					paginator = Paginator(sqs, results_per_page or RESULTS_PER_PAGE)
					try:
						page = paginator.page(int(request.GET.get('page', 1)))
					except InvalidPage:
						raise Http404("No such page of results!")

					context = {'form': form, 'page': page,'paginator': paginator,'query': sqs,'suggestion': None,}
					return render_to_response('search/search.html', {'query':None, 'results': results}, context_instance=RequestContext(request) )

				'''
				if not form.search():
					#sqs = SearchQuerySet.none
					#print sqs
					results = EmptySearchQuerySet()
					paginator = Paginator(results, results_per_page or RESULTS_PER_PAGE)

					context = {'query':None, 'results': results}
					return render_to_response('search/search.html', {'query':None, 'results': results}, context_instance=RequestContext(request) )
				else:
					(sqs, userauto, stateauto, titleauto, tagsauto) = form.search()
					print "in else form.search %s" %sqs

					return render_to_response('search/search.html', {'query': sqs if sqs.count() else None}, context_instance=RequestContext(request) )
				'''
			else:
				pass
		else:
			pass

'''

class AutocompleteSearchView(SearchView):
	__name__ = 'SearchWithRequest'

	def build_form(self, form_kwargs=None):
		if form_kwargs is None:
			form_kwargs = {}

		if self.searchqueryset is None:
			sqs = SearchQuerySet().autcomplete(content_auto=self.request.GET.get('q',''))
			form_kwargs['searchqueryset'] = sqs

		return super(AutocompleteSearchView, self).build_form(form_kwargs)
'''