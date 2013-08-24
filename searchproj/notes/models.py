# stdlib imports

# core django imports
from django.db import models
#from django.conf import settings
from django.contrib.auth.models import User

# 3rd party app imports
from model_utils.models import TimeStampedModel

class Note(TimeStampedModel):
	author 		= models.ForeignKey(User)
	pub_date 	= models.DateTimeField()
	title 		= models.CharField(max_length=200)
	body 		= models.TextField()

	def __unicode__(self):
		return self.title
