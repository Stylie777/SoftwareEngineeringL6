"""
Program:  Web Based Database Application
Filename: models.py            
@author:  © Jack Styles             
Course:   BSc Digital Technology Solutions                     
Module:   Software Engineering and Agile             
Tutor:    Suraksha Neupane                         
@version: 1.0     
Date:     22/09/23
"""

from django.db import models
from django.contrib.auth.models import User


class Status(models.Model):
    status_name = models.CharField(max_length=20, primary_key=True, null=False)
    status_description = models.CharField(max_length=100, blank=True, null=True)
    reporter_id = models.PositiveIntegerField(null=False, default=0)

    def __str__(self) -> str:
        """
        Used to return formatted values from an entry to display information to the user in a more readable way
        Returns:
            self.status_name: The name of the status objects
        """
        return self.status_name


class TicketType(models.Model):
    type_name = models.CharField(max_length=20, null=False, primary_key=True)
    type_description = models.CharField(max_length=100, blank=True, null=True)
    reporter_id = models.PositiveIntegerField(null=False, default=0)

    def __str__(self):
        """
        Used to return formatted values from an entry to display information to the user in a more readable way
        Returns:
            self.type: The name of the type objects
        """
        return self.type_name


class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True, null=False)
    ticket_title = models.CharField(max_length=100, null=False)
    ticket_info = models.CharField(max_length=2000, blank=True, null=True)
    assignee = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    type = models.ForeignKey(TicketType, on_delete=models.CASCADE, null=True)
    date_reported = models.DateField(null=False)
    date_due = models.DateField(blank=True, null=True)
    reporter_id = models.PositiveIntegerField(null=False, default=0)
