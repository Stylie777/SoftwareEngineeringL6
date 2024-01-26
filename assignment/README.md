<!---
Program:  Web Based Database Application
Filename: README.md           
@author:  © Jack Styles             
Course:   BSc Digital Technology Solutions                     
Module:   Software Engineering and Agile             
Tutor:    Suraksha Neupane                         
@version: 1.0     
Date:     22/09/23
-->

# Assignment

## Introduction 

This Django project contains a website for managing tickets in an IT company. The website is designed to be versatile to the users need's, whsers can create their own ticket types and statuses for the tickets, along with the tickets themselves.

## Accessing the webpage
The webpage is available online, for review, [here][online-webpage]. This can also be run locally by cloning this repository and running the Django server in your terminal. The appliction has been tested on MacOS Ventura 13.4 with Python 3.10.1. and is hosted using Pythonanywhere's server infrastructure based on Linux. The below is for Bash or Zsh terminals, for Windows please use the eqivilent in Powershell or Terminal.

**IMPORTANT:** A Python Virtual Environment will be required, please see the [python3 venv Documentation][venv-docs] for more information.

### Users
You can create your own user by using the [register][register-page] page. This gives you a user where you can create and view Tickets, Statuses and Ticket Types, along with updating the entries that you create. You can also update the Tickets that are assigned to you. Registration is simple, with the webpage explaining the information that is required and ensuring that the data you enter is valid.

Please contact the system administrator if you require an admin account, with justification to do so.

### Running locally
1. Clone the git repository:
```
git clone https://github.com/Stylie777/SoftwareEngineeringL5.git
```
2. Navigate to the assignment folder:
```
cd SoftwareEngineeringL5/assignment/assignment
```
3. Install the required packages using pip:
```
pip install -r requirements.txt
```
or
```
python3 -m pip install -r requirements.txt
```
4. Run the django server from the terminal. This should be done from the directory containing `manage.py`:
```
python3 manage.py runserver
```

This will launch a local Django server where the website can be used. The database is also stored locally, so any changes made on the local copy will not be replicated on the hosted version.

## Updating Database

The database can be manipulated with the four CRUD operations. The process for each singular database for the webpage is the same, as detailed below.

### Creation
Entries can be created within the website by any user. The link to do so is available under the sections respective Management tab. Three are available, `Ticket`, `Status` and `Ticket Type`.

The page to create an entry will use a form to collect the data, with some having required fieldd. Required fields are documented within the [Database Fields](##database-fields) section

### Viewing
The database entries can be viewed using the `View <database-name>` option under the `<database-name> Management` tab from the Navbar. From here the user can view the details of specific entries, update the entry and, for admin users, delete entries.

### Updating
Ticket types can be updated using the link for that type from the View Ticket Type table. From here the form will be loaded where the user can change the details of the ticket type. This will be revalidated using the same validation used when creating the type before commiting the changes to the database.

**Updating tickets is limited to admin users, the user who created the ticket and the user who is assigned the ticket. Anyone else can view, but not update.**

**Updating Statuses or Ticket Types is limited to admin users and the user who created the Status/Ticket Type.**

### Deleting
Only admin users can delete database entries. This can be done from the table to view all the tickets that are open, or from the page used to view the details of an entry. The user will be aske to confirm they wish to delete that entry before the deletion takes place. Once this takes place it is an irreversable operation.

Only other admin users can add new admins, and this is done using the `django-admin` utility within a console.

## Database fields

The fields listed below in __bold__ are required fields, and cannot be left blank. The forms are designed to remind the user of this when entering data into a form.

### Ticket Type

- __Ticket Title: this must starts with a captial letter and is required__
- Ticket info: This contains the details on the ticket that is being created
- __Assignee: This will be a user that is registered to the website and is required__
- __Status: This is one of the status entries that can be created by users and is_required__
- Type; This is the type of ticket being created
- Date due: This is the date the ticket is due to be completed by

### Status

- __Status name: This must start with a captial letter and is required__
- Status description: This is the description of the status being created where extra information can be added

### Ticket

- __Type name: This must start with a captial letter and is required__
- Type description: This is the type description being created where extra information can be added about the type.

## Tests

Unit tests have been written for models, views and forms used within the project. The tests can be found within the `tests.py` file. The unit tests are written as high level tests, so changes to functions logic should not effect the end result or changes to the tests themselves. This also allows the user to confirm any changes to the logic is valid when the Unit Tests pass.

The tests look at the models defined within `models.py`. Django's User Authentication models are not tested, as this is not models or logic that has been added as part of this project  

To run these, use this command in the terminal in the same directory used to run the local Django server.

```
python3 manage.py test
```

This should be run everytime a change is made to ensure continued validation of the webpage and ensure there are no errors. 

[online-webpage]: http://stylie777.pythonanywhere.com
[venv-docs]: https://docs.python.org/3/library/venv.html
[register-page]: https://stylie777.pythonanywhere.com/register/