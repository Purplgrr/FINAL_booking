import pandas as pd

def get_user(conn):
    return pd.read_sql(
        '''
            SELECT
                user_id,
                user_name
            FROM
                user
        ''',
        conn
    )

def get_new_user(conn, id, name):
    cur = conn.cursor()
    cur.execute(
        '''
            INSERT INTO user (user_id, user_name)
            VALUES (:user_id, :user_name)
        ''',
        {"user_id": id, "user_name": name}
    )
    conn.commit()
    return id

def del_booking_services(conn, booking_id):
    cursor = conn.cursor()
    cursor.executescript(
        f'''
            DELETE 
            FROM booking_additional_services
            WHERE
                booking_id = {booking_id}
        ''')
    conn.commit()

def add_booking_services(conn, booking_id, additional_services_id):
    cursor = conn.cursor()
    cursor.executescript(
        f'''
            INSERT INTO booking_additional_services (booking_id, additional_services_id)
            VALUES
                ({booking_id}, {additional_services_id})
        ''')
    conn.commit()

def get_selected_services(conn, booking_id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT additional_services_id FROM booking_additional_services WHERE booking_id = {booking_id} ")
    selected_services = [int(row[0]) for row in cursor.fetchall()]
    cursor.close()
    return selected_services 

def get_additional_services(conn):
    return pd.read_sql(
        '''
            SELECT
                additional_services_id,
                additional_services_name
            FROM
                additional_services
        ''',
        conn
    )

def get_first_user_id(conn):
    cursor = conn.cursor()
    cursor.execute(
        '''
            SELECT user_id FROM user
        '''
    )
    user_id = cursor.fetchone()[0]
    cursor.close()
    return user_id

def cancel_booking(conn, booking_id):
    cursor = conn.cursor()
    cursor.execute(
        f'''
            UPDATE booking
            SET room_status_id = 2
            WHERE booking_id = {booking_id}
        '''
    )
    conn.commit()
    cursor.close()

def get_room_status(conn, date_from, date_to):
    return pd.read_sql(
        f'''
            WITH occupied_rooms
            AS (
                SELECT
                    room_id,
                    room_status_name
                FROM
                    booking
                    JOIN room_status USING (room_status_id)
                WHERE
                    room_status_name IN ('забронировано', 'проживают')
                    AND strftime('%Y-%m-%d', check_in_date) <= '{date_from}'
                    AND strftime('%Y-%m-%d', check_out_date) >= '{date_to}'
            )

            SELECT
                room_number AS Номер,
                hotel_name AS Отель,
                room_type_name AS Тип,
                room_capacity AS Вместимость,
                room_price AS Цена,
                CASE
                    WHEN room_status_name IS NULL THEN 'свободно'
                    ELSE room_status_name
                END AS Статус
            FROM
                room
                LEFT JOIN booking USING (room_id)
                LEFT JOIN hotel USING (hotel_id)
                LEFT JOIN room_type USING (room_type_id)
                LEFT JOIN occupied_rooms USING (room_id)
        ''',
        conn
    )

def get_booking(conn, user_id):
    return pd.read_sql(
        f'''
            WITH services
            AS (
                SELECT
                    booking_id,
                    GROUP_CONCAT(additional_services_name || ' - ' || additional_services_price, ', ') AS full_service_name,
                    SUM(additional_services_price) AS sum_services
                FROM
                    booking_additional_services
                    JOIN additional_services USING (additional_services_id)
                GROUP BY
                    booking_id
            )

            SELECT
                booking_id,
                room_number AS Номер,
                hotel_name AS Отель,
                room_type_name AS Тип,
                room_capacity AS Вместимость,
                room_price AS Цена,
                check_in_date AS 'Дата въезда',
                check_out_date AS 'Дата выезда',
                live_in_date AS 'Дата начала проживания',
                live_out_date AS 'Дата конца проживания',
                full_service_name AS 'Доп. услуги',
                sum_services + room_price * (JULIANDAY(check_out_date) - JULIANDAY(check_in_date) + 1) AS 'Предварительная стоимость',
                sum_services + room_price * (JULIANDAY(live_out_date) - JULIANDAY(live_in_date) + 1) AS 'Фактическая стоимость',
                room_status_name AS Статус
            FROM
                booking
                JOIN services USING (booking_id)
                JOIN room USING (room_id)
                JOIN room_type USING (room_type_id)
                JOIN room_status USING (room_status_id)
                JOIN hotel USING (hotel_id)
            WHERE
                user_id = '{user_id}'
        ''',
        conn
    )

def set_live_in_date(conn, booking_id, today_date):
    cursor = conn.cursor()
    cursor.execute(
        f'''
            UPDATE booking
            SET live_in_date = '{today_date}'
            WHERE booking_id = {booking_id}
        '''
    )
    cursor.execute(
        f'''
            UPDATE booking
            SET room_status_id = 3
            WHERE booking_id = {booking_id}
        '''
    )
    cursor.close()
    conn.commit()

def set_live_out_date(conn, booking_id, today_date):
    cursor = conn.cursor()
    cursor.execute(
        f'''
            UPDATE booking
            SET live_out_date = '{today_date}'
            WHERE booking_id = {booking_id}
        '''
    )
    cursor.execute(
        f'''
            UPDATE booking
            SET room_status_id = 4
            WHERE booking_id = {booking_id}
        '''
    )
    cursor.close()
    conn.commit()