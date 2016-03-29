from flask import render_template, url_for, redirect, abort, flash, request, current_app

from flask.ext.login import login_required, current_user

# from app import db
from app.main import main

# from app.models import  User
# from app.utils import send_email

# from app.main.forms import (InventoryRecordsForm, EditInventoryRecordsForm, AssignAssertForm, AssertRequestForm, AssertForm)



@main.route('/', methods=['GET', 'POST'])
@login_required    
def index():
    return render_template('main/index.html')


# @main.route('/assert/create', methods=['GET', 'POST'])
# def create_assert():
#     form = AssertForm()

#     if form.validate_on_submit():
#         asserts = Assert(name=form.name.data)
#         db.session.add(asserts)
#         return redirect(url_for('main.index'))
#     return render_template('main/create-assert.html', form=form)

# @main.route('assert-requests', method=['GET', 'POST'])
# @login_required
# def assert_request():
#     form = AssertRequestForm()

#     if form.validate_on_submit():
#         asserts = Asserts(
#             requested_by_id=current_user.id,
#             assert_id=form.assert_name.data,
#             serial_code=form.serial_code.data,
#             serial_no=serial_no.data,
#             description=form.description.data)

#         db.session.add(asserts)
#         db.session.commit()
#         # admin = User.query.filter_by(email=current_app.config['INVENTORY_ADMIN']).first()
#         # send_mail(assign)
#         return render_template('')