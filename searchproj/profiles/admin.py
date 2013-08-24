'''
Created on Oct 25, 2012

@author: rise
Display the uploads in the django admin interface.
'''
# stdlib imports

# core django imports
from django.contrib import admin

# 3rd party app imports

# project imports
from .models import UserProfile
from .search_indexes import UserProfileIndex
from .models import Position
from .search_indexes import PositionIndex
from uploads.models import Submission
from uploads.search_indexes import SubmissionIndex
from uploads.models import Revision
from uploads.search_indexes import RevisionIndex
from uploads.models import Filetype
from uploads.search_indexes import FiletypeIndex
from notes.models import Note
from notes.search_indexes import NoteIndex



#class SubmissionInline(admin.TabularInline):
#	model		= Submission
#	extra		= 3
	
	
class UserProfileAdmin(admin.ModelAdmin):
	fieldsets		= [
					  ('Activation/Registration', { 'fields': ['user', 'userpic', 'activation_key', 'key_expires']}),
					  ('Mailing Address', { 'fields': ['address1', 'address2', 'city', 'state', 'zipcode'], 'classes': ['collapse']}), 
					  ]
	#inlines		= [SubmissionInline]
	list_display	= ['user','address1','state','zipcode']
	
	
class NoteAdmin(admin.ModelAdmin):
	fieldsets		= [
					('Title', { 'fields': ['author','title']}),
					('Published date',{ 'fields': ['pub_date']}),
					('Body', { 'fields': ['body']}),
					]
	list_display	= ('author', 'pub_date', 'title', 'body')
	
class SubmissionAdmin(admin.ModelAdmin):
	fieldsets		= [
					('User/Title', { 'fields': ['user', 'title']}),
					('Featured Video/Staff Picks',{ 'fields': ['vidfeature','vidstaffpick']}),
					('Scene File/Animation Info', { 'fields': ['filetype', 'description']}),
					]
	list_display	= ('id','title', 'user', 'filetype', 'created')
	
class RevisionAdmin(admin.ModelAdmin):
	fieldsets		= [ 
					('Submission/User', {'fields':['submission','user']}), 
					('Source File', {'fields':['sourcefile']}),
					('Video File', {'fields':['vidanimation']}),
					('Thumbnail Source', {'fields':['vidpic']}),
					('Comments', {'fields':['comments']})
					]
	list_display 	= ('id', 'submission', 'user', 'created', 'modified' )
	
admin.site.register(UserProfile, UserProfileAdmin)
#site.register(UserProfile, UserProfileIndex)
admin.site.register(Note, NoteAdmin)
#site.register(Note, NoteIndex)
admin.site.register(Submission, SubmissionAdmin)
#site.register(Submission, SubmissionIndex)
admin.site.register(Revision, RevisionAdmin)
#site.register(Revision, RevisionIndex)
admin.site.register(Position)
admin.site.register(Filetype)