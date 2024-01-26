"""
Program:  Web Based Database Application
Filename: urls.py            
@author:  © Jack Styles             
Course:   BSc Digital Technology Solutions                     
Module:   Software Engineering and Agile             
Tutor:    Suraksha Neupane                         
@version: 1.0     
Date:     22/09/23
"""

"""
URL configuration for assignment project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "myapp"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.HomePage, name="Home"),
    path("register/", views.RegisterPage, name="Register"),
    path("login/", views.LoginPage, name="Login"),
    path("logout/", views.LogoutPage, name="Logout"),
    path("create_ticket/", views.CreateTicketPage, name="Create Ticket"),
    path("create_status/", views.CreateStatusPage, name="Create Status"),
    path("create_ticket_type/", views.CreateTicketTypePage, name="Create Ticket Type"),
    path("view_tickets/", views.ViewTickets, name="View Tickets"),
    path("view_ticket/<int:id>", views.ViewTicket, name="View Ticket"),
    path("view_statuses/", views.ViewStatuses, name="View Statuses"),
    path("view_status/<str:status_name>", views.ViewStatus, name="View Status"),
    path("view_types/", views.ViewTypes, name="View Types"),
    path("view_type/<str:type_name>", views.ViewType, name="View Type"),
    path("update_ticket/<int:id>", views.UpdateTicket, name="Update Ticket"),
    path("update_status/<str:status_name>", views.UpdateStatusPage, name="Update Status"),
    path("update_type/<str:type_name>", views.UpdateTicketTypePage, name="Update Type"),
    path("delete_ticket/<int:id>", views.DeleteTicket, name="Delete Ticket"),
    path("delete_status/<str:status_name>", views.DeleteStatus, name="Delete Status"),
    path("delete_type/<str:type_name>", views.DeleteTicketType, name="Delete Type"),
    path("readme/", views.ReadmePage, name="Readme"),
]

urlpatterns += staticfiles_urlpatterns()
