from flask import render_template, url_for, redirect, abort, flash, request, current_app

from flask.ext.login import login_required, current_user

from app import db
from app.main import main

from app.models import  User,Assert, Assign
from app.utils import send_email

from app.main.forms import (InventoryRecordsForm, EditInventoryRecordsForm, AssignAssertForm,
                             AssertRequestForm, AssertForm, EditAdminProfileForm)



@main.route('/', methods=['GET', 'POST'])
@login_required    
def index():

    return render_template('main/index.html')

@main.route('/assert_detail', methods=['GET', 'POST'])
@login_required    
def assert_detail():

    return render_template('main/assert_detail.html') 

# renders the list of users in the database
@main.route('/users', methods=['GET', 'POST'])
@login_required    
def users_list():
    users = User.query.order_by(User.name.asc()).all()
    return render_template('main/users_list.html', users=users)    


# add paganation
@main.route('/assert/add', methods=['GET', 'POST'])
def add_assert():
    form = AssertForm()

    if form.validate_on_submit():
        asserts = Assert(name=form.name.data)
        db.session.add(asserts)
        return redirect(url_for('main.index'))
    return render_template('main/add_asserts.html', form=form)


@main.route('/view-assert/<int:assert_id>')
@login_required
def view_assert(assert_id):
    asserts = Assert.query.get_or_404(assert_id)
    return render_template('main/assert_detail.html')


@main.route('/edit-profile/<name>', methods=['GET', 'POST'])
@login_required
def edit_profile_admin(name):
    if not current_user.is_admin: 
        abort(403)
    user = User.query.filter_by(name=name).first()
    if not user:
        abort(404)
    form = EditAdminProfileForm(user=user)
    if form.validate_on_submit():
        try:
            user.email = form.email.data
            user.name = form.name.data
            user.is_admin = form.is_admin.data
            db.session.add(user)
            db.session.commit()
            flash("The profile has been updated.")
            return redirect(url_for('main.users_list'))
        except:
            db.session.rollback()
            flash("An error occurred while updating user information")
            return redirect(url_for('main.edit_profile_admin', name=user.name))
    form.email.data = user.email
    form.name.data = user.name
    form.is_admin.data = user.is_admin

    return render_template('main/edit_profile.html', form=form, user=user)    





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
