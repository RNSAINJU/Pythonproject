from django.test import TestCase
from django.urls import resolve, reverse
from .views import partner_list_view

def PartnerTests(TestCase):
    def test_partner_view_status_code(self):
        url=reverse('partners')
        response=self.client.get(url)
        self.assertEquals(response.status_code, 200)

def test_partner_url_resolves_partner_view(self):
    view=resolve('/')
    self.assertEquals(view.func ,partner_list_view)
