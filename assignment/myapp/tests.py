"""
Program:  Web Based Database Application
Filename: tests.py            
@author:  © Jack Styles             
Course:   BSc Digital Technology Solutions                     
Module:   Software Engineering and Agile             
Tutor:    Suraksha Neupane                         
@version: 1.0     
Date:     22/09/23
"""

from django.test import TestCase
from myapp.models import Status, TicketType
from django.urls import reverse
from myapp.views import (
    CreateStatusPage,
    ViewStatuses,
    ViewStatus,
    UpdateStatus,
    DeleteStatus,
    CreateTicketTypePage,
    ViewTypes,
    ViewType,
    UpdateTicketType,
    DeleteTicketType,
    CreateTicketPage,
    ViewTickets,
    ViewTicket,
    UpdateTicket,
    DeleteTicket,
)
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from myapp.forms import AddStatus, AddTicketType, Ticket, AddTicket
import datetime


class TestStatusModel(TestCase):
    def create_status_object(
        self,
        status_name: str = "Test Status",
        status_description: int = "This is a test status",
        reporter_id: int = 1,
    ) -> Status:
        """
        Creates a status database entry object for use in the test cases

        Tests can be written using the default values or values you have specified

        Parameters:
            status_name (str), default="Test Status": The name of the status
            status_descriptions (str), default="This is a test status": The description of the status
            reporter_id (int), default=1: The ID of the User that created the status

        returns:
            (Status): The object that would be a Database entry
        """
        return Status.objects.create(
            status_name=status_name,
            status_description=status_description,
            reporter_id=reporter_id,
        )

    def test_string_creation_for_forms(self):
        status = self.create_status_object()
        status_name = status.__str__()
        self.assertEqual(status_name, "Test Status")

    def create_user(self):
        """
        Creates a User for use in the test cases

        The following values are used:
            username - "Test Account"

            email - test@test.com

            password - TestPassword

        Use these credentials where Admin users are required after calling this function
        """
        self.user = User.objects.create_user(
            username="Test Account", email="test@test.com", password="TestPassword"
        )

    def get_response_code(self, url: str) -> int:
        """
        Gets the response code for a page on the application

        Parameters:
            url (str): The URL of the page to load

        Returns:
            (int): The response code for the URL
        """
        return self.client.get(url).status_code

    def test_create_status_view_response_code(self):
        self.create_user()
        self.client.login(username="Test Account", password="TestPassword")
        url = reverse(CreateStatusPage)
        self.assertEqual(self.get_response_code(url), 200)

    def test_view_statuses_view_response_code(self):
        self.create_user()
        self.client.login(username="Test Account", password="TestPassword")
        url = reverse(ViewStatuses)
        self.assertEqual(self.get_response_code(url), 200)

    def test_view_status_view_response_code(self):
        self.create_status_object()
        self.create_user()
        self.client.login(username="Test Account", password="TestPassword")
        url = reverse(ViewStatus, args=["Test Status"])
        self.assertEqual(self.get_response_code(url), 200)

    def test_update_status_view_response_code(self):
        self.create_status_object()
        self.create_user()
        self.client.login(username="Test Account", password="TestPassword")
        url = reverse(UpdateStatus, args=["Test Status"])
        self.assertEqual(self.get_response_code(url), 200)

    def create_super_user(self):
        """
        Create an admin user for use in the test cases.

        The following values are used:
            username - "Test Account Admin"

            email - testadmin@test.com

            password - TestPassword

        Use these credentials where Admin users are required after calling this function
        """
        self.user = User.objects.create_superuser(
            username="Test Account Admin",
            email="testadmin@test.com",
            password="TestPassword",
        )

    def test_delete_status_view_response_code(self):
        self.create_status_object()
        self.create_super_user()
        self.client.login(username="Test Account Admin", password="TestPassword")
        url = reverse(DeleteStatus, args=["Test Status"])
        self.assertEqual(self.get_response_code(url), 200)

    def create_status_form(
        self, status_name: str, status_description: str
    ) -> AddStatus:
        """
        Creates a Status form for use in the application

        Parameters:
            status_name (str): Name of the status
            status_description (str): Description of the status

            Returns:
                (AddStatus): The form for the Status object
        """
        data = {"status_name": status_name, "status_description": status_description}
        return AddStatus(data=data)

    def test_add_status_form_when_name_does_not_have_capital_letter_at_start_of_type_name(
        self,
    ):
        form = self.create_status_form("test Status", "This is a test")
        self.assertFalse(form.is_valid())

    def test_add_status_form_when_name_does_not_exist(self):
        form = self.create_status_form("", "This is a test")
        self.assertFalse(form.is_valid())

    def test_add_status_form_when_name_has_capital_letter_at_start_of_type_name(self):
        form = self.create_status_form("Test Status", "This is a test")
        result = form.is_valid()
        self.assertTrue(result)


