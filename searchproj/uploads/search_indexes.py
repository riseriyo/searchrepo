# python stdlib
import datetime

# django core
from django.utils.timezone import utc

# 3rd party plugins
from haystack import indexes

# author's app
from .models import Submission
from .models import Revision
from .models import Filetype

class FiletypeIndex(indexes.SearchIndex, indexes.Indexable):
	'''haystack's searchindex object handles data flow into elasticsearch'''

	text 			= indexes.EdgeNgramField(document=True, use_template=True)
	filetype		= indexes.CharField(model_attr='filetype', faceted=True)

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		#return self.get_model().objects.filter(created__lte=datetime.datetime.utcnow().replace(tzinfo=utc))
		return self.get_model().objects.all()

	def get_model(self):
		return Filetype


class SubmissionIndex(indexes.SearchIndex, indexes.Indexable):
	'''haystack's searchindex object handles data flow into elasticsearch'''

	text 				= indexes.CharField(document=True, use_template=True)
	title				= indexes.CharField(model_attr='title')
	filetype			= indexes.CharField(model_attr='filetype', faceted=True)
	description			= indexes.CharField(model_attr='description')

	# content for autocomplete field for autcomplete purposes.
	content_auto		= indexes.EdgeNgramField(model_attr='member')
	content_auto		= indexes.EdgeNgramField(model_attr="tags")

	# clean data
	#def prepare_user(self, obj):
	#	return obj.user.name or 'SubmissionIndex: User Not available'

	def prepare_title(self, obj):
		return obj.title or 'SubmissionIndex: title Not available'

	def prepare_filetype(self, obj):
		return obj.filetype or 'SubmissionIndex: filetype Not available'

	def prepare_tags(self,obj):
		return obj.tags or 'SubmissionIndex: tags Not available'

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.filter(created__lte=datetime.datetime.utcnow().replace(tzinfo=utc))
		#return self.get_model().objects.all()

	def get_model(self):
		return Submission


class RevisionIndex(indexes.SearchIndex, indexes.Indexable):
	'''haystack's searchindex object handles data flow into elasticsearch'''

	# use EdgeNgramField for autocompletion
	text				= indexes.CharField(document=True, use_template=True)
	sourcefile			= indexes.CharField(model_attr='sourcefile')
	vidanimation 		= indexes.CharField(model_attr='vidanimation')
	vidpic				= indexes.CharField(model_attr='vidpic')
	comments			= indexes.CharField(model_attr='comments')

	user 				= indexes.CharField(model_attr='user') 
	#content_auto	  	= indexes.EdgeNgramField(model_attr='user')

	# clean data
	def prepare_user(self,obj):
		return obj.user.name or 'RevisionIndex: user not available'

	def prepare_sourcefile(self, obj):
		return obj.sourcefile.url or 'RevisionIndex: sourcefile not available'

	def prepare_vidanimation(self, obj):
		return obj.vidanimation.url or 'RevisionIndex: vidanimation not available'

	def prepare_vidpic(self, obj):
		return obj.vidpic.url or 'RevisionIndex: vidpic not available'

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.filter(created__lte=datetime.datetime.utcnow().replace(tzinfo=utc))
		#return self.get_model().objects.all()

	def get_model(self):
		return Revision


