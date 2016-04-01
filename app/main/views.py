from flask import render_template, url_for, redirect, abort, flash, request, current_app

from flask.ext.login import login_required, current_user

from app import db
from app.main import main

from app.models import  User,Asset, Inventory, Report_lost
from app.utils import send_email
from datetime import datetime
from app.main.forms import (InventoryRecordsForm, 
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

    if form.validate_on_submit():
        asset = Asset.query.filter_by(name=form.asset_name.data).first()
        assigned_to = User.query.filter_by(name=form.assigned_to_id.data).first()

        date_bought_string = form.date_bought.data.strftime('%Y/%m/%d')
        date_assigned_string = form.date_assigned.data.strftime('%Y/%m/%d')
        date_returned_string = form.date_returned.data.strftime('%Y/%m/%d')

        date_bought_object = datetime.strptime(date_bought_string,'%Y/%m/%d')
        date_assigned_object = datetime.strptime(date_assigned_string,'%Y/%m/%d')
        date_returned_object = datetime.strptime(date_returned_string,'%Y/%m/%d')

        inventory = Inventory(asset_id=asset.id, serial_code=form.serial_code.data,
                            serial_no=form.serial_no.data, asset_name=asset.name,
                            description=form.description.data, date_bought=date_bought_object,
                            confirmed=form.confirmed.data, assigned=form.assigned.data,
                            revolved=form.revolved.data,
                            assigned_to_id=assigned_to.id,  date_assigned=date_assigned_object, 
                            date_returned=date_returned_object)
        db.session.add(inventory)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:    
        return render_template('main/inventory_detail.html', form=form) 

# renders the list of users in the database
@main.route('/users', methods=['GET', 'POST'])
@login_required    
def users_list():
    if current_user.is_admin:
        users = User.query.order_by(User.name.asc()).all()
        return render_template('main/users_list.html', users=users) 
    return render_template('main/index.html')    


@main.route('/assigned_users_list',methods=['GET', 'POST'])  
@login_required
def assigned_users_list():
    if current_user.is_admin:
        inventory = Inventory.query.filter_by(assigned=True).all()
        return render_template('main/assigned_list.html', inventory=inventory)

    return render_template('main/index.html')    
    
@main.route('/not_assigned_asset',methods=['GET', 'POST'])  
@login_required
def not_assigned_asset():
    if current_user.is_admin:
        inventory = Inventory.query.filter_by(assigned=False).all()
        return render_template('main/not_assigned_asset.html', inventory=inventory)
    return render_template('main/index.html')  

# add paganation
@main.route('/asset/add', methods=['GET', 'POST'])
@login_required 
def add_asset():
    form = AssetForm()

    if form.validate_on_submit():
        assets = Asset(name=form.name.data)
        db.session.add(assets)
        db.session.commit()
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
    if not current_user.is_admin: 
        abort(403)
    
    # Get the appropriate form for this user.
   
    form = InventoryRecordsForm()
    
    if form.validate_on_submit():
        assigned_to = User.query.filter_by(name=form.assigned_to_id.data).first()

        inventory.serial_code = form.serial_code.data
        inventory.serial_no = form.serial_no.data
        inventory.asset_name = form.asset_name.data
        inventory.description = form.description.data
        inventory.date_bought = form.date_bought.data
        inventory.confirmed = form.confirmed.data
        inventory.date_assigned = form.date_assigned.data
        inventory.date_returned = form.date_returned.data
        inventory.revolved = form.revolved.data
        inventory.assigned_to_id = assigned_to.id
       
        db.session.add(inventory)
    
        flash("Inventory list is up to date")
        return redirect(url_for('main.index'))

    form.serial_code.data = inventory.serial_code
    form.serial_no.data   = inventory.serial_no 
    form.asset_name.data  = inventory.asset_name
    form.description.data  = inventory.description
    form.date_bought.data = inventory.date_bought
    form.confirmed.data   = inventory.confirmed
    form.date_assigned.data = inventory.date_assigned
    form.date_returned.data = inventory.date_returned
    form.revolved.data = inventory.revolved
    form.assigned.data = inventory.assigned
    flash('No records changed')
    return render_template('main/update_inventory.html',form=form, inventory=inventory)

@main.route('/loss_asset', methods=['GET', 'POST'])
@login_required    
def lost_asset():
    if not current_user.is_admin or current_user.is_admin:
        report = Report_lost.query.filter_by(lost=True).all()
        return render_template('main/report_lost.html', report=report) 
    return render_template('main/index.html')    


@main.route('/report_lost', methods=['GET', 'POST'])
@login_required
def report_lost():
    form = ReportLostAssetForm()

    if form.validate_on_submit():
        lost= Report_lost(name=form.name.data,serial_code=form.serial_code.data,
                            asset_name=form.asset_name.data, lost=form.lost.data)
        db.session.add(lost)
        db.session.commit()
        # send_email(app.config['INVENTORY_ADMIN'],'Report Lost Asset', 'main/email/report_lost', lost_asset=lost)
        return render_template('main/report_lost.html', lost=lost)
    return render_template('main/lost_asset.html', form=form)



    
