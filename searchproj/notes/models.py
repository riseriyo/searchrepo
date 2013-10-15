# stdlib imports

# core django imports
from django.db import models
#from django.conf import settings
from django.contrib.auth.models import User

# 3rd party app imports
from model_utils.models import TimeStampedModel

# author's
from profiles.models import UserProfile

class Tag(TimeStampedModel):
	'''M2M tag can be in many Notes and a Note can have many tags'''
	tagname			= models.CharField(max_length=250, null=True, blank=True, unique=True) # tag can be in many notes
	notes 	 		= models.ManyToManyField('Note', related_name='tags', null=True, blank=True) 				# a note may have 0 or 1 or more tags

	def __unicode__(self):
		return "%s" %(self.tagname)

	def displayNotes(self):
		return ', '.join([note.title for note in self.notes.all()])


class Note(TimeStampedModel):
	user		= models.ForeignKey('profiles.UserProfile', related_name='author') # a submission remembers who submitted it
	pub_date 	= models.DateTimeField()
	title 		= models.CharField(max_length=200)
	body 		= models.TextField()
	#tags		= models.ManyToManyField('Tag', null=True, blank=True) # a note may have 0 or 1 or more tags
	#tag 		= models.CharField(max_length=250, null=True, blank=True, unique=True)

	def __unicode__(self):
		return "%s" %(self.title)

	def displayTags(self):
		return ', '.join([tag.tagname for tag in self.tags.all()])
