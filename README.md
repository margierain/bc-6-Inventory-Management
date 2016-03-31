# Bootcamp six Andela - **Inventory Management System.** 

Developed using flask *web-framework* in python language
To access the App Users need to register and a confirmation email will be sent to enable you verify your email account details.

Once your signed in, depending on your user status i.e an Administrator or a regular user you have access to the following:

## Main features
1. Sign in

2. Add other Adminanistrators

3. Create Assets Records to the inventory list.

4. Update Inventory records which include:

    1. Assigning and unassigning  assets to uses

    2. Incase issues arise eg. user reports lost or found assets, the admin can mark such issues as resolved

5. The admin should be able to view a list of users who are assigned assets as well as a list of assets not assigned


### User features
1. Report lost or found Assets

You can easily get a local copy of this application on your workstation. This guide assumes that you have a working installation of Python 3.4 and pip in your workstation

 ###### Clone this repository
` $ https://github.com/margierain/bc-6-Inventory-Management.git`

###### Install project dependencies via pip. It's recommended that you do this in a virtualenv

` $ pip install -r requirements.txt`

###### Initialize your development database.

` $ python manage.py db init`

###### To construct the database and migrate the database models.


` $ python manage.py db migrate`

` $ python manage.py db upgrade`

###### Run the server.

` $ python  manage.py runserver`

###### Run the server.


Incase your deploying this Inventory Management application the following environment variables have to be set-up.

1. ` INVENTORY_ADMIN` - The email address of this is system administrator. When the administrator (user with this email) signs up in the registration page, the system will automatically assign them the admin role.

2. `INVENTORY_MAIL_SENDER` - this is the automated email set to send users who sign up emails 

3. `SECRET_KEY` - this key generates the tokens generate by the CSRF as well as the authentication send to users who sign up 

4. `INVENTORY_PASSWORD`- this is the password for the Admin


### Improvements needed
1. More testing needs to be  done to verify, all the functionalities work properly

2. Add  features that will enable staff member (users) to request for assets they need




### Conclusion 

This is an Andela assigned project  to put  my skill on the runway  for both  learning process and evaluation purposes.
You can finally view it ok [heroku](http://webmart.herokuapp.com)

