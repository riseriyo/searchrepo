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
from .models import Position
from uploads.models import Submission
from uploads.models import Revision
from uploads.models import Filetype
from notes.models import Tag
from notes.models import Note

#class SubmissionInline(admin.TabularInline):
#	model		= Submission
#	extra		= 3
	
	
class UserProfileAdmin(admin.ModelAdmin):
	fieldsets		= [
					  ('Activation/Registration', { 'fields': ['user', 'userpic', 'activation_key', 'key_expires']}),
					  ('Mailing Address', { 'fields': ['address1', 'address2', 'city', 'state', 'zipcode'], 'classes': ['collapse']}), 
					  ]
	#inlines		= [SubmissionInline]
	list_display	= ['user','address1','state','zipcode',]


class TagAdmin(admin.ModelAdmin):
	fieldsets		= [
					('Tag', { 'fields': ['tagname']}),
					]
	list_display	= ('tagname', 'displayNotes', )


class NoteAdmin(admin.ModelAdmin):
	fieldsets		= [
					('Title', { 'fields': ['user','title']}),
					('Published date',{ 'fields': ['pub_date']}),
					('Body', { 'fields': ['body']}),
					]
	list_display	= ('user', 'pub_date', 'title', 'body', 'displayTags',)
	
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
admin.site.register(Tag, TagAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Revision, RevisionAdmin)
admin.site.register(Position)
admin.site.register(Filetype)