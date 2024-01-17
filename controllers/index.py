from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.index_model import get_hotels, get_rooms, get_room_types,\
    get_max_capacity, get_min_capacity, get_min_price, get_max_price,\
    get_additional_services, add_booking, add_additional_services
from datetime import date, timedelta


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()

    min_capacity = get_min_capacity(conn)
    max_capactiy = get_max_capacity(conn)

    capacity = ''

    min_date = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    date_from = min_date
    date_to = min_date
    
    min_price = get_min_price(conn)
    max_price = get_max_price(conn)

    price_from = int(min_price)
    price_to = int(max_price)

    room_types = []
    hotels = []

    selected_room = -1

    if request.form.get('find'):
        if request.form.get('room_capacity'):
            capacity = int(request.form.get('room_capacity'))
        
        if request.form.get('date_from'):
            date_from = request.form.get('date_from')
        else:
            date_from = min_date

        if request.form.get('date_to'):
            date_to = request.form.get('date_to')
        else:
            date_to = min_date

        if request.form.get('price_from'):
            price_from = int(request.form.get('price_from'))
        else:
            price_from = min_price
        
        if request.form.get('price_to'):
            price_to = int(request.form.get('price_to'))
        else:
            price_to = max_price
        
        if request.form.getlist('room_type_id'):
            room_types = [int(x) for x in request.form.getlist('room_type_id')]
        
        if request.form.getlist('hotel_id'):
            hotels = [int(x) for x in request.form.getlist('hotel_id')]
    
    elif request.form.get('next'):
        if request.form.get('room_capacity'):
            capacity = int(request.form.get('room_capacity'))
        
        if request.form.get('date_from'):
            date_from = request.form.get('date_from')
        else:
            date_from = min_date

        if request.form.get('date_to'):
            date_to = request.form.get('date_to')
        else:
            date_to = min_date

        if request.form.get('price_from'):
            price_from = int(request.form.get('price_from'))
        else:
            price_from = min_price
        
        if request.form.get('price_to'):
            price_to = int(request.form.get('price_to'))
        else:
            price_to = max_price
        
        if request.form.get('room_type_id')[1:-1].split(',')[0]:
            room_types = [int(x) for x in request.form.get('room_type_id')[1:-1].split(',')]
        
        if request.form.get('hotel_id')[1:-1].split(',')[0]:
            hotels = [int(x) for x in request.form.get('hotel_id')[1:-1].split(',')]

        selected_room = int(request.form.get('selected_room'))
    
    elif request.form.get('booking'):
        room_id = int(request.form.get('room_id').split(',')[0])
        check_in_date = request.form.get('check_in_date')
        check_out_date = request.form.get('check_out_date')
        user_id = request.form.get('user_id')

        if check_in_date and check_out_date and user_id:
            booking_id = add_booking(conn, check_in_date, check_out_date, room_id, user_id)

            for additional_services_id in request.form.getlist('additional_services_id'):
                print(booking_id, int(additional_services_id))
                add_additional_services(conn, booking_id, int(additional_services_id))

    # if room_types else get_room_types(conn)['room_type_id'].values

    df_hotels = get_hotels(conn)
    df_additional_services = get_additional_services(conn)
    df_room_types = get_room_types(conn)
    df_rooms = get_rooms(
        conn, 
        date_from, 
        date_to, 
        [capacity] if [capacity][0] else range(min_capacity, max_capactiy + 1),
        room_types if len(room_types) else df_room_types['room_type_id'].values, 
        price_from, 
        price_to,
        hotels if len(hotels) else df_hotels['hotel_id'].values
    )

    html = render_template(
        'index.html',
        df_rooms=df_rooms,
        len=len,
        date_from=date_from,
        date_to=date_to,
        min_date=min_date,
        df_hotels=df_hotels,
        df_room_types=df_room_types,
        min_capacity=min_capacity,
        max_capactiy=max_capactiy,
        min_price=min_price,
        max_price=max_price,
        price_from=price_from,
        price_to=price_to,
        capacity=capacity,
        room_types=room_types,
        hotels=hotels,
        selected_room=selected_room,
        str=str,
        df_additional_services=df_additional_services,
    )
    
    return html