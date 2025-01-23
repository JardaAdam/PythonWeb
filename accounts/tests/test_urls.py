from unittest import skip

from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from config.settings import testing


class DebugModeTest(TestCase):
    @skip
    def test_debug_is_false(self):
        # This test ensures that DEBUG is set to False
        self.assertFalse(testing.DEBUG, "DEBUG mode should be False in testing configuration.")

class PageNotFoundTest(SimpleTestCase):

    def test_404_page(self):
        response = self.client.get('/some/non-existent/url/')
        self.assertEqual(response.status_code, 404)
        # Ověřte, že se používá správná šablona
        self.assertTemplateUsed(response, '404.html')