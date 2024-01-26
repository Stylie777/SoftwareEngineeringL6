"""
Program:  Web Based Database Application
Filename: views.py            
@author:  © Jack Styles             
Course:   BSc Digital Technology Solutions                     
Module:   Software Engineering and Agile             
Tutor:    Suraksha Neupane                         
@version: 1.0     
Date:     22/09/23
"""

"""
References:
The markdown python library is used in this module to convert the README.md to HTML for display on the webpage.

Markdown (2023) Python-Markdown 3.4.4 Documentation. Available at: https://python-markdown.github.io (Accessed: 22 September 2023)
"""

from django.shortcuts import render, redirect
from .forms import NewUser, AddTicket, AddStatus, AddTicketType, UpdateStatus, UpdateTicketType
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Ticket, Status, TicketType
from django.contrib.auth.models import User
import markdown


def HomePage(request):
    """
    Renders the home page

    Parameters:
        request: The webpage request

    Returns:
        : Render of the webpage using the Django template
    """

    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(assignee=request.user.id)

        return render(
            request,
            "myapp/home.html",
            context={"tickets": tickets if tickets else None},
        )
    return render(request, "myapp/home.html")


def ReadmePage(request):
    """
    Renders the Readme page. Uses `markdown` to take the README.md of the application and generate
    a HTML page.

    Parameters:
        request: The webpage request

    Returns
        : Render of the webpage using the django template

    """

    # Markdown (2023) - START
    markdown.markdownFromFile(
        input=r"README.md", output=r"myapp/templates/myapp/readme_contents.html"
    )
    # Markdown (2023) - END

    return render(request, "myapp/readme.html")


