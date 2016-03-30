from flask.ext.wtf  import Form
from datetime import datetime 
from flask import flash
from wtforms import (TextField, IntegerField, DateField, BooleanField, PasswordField,
                    StringField, PasswordField, SubmitField,FileField, SelectField, RadioField)
from wtforms.validators import Required, Email, EqualTo, Length, Email, Regexp, ValidationError, regexp
from app.models import User, Assert, Assign  
from werkzeug import secure_filename
from wtforms import validators



class InventoryRecordsForm(Form):
    serial_code = TextField('Serial code', validators=[Required(), Length(10, 255)])
    serial_no   = IntegerField('Serial number', validators=[Required()])
    assert_name = SelectField('Name of Assert', coerce=int)
    description = TextField('Assert Description')
    date_bought = DateField("Date Purchased",
                          format='%d/%m/%Y')
    submit      = SubmitField('Add Inventory')

    def __init__(self, *args, **kwargs):
        super(InventoryRecordsForm, self).__init__(*args, **kwargs)
        self.assert_name.choices = [
            (ass.id, ass.name) for ass in Assert.query.order_by(Assert.name).all()
        ]


class AssignAssertForm(InventoryRecordsForm):
    user        = RadioField("Assign staff", coerce=int, validators=[validators.DataRequired()])
    return_date = DateField("Return date",
                            format='%d/%m/%Y') 
    submit      = SubmitField('Assign Assert')

    def __init__(self, *args, **kwargs):
        super(AssignAssertForm, self).__init__(*args, **kwargs)
        self.user.choices = [
            (use.id, use.name) for use in User.query.order_by(User.name).all()
        ]

class EditInventoryRecordsForm(InventoryRecordsForm):
    submit = SubmitField('Add new records')

    def __init__(self,**kwargs):
        super(EditInventoryRecordsForm,self).__init__()
        self.asserts_id = kwargs.get(asserts_id)

class AssertRequestForm(InventoryRecordsForm):
    staff_name = TextField('Staff_name',validators=[Required(), Length(10, 255)])
    submit = SubmitField('Request Assert')

    def __init__(self, *args, **kwargs):
        super(AssertRequestForm, self).__init__(*args, **kwargs)


class AssertForm(Form):
    name = StringField('Assert Name', validators=[Required()])
    submit = SubmitField('Add Assert')

    def validate_name(self, field):
        if Assert.query.filter_by(name=field.data).first():
            raise ValidationError("This Assert name  exists.")


class EditAdminProfileForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    name = StringField(
        'Username',
        validators=[Required(), Length(1, 64),
                    Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                           'Usernames should only contain letters, numbers, dots or underscores'
                           )
                    ])
    is_admin = BooleanField("Is Admin")
    submit = SubmitField('Update')

    def __init__(self, user, *args, **kwargs):
        super(EditAdminProfileForm, self).__init__(*args, **kwargs)
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered.')

    def validate_name(self, field):
        if field.data != self.user.name and User.query.filter_by(name=field.data).first():
            raise ValidationError("Username is taken")