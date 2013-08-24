from django import forms
from haystack.forms import FacetedSearchForm

'''
class UploadsSearchForm(forms.Form):
	q = forms.CharField()

class UploadsHaystackForm(FacetedSearchForm):
	"""slightly customized search form that allows filtering on SearchQuerySet"""

	def search(self):
		if not self.is_valid():
			return self.no_query_found()

		query = self.cleaned_data.get('q','')
		sqs = self.SearchQuerySet

		if not query:
			return self.no_query_found()

		if query:
			sqs = sqs.auto_query(query)

		if self.load_all:
			sqs = sqs.load_all()

		return sqs
		'''