from django.test import TestCase
from models import *
from django.utils import timezone
from django.core.urlresolvers import reverse
import datetime


# models test
class WhateverTest(TestCase):

    def create_Citizen(self, user_name="123456789", First_name="rosha", Last_name="rosha123", Address="admin",email="rosha1996@gmail.com",contact="9977105962"):
        return Citizens.objects.create(user_name=user_name, First_name=First_name, Last_name=Last_name, Address=Address, email=email, contact=contact)

    def test_Citizen_creation(self):
        w = self.create_Citizen()
        self.assertTrue(isinstance(w, Citizens))
        self.assertEqual("Citizens",w.__class__.__name__)


class WhateverTest2(TestCase):

    def create_Electionduration(self, election_year="2016",polling_date=datetime.date.today().strftime("%Y-%m-%d"),candidature_date=datetime.date.today().strftime("%Y-%m-%d")):
        return Election_duration.objects.create(election_year=election_year, polling_date=polling_date, candidature_date=candidature_date)

    def test_Election_duration_creation(self):
        w = self.create_Electionduration()
        self.assertTrue(isinstance(w, Election_duration))
        self.assertEqual("Election_duration",w.__class__.__name__)

class WhateverTest3(TestCase):

   
    def test_Candidates_creation(self):
        w=Candidates();
        self.assertEqual("Candidates",w.__class__.__name__)


class WhateverTest4(TestCase):
       
    def test_Login_data_creation(self):
       	w=Login_data();
        self.assertEqual("Login_data",w.__class__.__name__)
class WhateverTest5(TestCase):
       
    def test_Vote_Casted_creation(self):
        w=Vote_Casted();
        self.assertEqual("Vote_Casted",w.__class__.__name__)


#view test
class WhateverTest6(TestCase):
	def test_whatever_list_view(self):
	        url = reverse("Election.views.render_page")
	        resp = self.client.get(url)	
	        self.assertEqual(resp.status_code, 200)
class WhateverTest7(TestCase):
	def test_whatever_list_view(self):
	        url = reverse("Election.views.portal_render")
	        resp = self.client.get(url)	
	        self.assertEqual(resp.status_code, 200)
	       
class WhateverTest8(TestCase):
	def test_whatever_list_view(self):
	        url = reverse("Election.views.profile_render")
	        resp = self.client.get(url)	
	        self.assertEqual(resp.status_code, 200)
	       
class WhateverTest9(TestCase):
	def test_whatever_list_view(self):
	        url = reverse("Election.views.result_render")
	        resp = self.client.get(url)	
	        self.assertEqual(resp.status_code, 200)
	       
	       
class WhateverTest11(TestCase):
	def test_whatever_list_view(self):
	        url = reverse("Election.views.logout")
	        resp = self.client.get(url)	
	        self.assertEqual(resp.status_code, 200)
	        
	        
