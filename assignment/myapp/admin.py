"""
Program:  Web Based Database Application
Filename: admin.py            
@author:  © Jack Styles             
Course:   BSc Digital Technology Solutions                     
Module:   Software Engineering and Agile             
Tutor:    Suraksha Neupane                         
@version: 1.0     
Date:     22/09/23
"""

from django.contrib import admin
from myapp.models import Status, TicketType, Ticket

admin.site.register(Status)
admin.site.register(TicketType)
admin.site.register(Ticket)
