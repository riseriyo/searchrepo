from django import forms
from django.views.generic import CreateView

from .models import UserProfile

class UserProfileMixin(object):
	def action(self):
		msg = "{0} needs to be filled out.".format(self.__class__)
		raise NotImplementedError(msg)

	def form_valid(self,form):
		msg = "UserProfile has been {0}.".format(self.action)
		messages.info(self.request, msg)
		return super(UserProfileMixin, self).form_valid(form)
