#*******************************************************************
# models.py: 
# Database layout - A model class represents a database table, and 
# an instance of that class represents a particular record in the 
# database table.
#*******************************************************************
# stdlib imports
import os
import uuid

# core django imports
from django.db import models
from django.core.files import File
#from django.core.exceptions import ValidationError

# 3rd party app imports
#from easy_thumbnails.fields import ThumbnailerImageField
from model_utils.models import TimeStampedModel

# project's imports


class Filetype(TimeStampedModel):
	'''describe the file format of an upload'''
	filetype 			= models.CharField(max_length=50)

	def __unicode__(self):
		return "%s" %(self.filetype)


class Submission(TimeStampedModel):
	'''submit objects of scene files, animations; submission can have multiple revision objects'''
	user				= models.ForeignKey('profiles.UserProfile', related_name='member') # a submission remembers who submitted it
	title 				= models.CharField(max_length=250)
	filetype 			= models.ForeignKey(Filetype, null=True, blank=True)
	tags				= models.CharField(max_length=250, null=True)
	description 		= models.TextField()
	vidfeature			= models.BooleanField()
	vidstaffpick		= models.BooleanField()

	# used in admin interface, shell, etc.; self.id value autocreated by django
	def __unicode__(self):
		#return self.firstName or str(self.id)
		return "%s" %(self.title)
	
	def delete(self, *args, **kwargs):
		self.file.delete(False)
		super(Submission, self).delete(*args, **kwargs)

	def displayTags(self):
		return ', '.join([tag.tagname for tag in self.tags.all()])	

def upload_source_to(instance, filename):
	sourceExt = filename.split('.')[-1]
	sanitized_filename = "%s.%s" %(instance.randnum, sourceExt)
	return os.path.join("scenes","uid_" + str(instance.user.user_id), instance.randnum, (str(instance.created)[:26]).replace(" ","_"), sanitized_filename)

def upload_movie_to(instance, filename):
	ext = filename.split('.')[-1]
	sanitized_filename = "%s.%s" %(instance.randnum, ext)
	return os.path.join("videos","uid_" + str(instance.user.user_id), instance.randnum, (str(instance.created)[:26]).replace(" ","_"), sanitized_filename)

def upload_thumbnail_to(instance, filename):
	ext = filename.split('.')[-1]
	sanitized_filename = "%s.%s" %(instance.randnum, ext)
	return os.path.join("images","uid_" + str(instance.user.user_id), instance.randnum, (str(instance.created)[:26]).replace(" ","_"), sanitized_filename)
	
class Revision(TimeStampedModel):
	'''upload newly modified animation scenes, thumbnails, changing of text input'''
	randnum = str(uuid.uuid4())
	submission 			= models.ForeignKey('Submission', null=True, blank=True) # a revision remembers which submission it belongs to
	user				= models.ForeignKey('profiles.UserProfile', null=True, blank=True)
	#published			= models.DateTimeField(null=True)
	# original uploaded file (latest revision) for users to download; placed in MEDIA_ROOT
	sourcefile			= models.FileField('Revision',max_length=250, upload_to=upload_source_to)
	# video of source file; placed in MEDIA_ROOT and MEDIA_URL
	vidanimation		= models.FileField('Revision', max_length=250, upload_to=upload_movie_to, null=True, blank=True)
	# thumbnail preview/image; parsed out of filetype or submitted by user; placed in MEDIA_ROOT
	vidpic				= models.ImageField('Revision', max_length=250, upload_to=upload_thumbnail_to, null=True, blank=True)
	comments			= models.CharField(max_length=200)
	
	# revision is related to submission and submission has many revisions that need to be ordered wrt submission
	class Meta:
		order_with_respect_to = 'submission'
