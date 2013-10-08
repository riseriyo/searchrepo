from django.conf.urls import patterns, include, url

from haystack.views import SearchView, FacetedSearchView, search_view_factory
from haystack.forms import ModelSearchForm

from .formsprofilessearch import ProfilesAutoCompleteForm
from .viewsprofilessearch import autocompleteSearch


urlpatterns = patterns('',
	url(r'^$', 'profiles.viewsprofilessearch.autocompleteSearch', name='acsearch'),
)
