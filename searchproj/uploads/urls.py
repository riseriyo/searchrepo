from django.conf.urls import patterns, include, url

from haystack.views import SearchView, FacetedSearchView, search_view_factory
from haystack.forms import ModelSearchForm

from profiles.formsprofilessearch import ProfilesAutoCompleteForm
#from .viewsprofilessearch import autocompleteSearch
from .formsuploadssearch import UploadsHaystackForm
from .viewsuploadssearch import getSearchResults


urlpatterns = patterns('',
	url(r'^$', 'uploads.viewsuploadssearch.getSearchResults', name='search'),
)
