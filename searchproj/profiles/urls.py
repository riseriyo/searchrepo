from django.conf.urls import patterns, include, url

from haystack.views import SearchView, FacetedSearchView, search_view_factory
from haystack.forms import ModelSearchForm

from .formsprofilessearch import ProfilesAutoCompleteForm
from .viewsprofilessearch import autocompleteSearch

'''
urlpatterns = patterns('haystack.views',
    url(r'^$', search_view_factory(
        view_class=SearchView,
        #template='search/search.html',
        #searchqueryset=sqs,
        form_class=ProfilesAutoCompleteForm
    ), name='haystack_search'),
)




urlpatterns = patterns('haystack.views',
    url(r'^$', search_view_factory(
        view_class=autocompleteSearch,
        searchqueryset=sqs,
        form_class=ProfilesAutoCompleteForm,
    ), name='acsearch'),
)
'''

urlpatterns = patterns('',
	url(r'^$', 'profiles.viewsprofilessearch.autocompleteSearch', name='acsearch'),
)
