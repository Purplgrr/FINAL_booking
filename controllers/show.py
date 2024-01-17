from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.show_model import get_user, get_first_user_id, get_booking, \
    cancel_booking, get_additional_services, get_selected_services, \
    del_booking_services, add_booking_services, get_new_user, set_live_in_date, set_live_out_date, get_room_status
from datetime import date, timedelta

@app.route('/show', methods=['GET', 'POST'])
def show():
    conn = get_db_connection()

    today_date = date.today().strftime('%Y-%m-%d')
    min_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    date_from = min_date
    date_to = min_date

    if 'user_id' not in session:
        session['user_id'] = get_first_user_id(conn)
    is_edit = False
    booking_id = -1
    selected_services = []

    if request.form.get('show'):
        session['user_id'] = request.form.get('user_id')
        is_edit = False
        booking_id = -1
    elif request.form.get('cancel_booking'):
        booking_id = int(request.form.get('booking_id'))
        cancel_booking(conn, booking_id)
        is_edit = False
        booking_id = -1
    elif request.form.get('services_next'):
        booking_id = int(request.form.get('booking_id'))
        is_edit = True
        selected_services = get_selected_services(conn, booking_id)
    elif request.form.get('services_save'):
        booking_id = int(request.form.get('booking_id'))

        del_booking_services(conn, booking_id)

        services = request.form.getlist('additional_services_id')
        for service in services:
            add_booking_services(conn, booking_id, int(service))
    elif request.form.get('user_id') and request.form.get('user_name'):
        session['user_id'] = get_new_user(conn, request.form.get('user_id'), request.form.get('user_name'))
    elif request.form.get('set_live_in_date'):
        booking_id = int(request.form.get('booking_id'))
        set_live_in_date(conn, booking_id, today_date)
    elif request.form.get('set_live_out_date'):
        booking_id = int(request.form.get('booking_id'))
        set_live_out_date(conn, booking_id, today_date)
    elif request.form.get('find'):
        if request.form.get('date_from'):
            date_from = request.form.get('date_from')
        else:
            date_from = min_date

        if request.form.get('date_to'):
            date_to = request.form.get('date_to')
        else:
            date_to = min_date

    df_services = get_additional_services(conn)
    df_user = get_user(conn)
    df_booking = get_booking(conn, session['user_id'])
    df_room_status = get_room_status(conn, date_from, date_to)
    
    html = render_template(
        'show.html',
        user_id=session['user_id'],
        df_user=df_user,
        len=len,
        df_booking=df_booking,
        is_edit=is_edit,
        booking_id=booking_id,
        df_services=df_services,
        selected_services=selected_services,
        today_date=today_date,
        mid_date=min_date,
        date_from=date_from,
        date_to=date_to,
        df_room_status=df_room_status,
    )
    return html