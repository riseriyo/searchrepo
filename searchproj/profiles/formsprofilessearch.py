from django import forms
from haystack.forms import SearchForm


class ProfilesSearchForm(forms.Form):
	q = forms.CharField(required=False)

class ProfilesHaystackForm(SearchForm):
	"""slightly customized search form that allows filtering on SearchQuerySet"""

	def search(self):
		print"inside search"
		if not self.is_valid():
			print"inside first-if-not"
			return self.no_query_found()

		query = self.cleaned_data.get('q','')
		print query
		sqs = self.searchqueryset
		print sqs

		if not query:
			print"inside 2nd if-not"
			return self.no_query_found()

		if query:
			print"inside 3rd if"
			sqs = sqs.autocomplete(content_auto=query)
			print sqs

		if self.load_all:
			print"inside last if"
			sqs = sqs.load_all()

		return sqs
