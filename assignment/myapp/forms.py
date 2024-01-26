"""
Program:  Web Based Database Application
Filename: forms.py            
@author:  © Jack Styles             
Course:   BSc Digital Technology Solutions                     
Module:   Software Engineering and Agile             
Tutor:    Suraksha Neupane                         
@version: 1.0     
Date:     22/09/23
"""

import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ticket, Status, TicketType
from django.forms import ValidationError
import re


class NewUser(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "password1": forms.TextInput(attrs={"class": "form-control"}),
            "password2": forms.TextInput(attrs={"class": "form-control"}),
        }

    def save(self, commit: bool = True):
        """
        Saves the object to the datatable

        Parameters:
            commit (bool), default=True: Is the object being commited to the datatable

        Returns:
            user (NewUser): A User object, the object that has been entered into the datatable
        """
        user = super(NewUser, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
        return user


class AddTicket(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = (
            "ticket_title",
            "ticket_info",
            "assignee",
            "status",
            "type",
            "date_due",
        )

        widgets = {
            "ticket_title": forms.TextInput(attrs={"class": "form-control"}),
            "ticket_info": forms.Textarea(attrs={"class": "form-control"}),
            "assignee": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "type": forms.Select(attrs={"class": "form-control"}),
            "date_due": forms.DateInput(
                attrs={"class": "form-control"}, format="%d/%m/%y"
            ),
        }

    def clean_ticket_title(self) -> str:
        """
        Apply validation to the user input of the ticket title

        Returns:
            ticket_title (str): The validated ticket title
        """
        ticket_title = self.cleaned_data["ticket_title"]

        if not check_capital_letter(ticket_title):
            raise ValidationError(
                "Please enter the ticket title with the first letter as a Capital"
            )

        return ticket_title

    def save(self, commit: bool = True, **kwargs):
        """
        Commit the entry to the Ticket datatable

        Parameters:
            commit (bool), default=True: If the entry should be committed to the datatable
            **kwargs: Any extra arguments required. For this function, the webpage function is required

        Returns:
            ticket(AddTicket): The ticket object that is being committed
        """
        ticket = super(AddTicket, self).save(commit=False)
        ticket.date_reported = datetime.date.today()
        request = kwargs.pop("request", None)
        if request:
            ticket.reporter_id = request.user.id
        else:
            # Due to the user being logged in, this should never be reached. This is however a failsafe incase this happens.
            # If this is reached, the ticket will be unusable for the reporter, only an admin or assignee can edit this.
            ticket.reporter_id = 0

        if commit:
            ticket.save()
        return ticket


class AddStatus(forms.ModelForm):
    class Meta:
        model = Status
        fields = ("status_name", "status_description")

        widgets = {
            "status_name": forms.TextInput(attrs={"class": "form-control"}),
            "status_description": forms.Textarea(attrs={"class": "form-control"}),
        }

    def clean_status_name(self) -> str:
        """
        Apply validation to the Status Name that is entered by the user

        Returns:
            status_name (str): The validated Status Name that is to be committed
        """
        status_name = self.cleaned_data["status_name"]

        if not check_capital_letter(status_name):
            raise ValidationError(
                "Please enter the ticket title with the first letter as a Capital"
            )

        return status_name

    def save(self, commit: bool = True, **kwargs):
        """
        Commit the entry to the AddStatus datatable

        Parameters:
            commit (bool), default=true: Is the entry being committed
            **kwargs: Any extra arguments required. For this function, the webpage function is required

        Returns:
            status (AddStatus): The object of the entry being commited to the datatable
        """
        status = super(AddStatus, self).save(commit=False)
        request = kwargs.pop("request", None)
        if request:
            status.reporter_id = request.user.id
        else:
            # Due to the user being logged in, this should never be reached. This is however a failsafe incase this happens.
            # If this is reached, the ticket will be unusable for the reporter, only an admin or assignee can edit this.
            status.reporter_id = 0

        if commit:
            status.save()
        return status

class UpdateStatus(forms.ModelForm):
    class Meta:
        model = Status
        fields = ("status_description",)

        widgets = {
            "status_description": forms.Textarea(attrs={"class": "form-control"}),
        }

    def clean_status_name(self) -> str:
        """
        Apply validation to the Status Name that is entered by the user

        Returns:
            status_name (str): The validated Status Name that is to be committed
        """
        status_name = self.cleaned_data["status_name"]

        if not check_capital_letter(status_name):
            raise ValidationError(
                "Please enter the ticket title with the first letter as a Capital"
            )

        return status_name

    def save(self, commit: bool = True, **kwargs):
        """
        Commit the entry to the AddStatus datatable

        Parameters:
            commit (bool), default=true: Is the entry being committed
            **kwargs: Any extra arguments required. For this function, the webpage function is required

        Returns:
            status (AddStatus): The object of the entry being commited to the datatable
        """
        status = super(UpdateStatus, self).save(commit=False)
        request = kwargs.pop("request", None)
        if request:
            status.reporter_id = request.user.id
        else:
            # Due to the user being logged in, this should never be reached. This is however a failsafe incase this happens.
            # If this is reached, the ticket will be unusable for the reporter, only an admin or assignee can edit this.
            status.reporter_id = 0

        if commit:
            status.save()
        return status


class AddTicketType(forms.ModelForm):
    class Meta:
        model = TicketType
        fields = {"type_name", "type_description"}

        widgets = {
            "type_name": forms.TextInput(attrs={"class": "form-control"}),
            "type_description": forms.Textarea(attrs={"class": "form-control"}),
        }

    def clean_type_name(self) -> str:
        """
        Validate the type name entered by the user

        Returns:
            type_name (str): The validated type name
        """
        type_name = self.cleaned_data["type_name"]

        if not check_capital_letter(type_name):
            raise ValidationError(
                "Please enter the type name with the first letter as a Capital"
            )

        return type_name

    def save(self, commit: bool = True, **kwargs):
        """
        Commit the entry object to the TicketTyoe datatable

        Parameters:
            commit (bool): Is the object being committed to the datatable

        Returns:
            ticket_type (AddTicketType): The object of the entry being committed.
            **kwargs: Any extra arguments required. For this function, the webpage function is required
        """
        ticket_type = super(AddTicketType, self).save(commit=False)

        request = kwargs.pop("request", None)
        if request:
            ticket_type.reporter_id = request.user.id
        else:
            # Due to the user being logged in, this should never be reached. This is however a failsafe incase this happens.
            # If this is reached, the ticket will be unusable for the reporter, only an admin or assignee can edit this.
            ticket_type.reporter_id = 0
        if commit:
            ticket_type.save()
        return ticket_type
    
class UpdateTicketType(forms.ModelForm):
    class Meta:
        model = TicketType
        fields = {"type_description"}

        widgets = {
            "type_description": forms.Textarea(attrs={"class": "form-control"}),
        }

    def clean_type_name(self) -> str:
        """
        Validate the type name entered by the user

        Returns:
            type_name (str): The validated type name
        """
        type_name = self.cleaned_data["type_name"]

        if not check_capital_letter(type_name):
            raise ValidationError(
                "Please enter the type name with the first letter as a Capital"
            )

        return type_name

    def save(self, commit: bool = True, **kwargs):
        """
        Commit the entry object to the TicketTyoe datatable

        Parameters:
            commit (bool): Is the object being committed to the datatable

        Returns:
            ticket_type (AddTicketType): The object of the entry being committed.
            **kwargs: Any extra arguments required. For this function, the webpage function is required
        """
        ticket_type = super(UpdateTicketType, self).save(commit=False)

        request = kwargs.pop("request", None)
        if request:
            ticket_type.reporter_id = request.user.id
        else:
            # Due to the user being logged in, this should never be reached. This is however a failsafe incase this happens.
            # If this is reached, the ticket will be unusable for the reporter, only an admin or assignee can edit this.
            ticket_type.reporter_id = 0
        if commit:
            ticket_type.save()
        return ticket_type


def check_capital_letter(text: str) -> bool:
    """
    Checks a string to ensure it starts with a capital letter

    Parameters:
        text (str): The string to be examined

    Returns:
        (bool): Boolean value to denote if the regex returned a match
    """
    return bool(re.match(r"(^[A-Z]{1}[\w\s]*){1}", text))
