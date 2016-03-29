# from flask.ext.wtf  import Form
# from datetime import datetime 
# from flask import flash
# from wtforms import TextField, IntegerField, DateField, BooleanField, PasswordField, StringField, PasswordField,SubmitField,FileField
# from wtforms.validators import Required, Email, EqualTo, Length, Email, Regexp, ValidationError, regexp
# from app.model import User  
# from werkzeug import secure_filename



# class InventoryRecordsForm(Form):
#     serial_code = TextField('Serial code',validators=[Required(), Length(10, 255)])
#     serial_no = IntegerField('Serial number'validators=[Required(), Length(10, 255)])
#     assert_name = SelectField('Name of Assert', coerce=int )
#     description = TextField('Assert Description')
    
#     def __init__(self, *args, **kwargs):
#         super(InventoryRecordsForm, self).__init__(*args, **kwargs)
#         self.assert_name.choices = [
#             (ass.id, ass.name) for ass in assert_name.query.order_by(.name).all()
#         ]


# class EditInventoryRecordsForm(InventoryRecordsForm):
#     date_bought = DateField("Date Purchased",
#                           format='%d/%m/%Y', validators=[validators.Optional()])
#     submit = SubmitField('Add new records')

#     def __init__(self,**kwargs):
#         super(EditInventoryRecordsForm,self).__init__()
#         self.asserts_id = kwargs.get(asserts_id)

# class AssignAssertForm(InventoryRecordsForm):
#     user = RadioField("Assign staff", coerce=int, validators=[validators.DataRequired()])
#     return_date = DateField("Return date",
#                             format='%d/%m/%Y') 
#     submit = SubmitField('Assign Assert')

#     def __init__(self, *args, **kwargs):
#         super(AssignAssertForm, self).__init__(*args, **kwargs)


# class AssertRequestForm(InventoryRecordsForm):
#     staff_name = TextField('Staff_name',validators=[Required(), Length(10, 255)])
#     submit = SubmitField('Request Assert')

#     def __init__(self, *args, **kwargs):
#         super(AssertRequestForm, self).__init__(*args, **kwargs)


# class AssertForm(Form):
#     name = StringField('Assert Name', validators=[Required()])
#     submit = SubmitField('Add Assert')

#     def validate_name(self, field):
#         if Assert.query.filter_by(name=field.data).first():
#             raise ValidationError("This Assert name  exists.")
