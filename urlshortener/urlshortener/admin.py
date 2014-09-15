from django.contrib import admin
from .models import DictionaryWord
from .models import ShortURL 

admin.site.register(DictionaryWord)
admin.site.register(ShortURL)