class TestTicketTypeModel(TestCase):
    def create_ticket_type_object(
        self,
        type_name: str = "Test Ticket Type",
        type_description: str = "This is a test description",
        reporter_id: int = 1,
    ) -> TicketType:
        """
        Creates a Ticket Type database entry object for use in the test cases

        Tests can be written using the default values or values you have specified

        Parameters:
            type_name (str), default="Test Ticket Type": The name of the Ticket Type
            type_description (str), default="This is a test description": The description of the Ticket Type
            reporter_id (int), default=1: The ID of the User that created the Ticket Type

        returns:
            (TicketType): The object that would be a Database entry
        """
        return TicketType.objects.create(
            type_name=type_name,
            type_description=type_description,
            reporter_id=reporter_id,
        )

    def test_string_creation(self):
        ticket_type = self.create_ticket_type_object()
        ticket_type_name = ticket_type.__str__()
        self.assertEqual(ticket_type_name, "Test Ticket Type")

    def create_user(self):
        """
        Creates a User for use in the test cases

        The following values are used:
            username - "Test Account"

            email - test@test.com

            password - TestPassword

        Use these credentials where Admin users are required after calling this function
        """
        self.user = User.objects.create_user(
            username="Test Account", email="test@test.com", password="TestPassword"
        )

    def get_response_code(self, url: str) -> int:
        """
        Gets the response code for a page on the application

        Parameters:
            url (str): The URL of the page to load

        Returns:
            (int): The response code for the URL
        """
        return self.client.get(url).status_code

    def test_create_ticket_type_view_response_code(self):
        self.create_user()
        self.client.login(username="Test Account", password="TestPassword")
        url = reverse(CreateTicketTypePage)
        self.assertEqual(self.get_response_code(url), 200)

    def test_view_statuses_view_response_code(self):
        self.create_user()
        self.client.login(username="Test Account", password="TestPassword")
        url = reverse(ViewTypes)
        self.assertEqual(self.get_response_code(url), 200)

    def test_view_status_view_response_code(self):
        self.create_ticket_type_object()
        self.create_user()
        self.client.login(username="Test Account", password="TestPassword")
        url = reverse(ViewType, args=["Test Ticket Type"])
        self.assertEqual(self.get_response_code(url), 200)

    def test_update_status_view_response_code(self):
        self.create_ticket_type_object()
        self.create_user()
        self.client.login(username="Test Account", password="TestPassword")
        url = reverse(UpdateTicketType, args=["Test Ticket Type"])
        self.assertEqual(self.get_response_code(url), 200)

    def create_super_user(self):
        """
        Create an admin user for use in the test cases.

        The following values are used:
            username - "Test Account Admin"

            email - testadmin@test.com

            password - TestPassword

        Use these credentials where Admin users are required after calling this function
        """
        self.user = User.objects.create_superuser(
            username="Test Account Admin",
            email="testadmin@test.com",
            password="TestPassword",
        )

    def test_delete_status_view_response_code(self):
        self.create_ticket_type_object()
        self.create_super_user()
        self.client.login(username="Test Account Admin", password="TestPassword")
        url = reverse(DeleteTicketType, args=["Test Ticket Type"])
        self.assertEqual(self.get_response_code(url), 200)

    def create_ticket_type_form(
        self, type_name: str, type_description: str
    ) -> AddTicketType:
        """
        Creates a Ticket Type form for use in the application

        Parameters:
            type_name (str): Name of the Ticket Type
            type_description (str): Description of the Ticket Type

            Returns:
                (AddTicketType): The form for the TicketType object
        """
        data = {"type_name": type_name, "type_description": type_description}
        return AddTicketType(data=data)

    def test_add_ticket_type_form_when_name_does_not_have_capital_letter_at_start_of_string(
        self,
    ):
        form = self.create_ticket_type_form("test Type", "This is a test")
        self.assertFalse(form.is_valid())

    def test_add_status_form_when_name_does_not_exist(self):
        form = self.create_ticket_type_form("", "This is a test")
        self.assertFalse(form.is_valid())

    def test_add_status_form_when_name_has_capital_letter_at_start(self):
        form = self.create_ticket_type_form("Test Type", "This is a test")
        result = form.is_valid()
        self.assertTrue(result)


