from django.shortcuts import render_to_response
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from .models import Note


from .formsnotessearch import NotesSearchForm

#def notessearch(request):
#	form = NotesSearchForm(request.GET)
#	notes = form.search()
#	return render_to_response("search.html", {"notes": notes})

'''
class NotesList(ListView):
	paginate_by = 10
	model = Note

	def get_queryset(self):
		term = self.request.REQUEST.get('search')

		if term:
			return self.model.objects.filter(text_icontains=term)
		else:
			return self.model.objects.all()
'''