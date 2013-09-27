# stdlib python
import datetime

# django core
from django.utils.timezone import utc

# 3rd party plugins
from haystack import indexes

# author's code
from .models import UserProfile
from .models import Position

class PositionIndex(indexes.SearchIndex, indexes.Indexable):
	'''haystack's searchindex object handles data flow into elasticsearch'''

	text 			= indexes.CharField(document=True, use_template=True) # EdgeNgramField - tagging
	position		= indexes.CharField(model_attr='position')

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.filter(created__lte=datetime.datetime.utcnow().replace(tzinfo=utc))
		#return self.get_model().objects.all()

	def get_model(self):
		return Position


class UserProfileIndex(indexes.SearchIndex, indexes.Indexable):
	'''haystack's searchindex object handles data flow into elasticsearch'''

	text 			= indexes.CharField(document=True, use_template=True)
	position 		= indexes.CharField(model_attr='position')		
	city			= indexes.CharField(model_attr='city')
	zipcode			= indexes.CharField(model_attr='zipcode',faceted=True)

	# content for autocomplete field for autcomplete purposes.
	#username 			= indexes.CharField(model_attr='user')
	user_auto 	= indexes.EdgeNgramField(model_attr="user")
	state_auto	= indexes.EdgeNgramField(model_attr="state")

	# clean data
	#def prepare_user(self, obj):
	#	return obj.username.name or 'UserProfileIndex: User Not available'

	def prepare_state(self, obj):
		return obj.state or 'UserProfileIndex: state is Not available'

	def prepare_zipcode(self, obj):
		return obj.zipcode or 'UserProfileIndex: Not available'

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.filter(created__lte=datetime.datetime.utcnow().replace(tzinfo=utc))
		#return self.get_model().objects.all()

	def get_model(self):
		return UserProfile

