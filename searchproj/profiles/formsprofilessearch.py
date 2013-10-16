from django import forms

from haystack.forms import SearchForm
from haystack.inputs import AutoQuery
from haystack.query import EmptySearchQuerySet, SearchQuerySet

from .models import UserProfile
from uploads.models import Submission
from notes.models import Tag, Note


class ProfilesAutoCompleteForm(SearchForm):
	"""slightly customized search form that allows filtering on SearchQuerySet"""

	def search(self):
		print"inside search"
		if not self.is_valid():
			print"inside first-if-not"
			return self.no_query_found()

		query = self.cleaned_data.get('q','')
		print "query %s " %query
		sqs = self.searchqueryset
		print "sqs %s " %sqs

		if not query:
			print"inside 2nd if-not"
			print self.no_query_found()
			return self.no_query_found()

		if query:
			print"inside profilesautocompleteform - inside 3rd if"
			# or - if all lists are empty, do a general search; otherwise, do autocompletion 
			if not (sqs.using('autocomplete').autocomplete(user_auto=query) or sqs.using('autocomplete').autocomplete(state_auto=query) or 
				sqs.using('autocomplete').autocomplete(title_auto=query) or sqs.using('autocomplete').autocomplete(tagname_auto=query)):
				print"inside if - default"
				sqs = sqs.using('default').filter(content=AutoQuery(query)).highlight()
				print "sqs %s " %sqs
			else:
				# user must provide exact word for any search result
				print"inside if - autocomplete"
				sqs1 = EmptySearchQuerySet()
				sqs2 = EmptySearchQuerySet()
				sqs3 = EmptySearchQuerySet()
				sqs4 = EmptySearchQuerySet()

				
				if sqs.using('autocomplete').autocomplete(user_auto__exact=query):
					sqs1 = sqs.using('autocomplete').autocomplete(user_auto__exact=query)
					print 'inside user-auto - sqs1: %s' %sqs1

				if sqs.using('autocomplete').autocomplete(state_auto__exact=query):
					sqs2 = sqs.using('autocomplete').autocomplete(state_auto__exact=query)
					print 'inside state-auto - sqs2: %s' %sqs2

				if sqs.using('autocomplete').autocomplete(title_auto__exact=query):
					sqs3 = sqs.using('autocomplete').autocomplete(title_auto__exact=query)
					print 'inside title-auto - sqs3: %s' %sqs3

				if sqs.using('autocomplete').autocomplete(tagname_auto__exact=query):
					sqs4 = sqs.using('autocomplete').autocomplete(tagname_auto__exact=query)
					print 'inside tags-auto - sqs4: %s' %sqs4

				temp = EmptySearchQuerySet()
				for sobj in [sqs1,sqs2,sqs3,sqs4]:
					print "sobj: %s" %sobj
					if sobj:
						temp = sobj | temp
						print "temp %s" %temp

				sqs = temp
				print "in formsprofilessearch:  %s" %sqs

		if self.load_all:
			print"inside last if"
			sqs = sqs.load_all()

		return sqs


class UploadsHaystackForm(SearchForm):
	"""selected term from search widget apply auto query"""

	def search(self):
		if not self.is_valid():
			return self.no_query_found()

		query = self.cleaned_data.get('q','')
		sqs = self.searchqueryset

		if not query:
			return self.no_query_found()

		if query:
			print"inside formsuploadshaystackform - inside 3rd if"

			sqs = sqs.using('default').filter(content=AutoQuery(query)).highlight()

			#print "formsprofilessearch: sqs %s" %sqs
			print "in formsprofilessearch:  %s" %sqs

		if self.load_all:
			print"inside last if"
			sqs = sqs.load_all()

		return sqs
