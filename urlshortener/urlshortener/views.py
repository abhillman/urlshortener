from django.core.context_processors import csrf
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.views.generic import View
from django.http import HttpResponse
from .forms import ShortURLForm
from .models import ShortURL

def resolve_short_url(request, short_url):
    short_url = get_object_or_404(ShortURL, word__word=short_url)
    return redirect(short_url.original_url)

class CreateShortURL(View):
    def return_form(self, request, form):
        context = {'shorturl_form': form}
        context.update(csrf(request))
        return render_to_response('create_a_url.html', context)

    def get(self, request):
        return self.return_form(request, ShortURLForm())

    def post(self, request):
        shorturl_form = ShortURLForm(request.POST)
        if shorturl_form.is_valid():
            short_url = ShortURL.objects.create_short_url(shorturl_form.data['original_url'])
        else:
            return self.return_form(request, shorturl_form)
        return HttpResponse(short_url.word.word)
