'''
Created on Nov 21, 2012

@author: rise
'''
# stdlib imports

# core django imports
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response

# 3rd party imports

# project imports
from .formslogin import LoginForm

# *********************************************
# based on code by: 
# http://hackedexistence.com/project/django/video7-userauthentication-2.html
# *********************************************
def loginView(request):
	'''check if currently logged-in user is authenticated; check if user is a MFB member and active'''
	if request.method != 'POST' and request.user.is_authenticated() == True:
#		import pdb
#		pdb.set_trace()
		return HttpResponseRedirect('/profile/my_dashboard/')
	
	if request.method == 'POST' and (request.user.is_authenticated()) == False:
		form = LoginForm(request.POST)
		context = { 'form': form }
		if form.is_valid():
			# pull out info from form and assign them to variables
			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
			if user is not None:
				try:
					if user.is_active:
						login(request, user)
						return HttpResponseRedirect('/profile/my_dashboard/')
					else: # user needs to activate their account status
						return HttpResponseRedirect('/login/')
				except Exception as e: 
					print e
					import traceback, sys
					traceback.print_exc(file=sys.stdout)
			else:
				# return to login page due to error with credentials
				return render_to_response('registration/login.html', context, context_instance=RequestContext(request))
		else:
			# if form is not valid, go to login page
			return render_to_response('registration/login.html', context, context_instance=RequestContext(request))
	else: 
		# user is not submitting the form, show the login form
		form = LoginForm()
		context = { 'form': form }
		return render_to_response('registration/login.html', context, context_instance=RequestContext(request))
	
def logoutView(request):
	''' display message stating user has been successfully logged out of their account '''
	logout(request)
	return render_to_response("registration/logged_out.html", context_instance=RequestContext(request))
