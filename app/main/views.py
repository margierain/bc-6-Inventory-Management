from flask import render_template, url_for, redirect, abort, flash, request, current_app

from flask.ext.login import login_required, current_user

from app import db
from app.main import main

from app.models import  User,Asset, Inventory
from app.utils import send_email

from app.main.forms import (InventoryRecordsForm, AdminUpdateInventoryForm,
                              AssetForm, EditAdminProfileForm,ReportLostAssetForm)



@main.route('/', methods=['GET', 'POST'])
@login_required    
def index():
    inventories = []
    if current_user.is_admin:
        inventories = Inventory.query.order_by(Inventory.serial_code)
        return render_template('main/index.html', inventories=inventories)
    elif current_user.is_authenticated:
        assigned = current_user.assigned.all()
        return render_template('main/index.html', inventories=assigned)
    else:
        inventories = current_user.inventories.filter_by(
            assigned=False).order_by(Inventory.serial_code)
        return render_template('main/index.html', inventories=inventories)

@main.route('/inventory_detail', methods=['GET', 'POST'])
@login_required    
def inventory_detail():
    form = InventoryRecordsForm()
    
    inventory = Inventory.query.filter_by(asset_name=form.asset_name.data).all()
    if form.validate_on_submit():
        inventory = Inventory(serial_code=form.serial_code.data,
                            serial_no=form.serial_no.data, asset_name=form.asset_name,
                            description=form.description.data, date_bought=form.date_bought.data)
        db.session.add(inventory)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('main/inventory_detail.html', form=form, inventory=inventory) 

# renders the list of users in the database
@main.route('/users', methods=['GET', 'POST'])
@login_required 
@login_required    
def users_list():
    users = User.query.order_by(User.name.asc()).all()
    return render_template('main/users_list.html', users=users)    


# add paganation
@main.route('/asset/add', methods=['GET', 'POST'])
@login_required 
def add_asset():
    form = AssetForm()

    if form.validate_on_submit():
        assets = Asset(name=form.name.data)
        db.session.add(assets)
        return redirect(url_for('main.inventory_detail'))
    return render_template('main/add_assets.html', form=form)


@main.route('/view_inventory/<int:asset_id>')
@login_required
def view_iventory(asset_id):
    inventory = Inventory.query.get_or_404(asset_id)
    if not (current_user.is_admin):
        if assets.assigned_to_id != current_user.id:
            abort(403)
    return render_template('main/inventory_detail.html', inventory=inventory)


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




@main.route('/update-inventory/<int:inventory_id>', methods=['GET', 'POST'])
@login_required
def update_inventory(inventory_id):
    inventory = Inventory.query.get_or_404(inventory_id)
    
    
    # Get the appropriate form for this user.
    # if current_user.is_admin:
    form = AdminUpdateInventoryForm()
    # else:
    #     form = ReportLostAssetForm()
    # and the the post from users on lost items.
    if form.validate_on_submit():

        inventory.serial_code = form.serial_code.data
        inventory.serial_no   = form.serial_no.data
        inventory.asset_name = form.asset_name.data
        inventory.date_bought = form.date_bought.data
        inventory.confirmed   = form.confirmed.data
        inventory.date_assigned = form.date_assigned.data
        inventory.date_returned = form.date_returned
        db.session.add(inventory)
        
        flash("Inventory list in up to date")
        return redirect(url_for('main.index'))

    form.serial_code.data = inventory.serial_code
    form.serial_no.data   = inventory.serial_no 
    form.asset_name.data = inventory.asset_name
    form.date_bought.data = inventory.date_bought
    form.confirmed.data   = inventory.confirmed
    form.date_assigned.data = inventory.date_assigned
    form.date_returned = inventory.date_returned
    flash('No records changed')
    return render_template('main/update_inventory.html',form=form, inventory=inventory)
