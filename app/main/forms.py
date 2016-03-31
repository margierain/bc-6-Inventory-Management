from flask.ext.wtf  import Form
from datetime import datetime 
from flask import flash
from wtforms import (TextField, IntegerField, DateField, BooleanField, PasswordField,
                    StringField, PasswordField, SubmitField,FileField, SelectField, RadioField)
from wtforms.validators import Required, Email, EqualTo, Length, Email, Regexp, ValidationError, regexp
from app.models import User, Asset, Inventory 
from werkzeug import secure_filename
from wtforms import validators


# Add assert record to  inventory
class InventoryRecordsForm(Form):
    serial_code = TextField('Serial code', validators=[Required(), Length(10, 255)])
    serial_no   = IntegerField('Serial number', validators=[Required()])
    asset_name = SelectField('Name of Asset', coerce=int)
    description = TextField('Asset Description')
    date_bought = DateField("Date Purchased",
                          format='%d/%m/%Y')
    submit      = SubmitField('Add Inventory')

    def __init__(self, *args, **kwargs):
        super(InventoryRecordsForm, self).__init__(*args, **kwargs)
        self.asset_name.choices = [
            (ass.id, ass.name) for ass in Asset.query.order_by(Asset.name).all()
        ]

# assign  assert to staff
class AdminUpdateInventoryForm(InventoryRecordsForm):
    confirmed = BooleanField("Confirm  Request")
    assigned = BooleanField("Assigned")
    resolved = BooleanField("Resolved")
    assigned_to_id = SelectField("Assigned To", coerce=int)
    date_assigned = DateField("Return date",
                            format='%d/%m/%Y')
    date_returned = DateField("Return date",
                            format='%d/%m/%Y') 
    submit      = SubmitField('Update Asset')

    def __init__(self, *args, **kwargs):
        super(AdminUpdateInventoryForm, self).__init__(*args, **kwargs)
        self.assigned_to_id.choices = [
            (use.id, use.name) for use in User.query.order_by(User.name).all()
        ]

    def validate_assigned_to_id(self, field):
        id = field.data
        if not User.query.filter_by(id=id).first():
            flash("Staff has no been assigned asserts.")

#form used to add new asserts 
class AssetForm(Form):
    name = StringField('Asset Name', validators=[Required()])
    submit = SubmitField('Add Asset')

    def validate_name(self, field):
        if Asset.query.filter_by(name=field.data).first():
            raise ValidationError("This Asset name  exists.")

# form used to Add admins
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


class ReportLostAssetForm(InventoryRecordsForm):
    lost = BooleanField("Lost Asset")
    found = BooleanField("Found Asset")
    submit = SubmitField("Report lost or found Asset")

    def __init__(self, *args, **kwargs):
        super(ReportLostAssetForm, self).__init__(*args, **kwargs)