class TestTicketModel(TestCase):
    status_model = TestStatusModel()
    type_model = TestTicketTypeModel()

    def create_ticket_object(self, ticket_title: str = "Test Ticket Title") -> Ticket:
        """
        Creates a ticket database entry object for use in the test cases

        Tests can be written using the default values or values you have specified

        Parameters:
            ticket_title (str), default="Test Ticket Title": The name of the Ticket

        returns:
            (Ticket): The object that would be a Database entry
        """
        status_object = self.status_model.create_status_object()
        type_object = self.type_model.create_ticket_type_object()
        return Ticket.objects.create(
            ticket_title=ticket_title,
            date_reported=datetime.date.today(),
            status_id=status_object,
            type_id=type_object,
            reporter_id=1,
        )

    def create_user(self):
        """
        Creates a User for use in the test cases

        The following values are used:
            username - "Test Account"

            email - test@test.com

            password - TestPassword

        Use these credentials where Admin users are required after calling this function
        """
        self.user = User.objects.create_user(
            username="Test Account", email="test@test.com", password="TestPassword"
        )

    def get_response_code(self, url: str) -> int:
        """
        Gets the response code for a page on the application

        Parameters:
            url (str): The URL of the page to load

        Returns:
            (int): The response code for the URL
        """
        return self.client.get(url).status_code

    def test_create_ticket_view_response_code(self):
        self.create_user()
        self.client.login(username="Test Account", password="TestPassword")
        url = reverse(CreateTicketPage)
        self.assertEqual(self.get_response_code(url), 200)

    def test_view_tickets_view_response_code(self):
        self.create_user()
        self.client.login(username="Test Account", password="TestPassword")
        url = reverse(ViewTickets)
        self.assertEqual(self.get_response_code(url), 200)

    def test_view_ticket_view_response_code(self):
        self.create_ticket_object()
        self.create_user()
        self.client.login(username="Test Account", password="TestPassword")
        ticket = Ticket.objects.get(ticket_title="Test Ticket Title")
        url = reverse(ViewTicket, args=[ticket.ticket_id])
        self.assertEqual(self.get_response_code(url), 200)

    def test_update_ticket_view_response_code(self):
        self.create_ticket_object()
        self.create_user()
        self.client.login(username="Test Account", password="TestPassword")
        ticket = Ticket.objects.get(ticket_title="Test Ticket Title")
        url = reverse(UpdateTicket, args=[ticket.ticket_id])
        self.assertEqual(self.get_response_code(url), 200)

    def create_super_user(self):
        """
        Create an admin user for use in the test cases.

        The following values are used:
            username - "Test Account Admin"

            email - testadmin@test.com

            password - TestPassword

        Use these credentials where Admin users are required after calling this function
        """
        self.user = User.objects.create_superuser(
            username="Test Account Admin",
            email="testadmin@test.com",
            password="TestPassword",
        )

    def test_delete_ticket_view_response_code(self):
        self.create_ticket_object()
        self.create_super_user()
        self.client.login(username="Test Account Admin", password="TestPassword")
        ticket = Ticket.objects.get(ticket_title="Test Ticket Title")
        url = reverse(DeleteTicket, args=[ticket.ticket_id])
        self.assertEqual(self.get_response_code(url), 200)

    def create_ticket_form(self, ticket_title: str) -> AddTicket:
        """
        Creates a Ticket Type form for use in the application

        Parameters:
            ticket_title (str): Name of the Ticket

            Returns:
                (AddTicket): The form for the Status object
        """
        data = {
            "ticket_title": ticket_title,
            "status": self.status_model.create_status_object(),
            "type": self.type_model.create_ticket_type_object(),
        }
        return AddTicket(data=data)

    def test_add_ticket_form_when_name_does_not_have_capital_letter_at_start_of_string(
        self,
    ):
        form = self.create_ticket_form("test Ticket")
        self.assertFalse(form.is_valid())

    def test_add_status_form_when_name_does_not_exist(self):
        form = self.create_ticket_form("")
        self.assertFalse(form.is_valid())

    def test_add_status_form_when_name_has_capital_letter_at_start(self):
        form = self.create_ticket_form("Test Ticket")
        result = form.is_valid()
        self.assertTrue(result)
