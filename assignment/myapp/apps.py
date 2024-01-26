"""
Program:  Web Based Database Application
Filename: apps.py            
@author:  © Jack Styles             
Course:   BSc Digital Technology Solutions                     
Module:   Software Engineering and Agile             
Tutor:    Suraksha Neupane                         
@version: 1.0     
Date:     22/09/23
"""

from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myapp"
