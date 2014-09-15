from django.db import models
from django.utils import timezone


class DictionaryWordQuerySet(models.QuerySet):
    def search(self, superstring):
        """
        Takes a 'superstring' such as 'hello, world' and will return all
        words that are substrings of the superstring. For example, a search
        for 'hello, world', might return 'hello' and 'world'. In addition,
        the search is in order of longest word to shortest word.
        """ 
        # Note: This is sqlite3 dependent -- implementation may differ slightly depending on db engine
        return self.extra(where=["'%s' LIKE '%%' || word || '%%'" % superstring])
    
    def order_by_word_length(self):
        """Returns dictionary words in order of their length, longest first.""" 
        return self.extra(select={'length': 'Length(word)'}).order_by('-length')


class DictionaryWord(models.Model):
    objects = DictionaryWordQuerySet.as_manager()
    word = models.TextField(db_index=True, unique=True)

    def __str__(self):
        return u'%s' % self.word


class ShortURLManager(models.Manager):
    def create_short_url(self, original_url):
        # Search for a word that is not taken that is part of the original url
        word = DictionaryWord.objects.search(original_url).filter(shorturl__isnull=True)\
            .extra(select={'length': 'Length(word)'}).order_by('-length').first()
        if not word:
            # If we could not find a word, we look for a random, free word 
            word = DictionaryWord.objects.filter(shorturl__isnull=True).order_by('?').first()
        if not word:
            # If we cannot find a free word, we remove the oldest short url and use its dictionary word
            word = DictionaryWord.objects.order_by('-shorturl__time_created').last()
            word.shorturl.delete()
        return self.create(word=word, original_url=original_url, time_created=timezone.now())


class ShortURL(models.Model):
    objects = ShortURLManager()
    time_created = models.DateTimeField(default=timezone.now())
    word = models.OneToOneField(DictionaryWord, primary_key=True)
    original_url = models.TextField()
    
    def __str__(self):
       return u'%s (%s)' % (self.word.word, self.original_url)