def RegisterPage(request):
    """
    Renders the registration page

    Parameters:
        request: The webpage request

    Returns:
        : Render of the webpage using the django template
    """
    if request.method == "POST":
        form = NewUser(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration Successful")
            return redirect("Home")
        messages.error(
            request, "Registration Unsuccessful, please proivde valid information."
        )

    form = NewUser()
    return render(
        request=request,
        template_name="myapp/register.html",
        context={"register_form": form},
    )


def LoginPage(request):
    """
    Renders the login page

    Parameters:
        request: The webpage request

    Returns:
        : Render of the webpage using the django template
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect("Home")
            else:
                messages.error(
                    request, "Invalid Username or Password. Please try again."
                )
    form = AuthenticationForm()
    return render(
        request=request, template_name="myapp/login.html", context={"login_form": form}
    )


@login_required(login_url="/login")
def LogoutPage(request):
    """
    Renders the logout page

    Parameters:
        request: The webpage request

    Returns:
        : Render of the webpage using the django template
    """
    logout(request)
    messages.info(request, "You have logged out.")
    return redirect("Home")


@login_required(login_url="/login")
def CreateTicketPage(request):
    """
    Renders the create ticket page

    Parameters:
        request: The webpage request

    Returns:
        : Render of the webpage using the django template
    """
    form = AddTicket(request.POST)

    if form.is_valid():
        form.save(request=request)
        messages.success(request, message="Ticket logged")
        return redirect("Home")

    return render(
        request, "myapp/form.html", context={"form": form, "title": "Create Ticket"}
    )


@login_required(login_url="/login")
def CreateStatusPage(request):
    """
    Renders the create status page

    Parameters:
        request: The webpage request

    Returns:
        : Render of the webpage using the django template
    """
    form = AddStatus(request.POST)

    if form.is_valid():
        form.save(request=request)
        messages.success(request, "Status Type Created")
        return redirect("Home")

    return render(
        request, "myapp/form.html", context={"form": form, "title": "Create Status"}
    )


@login_required(login_url="/login")
def CreateTicketTypePage(request):
    """
    Renders the create ticket type page

    Parameters:
        request: The webpage request

    Returns:
        : Render of the webpage using the django template
    """
    form = AddTicketType(request.POST)

    if form.is_valid():
        form.save(request=request)
        messages.success(request, "Ticket Type Created")
        return redirect("Home")

    return render(
        request,
        "myapp/form.html",
        context={"form": form, "title": "Create Ticket Type"},
    )


def can_user_update_ticket(request, ticket: Ticket) -> bool:
    """
    Performs check to see if a user can update a ticket

    Parameters:
        request: The webpage request, used to extract the current users information
        ticket (Ticket): The ticket that the user is wishing to update

    Returns:
        (bool): Denotes if the user can update the ticket
    """
    try:
        return (
            request.user.id == ticket.reporter_id
            or request.user.is_superuser
            or request.user.id == ticket.assignee.id
        )
    except:
        # If the above fails, the application assumes that the user cannot edit this ticket. This is a failsafe to prevent unauthorised updating on an entry
        return False


@login_required(login_url="/login")
def ViewTickets(request):
    """
    Renders the view tickets page

    Parameters:
        request: The webpage request

    Returns:
        : Render of the webpage using the django template
    """
    items = []

    for ticket in Ticket.objects.all():
        try:
            reporter = User.objects.get(id=ticket.reporter_id).username
        except:
            reporter = "None"

        can_update = can_user_update_ticket(request, ticket)

        items.append({"ticket": ticket, "reporter": reporter, "can_update": can_update})

    return render(request, "myapp/display_tickets.html", {"items": items})


@login_required(login_url="/login")
def ViewTicket(request, id: int):
    """
    Renders the view ticket page

    Parameters:
        request: The webpage request

    Returns:
        : Render of the webpage using the django template
    """
    ticket = Ticket.objects.get(ticket_id=id)

    return render(
        request,
        "myapp/display_ticket.html",
        {"ticket": ticket, "can_update": can_user_update_ticket(request, ticket)},
    )


def can_user_update(request, object) -> bool:
    """
    Checks if user can update a TicketType or Status entry. This has a different test to Ticket as these do not have the possibility to assign a user

    Parameters:
        request: The webpage request
        object: The Status or TicketType entry that the user is within to update

    Returns:
        (bool): Can the user update this entry

    """
    return request.user.id == object.reporter_id or request.user.is_superuser


@login_required(login_url="/login")
def ViewStatuses(request):
    """
    Renders the view statuses page

    Parameters:
        request: The webpage request

    Returns:
        : Render of the webpage using the django template
    """
    items = []

    for status in Status.objects.all():
        try:
            reporter = User.objects.get(id=status.reporter_id).username
        except:
            reporter = "None"

        can_update = can_user_update(request, status)

        items.append({"status": status, "reporter": reporter, "can_update": can_update})
    return render(request, "myapp/display_statuses.html", {"items": items})


@login_required(login_url="/login")
def ViewStatus(request, status_name):
    """
    Renders the view status page

    Parameters:
        request: The webpage request

    Returns:
        : Render of the webpage using the django template
    """
    try:
        status_name.replace("%20", " ")
    except:
        pass
    status = Status.objects.get(status_name=status_name)
    return render(
        request,
        "myapp/display_status.html",
        {"status": status, "can_update": can_user_update(request, status)},
    )


@login_required(login_url="/login")
def ViewTypes(request):
    """
    Renders the view types page

    Parameters:
        request: The webpage request

    Returns:
        : Render of the webpage using the django template
    """
    # types = TicketType.objects.all()
    # return render(request, "myapp/display_types.html", {"types": types})
    items = []

    for ticket_type in TicketType.objects.all():
        try:
            reporter = User.objects.get(id=ticket_type.reporter_id).username
        except:
            reporter = "None"

        can_update = can_user_update(request, ticket_type)

        items.append(
            {"ticket_type": ticket_type, "reporter": reporter, "can_update": can_update}
        )

    return render(request, "myapp/display_types.html", {"items": items})


@login_required(login_url="/login")
def ViewType(request, type_name):
    """
    Renders the view type page

    Parameters:
        request: The webpage request

    Returns:
        : Render of the webpage using the django template
    """
    try:
        type_name.replace("%20", " ")
    except:
        pass
    type = TicketType.objects.get(type_name=type_name)
    return render(
        request,
        "myapp/display_type.html",
        {"type": type, "can_update": can_user_update(request, type)},
    )


@login_required(login_url="/login")
def UpdateTicket(request, id):
    """
    Renders the update ticket page

    Parameters:
        request: The webpage request

    Returns:
        : Render of the webpage using the django template
    """
    ticket = Ticket.objects.get(ticket_id=id)

    if can_user_update_ticket(request, ticket):
        form = AddTicket(request.POST or None, instance=ticket)

        if form.is_valid():
            form.save(request=request)
            messages.success(request, message=f"Ticket {id} Updated")
            return redirect("View Tickets")
        return render(
            request, "myapp/form.html", {"form": form, "title": "Update Ticket"}
        )
    else:
        messages.error(
            request,
            message="You are not an admin user, the assigned user or the user who created this ticket. You cannot update this ticket.",
        )
        return redirect("View Tickets")


@login_required(login_url="/login")
def UpdateStatusPage(request, status_name):
    """
    Renders the update status page

    Parameters:
        request: The webpage request

    Returns:
        : Render of the webpage using the django template
    """
    try:
        status_name.replace("%20", " ")
    except:
        pass
    status = Status.objects.get(status_name=status_name)

    if can_user_update(request, status):
        form = UpdateStatus(request.POST or None, instance=status)

        if form.is_valid():
            form.save(request=request)
            messages.success(request, message=f"Status {status_name} Updated")
            return redirect("View Statuses")
        return render(
            request, "myapp/form.html", {"form": form, "title": "Update Status"}
        )
    else:
        messages.error(
            request,
            message="You are not an admin user the user who created this status. You cannot update this status.",
        )
        return redirect("View Statuses")


@login_required(login_url="/login")
def UpdateTicketTypePage(request, type_name):
    """
    Renders the update ticket type page

    Parameters:
        request: The webpage request

    Returns:
        : Render of the webpage using the django template
    """
    try:
        type_name.replace("%20", " ")
    except:
        pass
    type = TicketType.objects.get(type_name=type_name)

    if can_user_update(request, type):
        form = UpdateTicketType(request.POST or None, instance=type)

        if form.is_valid():
            form.save(request=request)
            messages.success(request, message=f"Ticket Type {type_name} Updated")
            return redirect("View Types")
        return render(
            request, "myapp/form.html", {"form": form, "title": "Update Ticket Type"}
        )
    else:
        messages.error(
            request,
            message="You are not an admin user the user who created this ticket type. You cannot update this type.",
        )
        return redirect("View Types")


@user_passes_test(lambda user: user.is_superuser)
def DeleteTicket(request, id):
    """
    Renders the delete ticket page

    Parameters:
        request: The webpage request

    Returns:
        : Render of the webpage using the django template
    """
    ticket = Ticket.objects.get(ticket_id=id)

    if request.method == "POST":
        if "delete" in request.POST:
            ticket.delete()
            messages.success(request, message=f"Ticket {id} deleted")

        return redirect("View Tickets")

    return render(
        request,
        "myapp/delete_object.html",
        context={"model_name": "Ticket", "object_id": ticket.ticket_id},
    )


@user_passes_test(lambda user: user.is_superuser)
def DeleteStatus(request, status_name):
    """
    Renders the delete status page

    Parameters:
        request: The webpage request

    Returns:
        : Render of the webpage using the django template
    """
    status = Status.objects.get(status_name=status_name)

    if request.method == "POST":
        if "delete" in request.POST:
            status.delete()
            messages.success(request, message=f"Status, {status_name}, deleted")

        return redirect("View Statuses")

    return render(
        request,
        "myapp/delete_object.html",
        context={"model_name": "Status", "object_id": status.status_name},
    )


@user_passes_test(lambda user: user.is_superuser)
def DeleteTicketType(request, type_name):
    """
    Renders the delete ticket type page

    Parameters:
        request: The webpage request

    Returns:
        : Render of the webpage using the django template
    """
    type = TicketType.objects.get(type_name=type_name)

    if request.method == "POST":
        if "delete" in request.POST:
            type.delete()
            messages.success(request, message=f"Type, {type_name}, deleted")

        return redirect("View Types")

    return render(
        request,
        "myapp/delete_object.html",
        context={"model_name": "Ticket Type", "object_id": type.type_name},
    )
