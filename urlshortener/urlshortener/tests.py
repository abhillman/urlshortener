from django.test import TestCase
from .models import DictionaryWord
from .models import ShortURL


class URLShortenerTestCase(TestCase):
    def create_words(self, words=["lawsuit", "interest", "applesauce",]):
        self.words = ["lawsuit", "interest", "applesauce", ]
        DictionaryWord.objects.bulk_create([DictionaryWord(word=word) for word in self.words])


class DictionaryWordTestCase(URLShortenerTestCase):
    def setUp(self):
        self.create_words()

    def test_search_query(self):
        """Helps ensure DictionaryWord.objects.search method functions properly."""
        # Search for words based on URL string
        found_words = list(DictionaryWord.objects.search("http://techcrunch.com/2012/12/28/pinterest-lawsuit/")\
                           .values_list('word', flat=True))

        # Make sure we found the correct words
        self.assertEquals(set(found_words), set(("lawsuit", "interest")), "incorrect words found")

    def test_order_query(self):
        """Helps ensure DictionaryWord.objects.order_by_word_length functions properly."""
        pass
        expected_ordered_words = self.words[:] 
        expected_ordered_words.sort(key=lambda word: -len(word))
        observed_ordered_words = list(DictionaryWord.objects.order_by_word_length().values_list('word', flat=True))
        self.assertEqual(expected_ordered_words, observed_ordered_words)


class ShortURLTestCase(URLShortenerTestCase):
    def setUp(self):
        self.create_words()

    def test_create_short_url(self):
        """We check to make sure the logic to create a short url is in order."""
        short_url = ShortURL.objects.create_short_url("http://techcrunch.com/2012/12/28/pinterest-lawsuit/")
        self.assertEqual(short_url.word.word, 'interest')

        short_url = ShortURL.objects.create_short_url("http://techcrunch.com/2012/12/28/pinterest-lawsuit/")
        self.assertEqual(short_url.word.word, 'lawsuit')

        short_url = ShortURL.objects.create_short_url("http://techcrunch.com/2012/12/28/pinterest-lawsuit/")
        self.assertEqual(short_url.word.word, 'applesauce')

        short_url = ShortURL.objects.create_short_url("http://techcrunch.com/2012/12/28/pinterest-lawsuit/")
        self.assertEqual(short_url.word.word, 'interest')

        short_url = ShortURL.objects.create_short_url("http://techcrunch.com/2012/12/28/pinterest-lawsuit/")
        self.assertEqual(short_url.word.word, 'lawsuit')
        
        short_url = ShortURL.objects.create_short_url("http://techcrunch.com/2012/12/28/pinterest-lawsuit/")
        self.assertEqual(short_url.word.word, 'applesauce')
