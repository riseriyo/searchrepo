# stdlib imports
import logging

logging.basicConfig(filename='log_formsregistration.log', level=logging.info)


# core django imports
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm # ability to pass some model to the form

# 3rd party imports

# project imports
from .models import UserProfile
from .models import Position

POSITIONS = [
				('10', 'Apprentice'),
				('20', 'Journeyman'),
				('30', 'Master'),
				('40', 'Other DIYer')
				]

#****************************************************
# Create custom form for creating new user profiles
# make password input invisible
#*****************************************************
class RegistrationForm(ModelForm):
	username	= forms.CharField(label=(u'Username'), widget=forms.TextInput({"placeholder": "Username"}))
	email		= forms.EmailField(label=(u'Email Address'), widget=forms.TextInput({"placeholder": "Email Address"})) 
	position	= forms.ChoiceField(label=(u'Position'), widget=forms.Select, choices=POSITIONS)
	password	= forms.CharField(label=(u'Password'), widget=forms.PasswordInput(attrs={"placeholder": "Password"}, render_value=False) )
	cpassword	= forms.CharField(label=(u'Confirm Password'), widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}, render_value=False))
	
	class Meta:
		''' automatically takes the model, UserProfile, and creates a form out of the fields of the model'''
		model = UserProfile
		fields = ('username', 'email', 'position', 'password')
		
	def clean_username(self):
		''' used with form.is_valid() and will take the field value of username of the model, RegistrationForm'''
		username = self.cleaned_data['username']
		try:
			User.objects.get(username=username) # find any Users with the same username
		except User.DoesNotExist:
			# if new user does not exist in Users account, then ok name to use
			return username
		raise forms.ValidationError("That username is already taken, please select another.")
	
	def clean_email(self):
		'''used with with form.is_valid() and will take the field value of email of the model, RegistrationForm'''
		email = self.cleaned_data['email']
		try:
			User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError("That email address has already been used. Please use another one.")

	
	def clean_position(self):
		position_pk = self.cleaned_data['position']
		logging.info("position=%s"%position_pk) 
		try:
			return Position.objects.get(pk=position_pk)
			#return 
		except Position.DoesNotExist:
			#pass
			raise forms.ValidationError("Please select a position.")
	
	def clean(self):
		'''' method has access to remaining variables in the form'''
		print("clean method")
		password = self.cleaned_data.get('password', None)
		cpassword = self.cleaned_data.get('cpassword', None)
		if password and cpassword and (password == cpassword):
			print("in if")
			return self.cleaned_data
		else:
			print("mismatched")
			raise forms.ValidationError("The passwords did not match. Please try again.")
		