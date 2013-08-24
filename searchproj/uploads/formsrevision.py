'''
Created on Jan 3, 2013

@author: rise
'''
# stdlib imports

# core django imports
from django import forms
from django.forms import ModelForm # ability to pass some model to the form

# 3rd party imports
import magic

# project app imports
from .models import Submission
from .models import Revision
from .models import Filetype
#from easy_thumbnails.fields import ThumbnailerImageField

FILETYPES = [
				('0', 'Select file format of source file'),
				('10', '.blend (Blender)'),
				('20', '.ma/.mb (Maya)'),
				('30', '.c4d (Cinema 4D)'),
				('40', '.max/.3ds (3DS Max)'),
				('50', '.dae (Collada)'),
				('60', '.x3d (Web 3D)'),
				('70', '.ai (Illustrator)'), 
				('80', '.psd/.eps (Photoshop)'),
				('9', 'Other file format')
				]

VALIDMIMES = [
			'text/plain',
			'application/octet-stream',
			'application/xml',
			'application/pdf',
			'application/zip',
			'inode/directory',
			'text/plain',
			'image/x-xcf',
			'application/postscript',
			'image/vnd.adobe.photoshop',
			'video/quicktime',
			'video/mp4',
			'video/x-msvideo',
			'video/x-ms-asf',
			'video/avi',
			'video/mov',
]


class SubmissionForm(ModelForm):
	'''create a Submission object and modify with revision form object'''
	title			= forms.CharField(label=(u'Title'), widget=forms.TextInput({"placeholder":"Enter a title", "class":"input-block-level", 'id':'title'}), error_messages={'invalid':("Enter a title.")})
	tags			= forms.CharField(label=(u'Tags'),widget=forms.TextInput({"placeholder":"Add tags for easy discovery","class":"input-block-level", 'id':'tags'}),error_messages={"invalid":("Enter a tag")})
	description	 	= forms.CharField(label=(u'Description'), widget=forms.Textarea({"placeholder": "Please describe your data as well as you can", "class":"input-block-level",'id':'description'}))
	
	class Meta: 
		model = Submission
		fields = ('title','tags','description')
	
	def clean_title(self):
		title = self.cleaned_data['title']
		if title is None:
			raise forms.ValidationError("Please enter a title.")
		return self.cleaned_data['title']
	
	def clean_tags(self):
		tags = self.cleaned_data['tags']
		if tags is None:
			raise forms.ValidationError("Please add tags for easy discovery.")
		return self.cleaned_data['tags']
	
	def clean_description(self):
		description = self.cleaned_data['description']
		if description is None:
			raise forms.ValidationError("Please tell us about your animation.")
		return self.cleaned_data['description']
		
		
class FiletypeForm(ModelForm):
	'''create a filetype form to describe file format'''
	filetype 		= forms.ChoiceField(label=(u'Filetype'), widget=forms.Select({"id":'filetype-select'}), choices=FILETYPES, initial="Select file format of source file")
	
	class Meta:
		model = Filetype
		
	def clean_filetype(self):
		filetype_pk = self.cleaned_data['filetype']
		try:
			return Filetype.objects.get(pk=filetype_pk)
		except Filetype.DoesNotExist:
			raise forms.ValidationError("Please choose a filetype.")
		
		
class RevisionForm(ModelForm):
	'''create a Revision object with form, add when Submission object is revised'''
	vidanimation 	= forms.FileField(label=(u'Video File'), required=False)
	vidpic			= forms.ImageField(label=(u'Thumbnail'), required=False)
	comments		= forms.CharField(label=(u'Ancestors'), widget=forms.TextInput({"placeholder":"Please enter comments", "class":"input-block-level", 'id':'comments'}))
	
	class Meta: 
		model = Revision
		fields = ('sourcefile','vidanimation','vidpic','comments')

	def clean_sourcefile(self):
		'''check size, filetype, and extension of source upload'''
		upload = self.cleaned_data.get('sourcefile')
		if upload:
			if upload._size > 100*1024*1024: #1mb; 10*1024*1024 = 10mb
				raise forms.ValidationError("Source file exceeds maximum size: 100mb")
			if upload._size < 2.5*1024*1024:
				if not magic.from_buffer(upload.name, mime=True) in VALIDMIMES:
					raise forms.ValidationError("Source file is not a valid filetype.")
			else:
				if not magic.from_file(upload.temporary_file_path(), mime=True) in VALIDMIMES:
					raise forms.ValidationError("Source file is not a valid filetype.")
			if upload.name.split('.')[-1] is None:
				raise forms.ValidationError("Source file has no extension.")
		else:
			raise forms.ValidationError("Unable to read uploaded file.")
		return self.cleaned_data.get('sourcefile')
	
	def clean_vidanimation(self):
		'''optional upload; check size, filetype, and extension of video upload'''
		upload = self.cleaned_data.get('vidanimation')
		if upload:
			if upload._size > 50*1024*1024: #5mb; 10*1024*1024 = 10mb
				raise forms.ValidationError("Video file exceeds maximum size: 50mb")
			if upload._size < 2.5*1024*1024:
				if not magic.from_buffer(upload.name, mime=True) in VALIDMIMES:
					raise forms.ValidationError("Video file is not a valid filetype.")
			else:
				if not magic.from_file(upload.temporary_file_path(), mime=True) in VALIDMIMES:
					raise forms.ValidationError("Video file is not a valid filetype.")
			if upload.name.split('.')[-1] is None:
				raise forms.ValidationError("Video file has no extension.")
		return self.cleaned_data.get('vidanimation')
		
	
	def clean_vidpic(self):
		'''optional upload; check size and extension of thumbnail upload'''
		upload = self.cleaned_data.get('vidpic')
		if upload:
			if upload._size > 5*1024*1024: #10*1024*1024 = 10mb
				raise forms.ValidationError("Thumbnail file exceeds maximum size: 5mb")
			if upload.name.split('.')[-1] is None:
				raise forms.ValidationError("Thumbnail file has no extension.")
		return self.cleaned_data.get('vidpic')
	
	def clean_comments(self):
		'''comments required'''
		comments = self.cleaned_data['comments']
		if comments is None:
			raise forms.ValidationError("Please enter your comments.")
		elif len(comments) > 250:
			raise forms.ValidationError("Exceeds maximum characters: 250")
		return self.cleaned_data['comments']
	