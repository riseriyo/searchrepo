# stdlib python
import datetime

# django core
from django.utils import timezone
from django.utils.timezone import utc

# 3rd party plugins
from haystack import indexes

# author's code
from .models import Note
from .models import Tag


class TagIndex(indexes.SearchIndex, indexes.Indexable):
	'''index tags '''
	text 				= indexes.CharField(document=True, use_template=True)
	tagname_auto	 	= indexes.EdgeNgramField(model_attr="tagname", null=True) # or indexes.EdgeNgramField()???
	notes 				= indexes.MultiValueField()

	# error TypeError: 'ManyRelatedManager' object is not iterable - don't add model_attr to MultiValueField()!!!
	# ERROR:root:Error updating notes using default  
	def prepare_tags(self,obj):
		#return [obj.id for tag in obj.tags.all()] or 'NoteIndex: tags not available'
		#return [obj.id for tag in obj.tags.all()]
		return [note.title for note in obj.notes.all()]
		
	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.filter(created__lte=datetime.datetime.utcnow().replace(tzinfo=utc))
		#return self.get_model().objects.all()

	def get_model(self):
		return Tag


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
	'''haystack's searchindex object handles data flow into elasticsearch'''
	
	text 				= indexes.CharField(document=True, use_template=True)
	user 				= indexes.CharField(model_attr='user')
	pub_date 			= indexes.DateTimeField(model_attr='pub_date')
	#tags				= indexes.MultiValueField()
	body				= indexes.CharField(model_attr='body')

	#content_auto		= indexes.EdgeNgramField(model_attr='author')
	title_auto 			= indexes.EdgeNgramField(model_attr="title")
	#body_auto	= indexes.EdgeNgramField(model_attr="body")

	# clean data
	def prepare_author(self, obj):
		return obj.user.name or 'NoteIndex: Notetaker available'

	def prepare_pub_date(self, obj):
		return obj.pub_date or 'NoteIndex: pub_date Not available'

	def prepare_title(self, obj):
		return obj.title or 'NoteIndex: title Not available'

	def prepare_body(self,obj):
		return obj.body or 'NoteIndex: body not available'

	#def prepare_tags(self, obj):
	#	return [tag.tagname for tag in self.tag_set.all()]

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.filter(created__lte=datetime.datetime.utcnow().replace(tzinfo=utc))
		#return self.get_model().objects.all()

	def get_model(self):
		return Note
