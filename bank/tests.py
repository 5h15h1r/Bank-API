# bank/tests/test_views.py
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Banks, Branch
from .serializers import BankSerializer, BranchSerializer

class BankListTests(TestCase):
    def setUp(self):
        # Set up data for testing
        self.client = APIClient()
        self.bank1 = Banks.objects.create(bank_id=1, name="Bank1")
        self.bank2 = Banks.objects.create(bank_id=2, name="Bank2")
        # Add more data as needed

    def test_get_banks_list(self):
        response = self.client.get('/your-api-url/')  # Replace with your actual API URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)  # Assuming two banks are created in setUp

    def test_invalid_page_number(self):
        response = self.client.get('/your-api-url/', {'page': 0})  # Invalid page number
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Add more tests as needed

class BranchDetailTests(TestCase):
    def setUp(self):
        # Set up data for testing
        self.client = APIClient()
        self.branch1 = Branch.objects.create(ifsc="IFSC1", branch="Branch1")
        self.branch2 = Branch.objects.create(ifsc="IFSC2", branch="Branch2")
        # Add more data as needed

    def test_get_branch_by_ifsc(self):
        response = self.client.get(f'/your-api-url/{self.branch1.ifsc}/')  # Replace with your actual API URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ifsc'], self.branch1.ifsc)

    def test_get_branch_by_branch_name(self):
        response = self.client.get(f'/your-api-url/{self.branch2.branch}/')  # Replace with your actual API URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['branch'], self.branch2.branch)

    # Add more tests as needed
