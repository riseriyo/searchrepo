from django import forms

from haystack.forms import SearchForm
from haystack.inputs import AutoQuery

from .models import UserProfile
from uploads.models import Submission


class ProfilesSearchForm(forms.Form):
	q = forms.CharField(required=False)

class ProfilesAutoCompleteForm(SearchForm):
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
			print self.no_query_found()
			return self.no_query_found()

		userauto = False
		stateauto = False
		titleauto = False
		tagsauto = False

		if query:
			print"inside 3rd if"
			# or - if all lists are empty, do a general search; otherwise, do autocompletion 
			if not (sqs.using('autocomplete').autocomplete(user_auto=query) or sqs.using('autocomplete').autocomplete(state_auto=query) or 
				sqs.using('autocomplete').autocomplete(title_auto=query) or sqs.using('autocomplete').autocomplete(tags_auto=query)):
			#if not sqs:
				print"inside if - default"
				sqs = sqs.using('default').filter(content=AutoQuery(query)).highlight()
				print sqs
			else:
				# user must provide exact word for any search result
				#sqs = sqs.using('default').models(UserProfile, Submission).filter(content=query)
				print"inside if - autocomplete"
				if sqs.using('autocomplete').autocomplete(user_auto=query):
					print 'inside user-auto'
					sqs = sqs.using('autocomplete').autocomplete(user_auto=query)
					userauto = True
				elif sqs.using('autocomplete').autocomplete(state_auto=query):
					print 'inside state-auto'
					sqs = sqs.using('autocomplete').autocomplete(state_auto=query)
					stateauto = True
				elif sqs.using('autocomplete').autocomplete(title_auto=query):
					print 'inside title-auto'
					sqs = sqs.using('autocomplete').autocomplete(title_auto=query)
					titleauto = True
				elif sqs.using('autocomplete').autocomplete(tags_auto=query):
					print 'inside tags-auto'
					sqs = sqs.using('autocomplete').autocomplete(tags_auto=query)
					tagsauto = True

				print sqs

		if self.load_all:
			print"inside last if"
			sqs = sqs.load_all()

		return (sqs, userauto, stateauto, titleauto, tagsauto)
