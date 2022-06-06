from time import time
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Hours
from datetime import date, datetime
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    independent = "independent"
    supervised = "supervised"
    if request.method == 'POST':
        month = request.form.get('month')
        year = request.form.get('year')
        if month == "Choose the month to check." or year == "Choose the year to check.":
            flash('Choose both fields!', category='error')
        else:
            hours = Hours.query.all()
            # Calculates the indepdent hours from the specific date requested
            ind_hours = [hours.sessTime for hours in hours if month == hours.date[5:7] and year == hours.date[:4] and hours.supInd == "independent"]
            i_hours = sum(ind_hours)
            # Calculates the supervised hours from the specific date requested
            sup_hours = [hours.sessTime for hours in hours if month == hours.date[5:7] and year == hours.date[:4] and hours.supInd == "supervised"]
            s_hours = sum(sup_hours)

            flash('Showing hours for selected time.', category='success')
            return render_template('home.html', user=current_user, hours=hours, month=month, year=year, independent=independent, supervised=supervised, i_hours=i_hours, s_hours=s_hours)

    return render_template('home.html', user=current_user)


# Allows user to input hours for specific date & time 

@views.route('/hours', methods=['GET', 'POST'])
@login_required
def hours():
    if request.method == 'POST':
        date = request.form.get('date')
        s_time = request.form.get('startTime')
        e_time = request.form.get('endTime')
        h_type = request.form.get('supInd')

        time_diff = datetime.strptime(e_time, '%H:%M') - datetime.strptime(s_time, '%H:%M')
        sess_time = (time_diff.total_seconds()/3600)
        print(sess_time)

        if date == '' or s_time == '' or e_time == '' or h_type == 'None':
            flash('Ensure all fields are populated!', category='error')
        else:
            new_session = Hours(date=date, start=s_time, end=e_time, sessTime=sess_time, supInd=h_type, user_id=current_user.id)
            db.session.add(new_session)
            db.session.commit()
            flash('Hours successfully added!', category='success')

    return render_template('hours.html', user=current_user)

# Allows user to delete false entries when table is created 

@views.route('/delete-sess', methods=['POST'])
def delete_sess():
    sess = json.loads(request.data)
    sessId = sess['sessId']
    sess = Hours.query.get(sessId)
    if sess:
        if sess.user_id == current_user.id:
            db.session.delete(sess)
            db.session.commit()

    return jsonify({})

