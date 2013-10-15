# django core
from django import forms

from haystack.forms import SearchForm
from haystack.inputs import AutoQuery
from haystack.query import EmptySearchQuerySet, SearchQuerySet

from profiles.models import UserProfile
from .models import Submission
from notes.models import Tag, Note

class UploadsSearchForm(forms.Form):
	q = forms.CharField()

class UploadsHaystackForm(SearchForm):
	"""slightly customized search form that allows filtering on SearchQuerySet"""

	def search(self):
		if not self.is_valid():
			return self.no_query_found()

		query = self.cleaned_data.get('q','')
		sqs = self.searchqueryset

		if not query:
			return self.no_query_found()

		#if query:
			#sqs = sqs.auto_query(query)
		#	sqs = sqs.using('default').filter(user=AutoQuery(query)).highlight()

		#if self.load_all:
		#	sqs = sqs.load_all()

		#return sqs

		userauto = False
		stateauto = False
		titleauto = False
		tagnameauto = False

		if query:
			print"inside formsuploadshaystackform - inside 3rd if"

			'''
			# or - if all lists are empty, do a general search; otherwise, do autocompletion 
			if not (sqs.using('autocomplete').autocomplete(user_auto=query) or sqs.using('autocomplete').autocomplete(state_auto=query) or 
				sqs.using('autocomplete').autocomplete(title_auto=query) or sqs.using('autocomplete').autocomplete(tagname_auto=query)):
				print"inside if - default"
				sqs = sqs.using('default').filter(content=AutoQuery(query)).highlight()
				print "sqs %s " %sqs
			else:
				# user must provide exact word for any search result
				print"inside if - autocomplete"
				autobools = {}
				sqs1 = EmptySearchQuerySet()
				sqs2 = EmptySearchQuerySet()
				sqs3 = EmptySearchQuerySet()
				sqs4 = EmptySearchQuerySet()

				
				if sqs.using('autocomplete').autocomplete(user_auto=query):
					print 'inside user-auto'
					sqs1 = sqs.using('autocomplete').autocomplete(user_auto=query).best_match()
					autobools['userauto'] = True
					userauto =True

				if sqs.using('autocomplete').autocomplete(state_auto=query):
					print 'inside state-auto'
					sqs2 = sqs.using('autocomplete').autocomplete(state_auto=query)
					autobools['stateauto'] = True
					stateauto = True

				if sqs.using('autocomplete').autocomplete(title_auto=query):
					print 'inside title-auto'
					sqs3 = sqs.using('autocomplete').autocomplete(title_auto=query)
					autobools['titleauto'] = True
					titleauto = True
					
				if sqs.using('autocomplete').autocomplete(tagname_auto=query):
					print 'inside tags-auto'
					sqs4 = sqs.using('autocomplete').autocomplete(tagname_auto=query)
					autobools['tagauto'] = True
					tagnameauto = True
				
				sqs1 = sqs.using('autocomplete').autocomplete(user_auto=query)
				sqs2 = sqs.using('autocomplete').autocomplete(state_auto=query)
				sqs3 = sqs.using('autocomplete').autocomplete(title_auto=query)
				sqs4 = sqs.using('autocomplete').autocomplete(tag_auto=query)
				
				temp = EmptySearchQuerySet()
				for sobj in [sqs1,sqs2,sqs3,sqs4]:
					print "sobj: %s" %sobj
					if sobj:
						temp = sobj | temp
						print "temp %s" %temp

				#sqsa = sqs1 | sqs2 
				#sqsb = sqs3 | sqs4
				#sqs = sqsa | sqsb
				sqs = temp
				'''
			sqs = sqs.using('default').filter(content=AutoQuery(query)).highlight()

			#print "formsprofilessearch: sqs %s" %sqs
			print "in formsprofilessearch:  %s" %sqs

		if self.load_all:
			print"inside last if"
			sqs = sqs.load_all()

		return (sqs , userauto, stateauto, titleauto, tagnameauto)
