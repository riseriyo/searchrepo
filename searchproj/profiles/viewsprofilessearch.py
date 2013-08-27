# stdlib python
import pdb

# django core
from django.shortcuts import render_to_response
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

# 3rd party plugins
from haystack.query import SearchQuerySet

# author code
from .models import UserProfile
#from .formsprofilessearch import ProfilesSearchForm

import logging
logger = logging.getLogger(__name__)


def autocompleteSearch(request):
	"""create a SQS and set the content_auto to what is inside the POST array"""

	print"inside autocompleteSearch"
	# return haystack objects
	sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q',''))
	

	return render_to_response("search/search.html", {'results':sqs})

