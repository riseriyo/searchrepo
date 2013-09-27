# stdlib python
import datetime

# django core
from django.utils import timezone
from django.utils.timezone import utc

# 3rd party plugins
from haystack import indexes

# author's code
from .models import Note


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
	'''haystack's searchindex object handles data flow into elasticsearch'''
	
	text 				= indexes.CharField(document=True, use_template=True)
	user 				= indexes.CharField(model_attr='user')
	pub_date 			= indexes.DateTimeField(model_attr='pub_date')
	#title				= indexes.CharField(model_attr='title')
	body				= indexes.CharField(model_attr='body')

	#content_auto		= indexes.EdgeNgramField(model_attr='author')
	title_auto 	= indexes.EdgeNgramField(model_attr="title")
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

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.filter(created__lte=datetime.datetime.utcnow().replace(tzinfo=utc))
		#return self.get_model().objects.all()

	def get_model(self):
		return Note
