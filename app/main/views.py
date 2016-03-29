from flask import render_template, url_for, redirect, abort, flash, request, current_app

from flask.ext.login import login_required, current_user

from app import db
from app.main import main

from app.models import  User
from app.utils import send_email



@main.route('/', methods=['GET', 'POST'])
@login_required    
def index():
    return render_template('main.index')