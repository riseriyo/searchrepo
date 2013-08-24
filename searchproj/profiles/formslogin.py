# stdlib imports

# core django imports
from django import forms

# 3rd party imports

# project app imports

class LoginForm(forms.Form):
	'''login form for login page'''
	username		= forms.CharField(label=(u'Username'), widget=forms.TextInput({"placeholder": "Username", 'tabindex':'1'}))
	password		= forms.CharField(label=(u'Password'), widget=forms.PasswordInput(attrs={"placeholder": "Password", 'tabindex': '2'}, render_value=False))
	