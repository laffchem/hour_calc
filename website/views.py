from time import time
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Hours
from datetime import datetime, timedelta
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
            # Calculates all of the independent hours in terms of various requirements for display on the table.

            # Calculates the direct independent hours from the specific date requested
            dir_ind_hours = [hours.sessTime for hours in hours 
            if month == hours.date[5:7] and year == hours.date[:4] 
            and hours.supInd == "independent" and hours.dirInd == "direct"]
            dir_independent_hours = sum(dir_ind_hours)

            #Calculates the indirect independent hours from the specific date requested.
            ind_ind_hours = [hours.sessTime for hours in hours 
            if month == hours.date[5:7] and year == hours.date[:4] 
            and hours.supInd == "independent" and hours.dirInd == "indirect"]
            ind_independent_hours = sum(ind_ind_hours)

            # Calculates the indepdent hours from the specific date requested
            ind_hours = [hours.sessTime for hours in hours 
            if month == hours.date[5:7] and year == hours.date[:4] 
            and hours.supInd == "independent"]
            independent_hours = sum(ind_hours)
            
            # Calculates all of the supervised hours in terms of various requirements for display on the table.

            # Calculates the direct supervised hours from the specific date requested.
            dir_sup_hours = [hours.sessTime for hours in hours 
            if month == hours.date[5:7] and year == hours.date[:4] 
            and hours.supInd == "supervised" and hours.dirInd == "direct"]
            dir_supervised_hours = sum(dir_sup_hours)

            # Calculates the indirect supervised hours from the specific date requested.
            ind_sup_hours = [hours.sessTime for hours in hours 
            if month == hours.date[5:7] and year == hours.date[:4] 
            and hours.supInd == "supervised" and hours.dirInd == "direct"]
            ind_supervised_hours = sum(ind_sup_hours)

            # Calculates the supervised hours from the specific date requested
            sup_hours = [hours.sessTime for hours in hours 
            if month == hours.date[5:7] and year == hours.date[:4] 
            and hours.supInd == "supervised"]
            supervised_hours = sum(sup_hours)

            #Calculates the total hours for the month.
            total = independent_hours + supervised_hours

            flash('Showing hours for selected time.', category='success')
            return render_template(
                'home.html', 
                user=current_user, 
                hours=hours, 
                month=month, 
                year=year, 
                independent=independent, 
                supervised=supervised, 
                dirIndHours = dir_independent_hours, 
                indIndHours= ind_independent_hours,
                i_hours = independent_hours,
                dirSupHours = dir_supervised_hours,
                indSupHours = ind_supervised_hours, 
                s_hours=supervised_hours,
                total=total)

    return render_template('home.html', user=current_user)


# Allows user to input hours for specific date & time. Annoyingly for user,
# this will double check to ensure start time is < end time. But it resets
# the form. Have to figure out how to make that not happen.

@views.route('/hours', methods=['GET', 'POST'])
@login_required
def hours():
    if request.method == 'POST':
        date = request.form.get('date')
        s_time = request.form.get('startTime')
        e_time = request.form.get('endTime')
        s_type = request.form.get('supInd')
        h_type = request.form.get('dirInd')

        time_diff = datetime.strptime(e_time, '%H:%M') - datetime.strptime(s_time, '%H:%M')
        sess_time = (time_diff.total_seconds()/3600)
        

        if date == '' or s_time == '' or e_time == '' or h_type == 'None':
            flash('Ensure all fields are populated!', category='error')
        elif sess_time <= 0:
            flash('Start time must be greater than end time!', category='error')        
        else:
            new_session = Hours(
                date=date, 
                start=s_time, 
                end=e_time, 
                sessTime=sess_time, 
                supInd=s_type, 
                dirInd=h_type, 
                user_id=current_user.id
                )
            db.session.add(new_session)
            db.session.commit()
            flash('Hours successfully added!', category='success')

    return render_template('hours.html', user=current_user)

# Allows user to delete false entries when table is created. This will reload
# the current table they were on, but the form info will be blank.

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

