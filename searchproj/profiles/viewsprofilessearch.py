# stdlib python
import pdb
import json

# django core
# core django imports
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.http import HttpResponse

# 3rd party plugins
from haystack.query import SearchQuerySet

# author code
from .models import UserProfile
from .formsprofilessearch import ProfilesAutoCompleteForm

import logging
logger = logging.getLogger(__name__)


def autocompleteSearch(request):
	"""create a SQS and set the content_auto to what is inside the POST array"""
	#pdb.set_trace()
	print"inside autocompleteSearch"
	print request.GET

	if request.is_ajax():
		print 'inside is_ajax'
		if request.method == "GET":
			print 'inside GET'
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
					suggestions = [result.body for result in sqs]

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
	else: # is_ajax
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