'''
Created on Nov 21, 2012

@author: rise
'''
# stdlib imports
import datetime
import random
import hashlib 

# core django imports
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.timezone import utc

# 3rd party imports

# project imports
from .formsregistration import RegistrationForm
from profiles.models import UserProfile

def Registration(request):
	'''register a user as a Rooroo member'''
	if request.user.is_authenticated():
		# already registered and logged in
		return HttpResponseRedirect('index.html')

	if request.method == 'POST':
		# submission of customized form
		form = RegistrationForm(request.POST)
		if form.is_valid():
			try:
				# all fields in form are filled out, unique username, correct email format, matching passwords
				new_user = User.objects.create_user(username=form.cleaned_data['username'], # pass value in username field in form
											email=form.cleaned_data['email'],
											password=form.cleaned_data['password'])
			except Exception as e:
				print e
				import traceback
				import sys
				traceback.print_exc(file=sys.stdout)
			else:
				new_user.is_active = False
				new_user.save() # save form input into a user object for logging into account

			finally:
				# build the activation key for new user profile account; expires after 2 days
				salt = hashlib.sha1(str(random.random())).hexdigest()[:5] 
				activation_key = hashlib.sha1(salt+new_user.username).hexdigest() 
				key_expires = datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(2)

			try:
				# create manual UserProfile object
				print"userprofile"
				new_userprofile = UserProfile(user=new_user, activation_key=activation_key, key_expires=key_expires, position=form.cleaned_data['position'])
			except Exception as e:
				print e
				import traceback
				traceback.print_exc(file=sys.stdout)
				# error: new user object created but not new user profile;
				# make new user inactive to avoid breaking foreign keys to users, then delete
				new_user.is_active = False
				new_user.delete()
				return render_to_response('registration/registration_form.html', { 'form': form }, context_instance=RequestContext(request))
			else:
				print"in else"
				new_userprofile.save()

				email_subject = "REQUEST: Activate Your RooRoo Account"
				email_body = "Hello %s,\n\nTo activate your account, please click on the link within 48 hours:\nhttp://localhost:8000/accounts/confirm/%s \n\nNote: This is an auto-generated e-mail message; please do not reply."%(
																						new_user.username,
																						new_userprofile.activation_key)
				#https://mol-flipbook.sbgrid.org/accounts/confirm/%s \n\nNote: This is an auto-generated e-mail message, please do not reply."%(

				from_sender = 'molecularflipbook@gmail.com'
				to_recipient = [new_user.email]

				try:
					send_mail(email_subject, email_body, from_sender, to_recipient)
				except Exception as e:
					print e
					traceback.print_exc(file=sys.stdout)
				finally:
					# render html page stating email is sent out to user
					return render_to_response('registration/registration_complete.html', context_instance=RequestContext(request))
		else:
			# form not valid, try again
			print("User form is bound:{0} errors:{1}").format(form.is_bound, form.errors)
			return render_to_response('registration/registration_form.html', { 'form': form }, context_instance=RequestContext(request))

	else:
		'''user is not submitting the form, show them a blank registration form'''
		form = RegistrationForm()
		# add form to context
		context = { 'form': form }
		return render_to_response('registration/registration_form.html', context, context_instance=RequestContext(request))

def confirm(request, activation_key):
	'''send activation link via email address of user'''
	if request.user.is_authenticated():
		return render_to_response('registration/activation_complete.html', context_instance=RequestContext(request))
	try: 
		new_userprofile = get_object_or_404(UserProfile, activation_key=activation_key)
	except UserProfile.DoesNotExist:
		raise Http404
	else:
		if new_userprofile.key_expires < datetime.datetime.utcnow().replace(tzinfo=utc):
			return render_to_response('registration/activation_incomplete.html', {'expired': True}, context_instance=RequestContext(request))
		user_account = new_userprofile.user
		user_account.is_active = True
		user_account.save()
		return render_to_response('registration/activation_complete.html', {'success': True}, context_instance=RequestContext(request))


