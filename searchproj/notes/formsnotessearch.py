from django import forms
from haystack.forms import SearchForm

'''
class NotesSearchForm(forms.Form):
	"""Basic form for searching with Queryset filter method"""
	q = forms.CharField()

class NotesHaystackForm(SearchForm):
	"""Slightly customized search form that allows filtering on the SearchQuerySet"""

	def search(self):
		if not self.is_valid():
			return self.no_query_found()

		query = self.cleaned_data.get('q','')
		sqs = self.searchqueryset

		if not query:
			return self.no_query_found

		if query:
			sqs = sqs.auto_query(query)

		if self.load_all:
			sqs = sqs.load_all()

		return sqs
	'''