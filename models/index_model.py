import pandas as pd

def get_hotels(conn):
    return pd.read_sql(
        '''
            SELECT
                hotel_id,
                hotel_name
            FROM
                hotel
        ''',
        conn
    )

def get_room_types(conn):
    return pd.read_sql(
        '''
            SELECT
                room_type_id,
                room_type_name
            FROM
                room_type
        ''',
        conn
    )

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

def get_rooms(conn, date_from, date_to, room_capacity, room_types, room_price_from, room_price_to, hotels):
    return pd.read_sql(
        f'''
            WITH occupied_rooms
            AS (
                SELECT
                    room_id
                FROM
                    booking
                    JOIN room_status USING (room_status_id)
                WHERE
                    room_status_name IN ('забронировано', 'проживают')
                    AND strftime('%Y-%m-%d', check_in_date) <= '{date_from}'
                    AND strftime('%Y-%m-%d', check_out_date) >= '{date_to}'
            )

            SELECT
                hotel_name,
                room_type_name,
                room_capacity,
                room_price,
                COUNT(room_id) AS free_room_count,
                GROUP_CONCAT(room_id) AS room_id
            FROM
                room
                LEFT JOIN hotel USING (hotel_id)
                LEFT JOIN room_type USING (room_type_id)
            WHERE
                room_type_id IN {'({})'.format(', '.join([str(elem) for elem in room_types]))}
                AND room_capacity IN {'({})'.format(', '.join([str(elem) for elem in room_capacity]))}
                AND room_id NOT IN (SELECT room_id FROM occupied_rooms)
                AND room_price BETWEEN {room_price_from} AND {room_price_to}
                AND hotel_id IN {'({})'.format(', '.join([str(elem) for elem in hotels]))}
            GROUP BY
                hotel_name,
                room_type_name,
                room_capacity,
                room_price
            ORDER BY
                room_capacity
        ''',
        conn
    )


def add_booking(conn, check_in_date, check_out_date, room_id, user_id):
    cursor = conn.cursor()
    cursor.execute(
        f'''
            INSERT INTO booking(user_id, room_id, check_in_date, check_out_date, room_status_id)
            VALUES
                ('{user_id}', {room_id}, '{check_in_date}', '{check_out_date}', 1)
        '''
    )
    conn.commit()
    return cursor.lastrowid

def add_additional_services(conn, booking_id, additional_services_id):
    cursor = conn.cursor()
    cursor.execute(
        f'''
            INSERT INTO booking_additional_services(booking_id, additional_services_id)
            VALUES
                ({booking_id}, {additional_services_id})
        '''
    )
    conn.commit()

def get_max_capacity(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(room_capacity) FROM room")
    max_capacity = cursor.fetchone()[0]
    cursor.close()
    return max_capacity

def get_min_capacity(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT MIN(room_capacity) FROM room")
    min_capacity = cursor.fetchone()[0]
    cursor.close()
    return min_capacity

def get_min_price(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT MIN(room_price) FROM room")
    min_price = cursor.fetchone()[0]
    cursor.close()
    return min_price
 
def get_max_price(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(room_price) FROM room")
    max_price = cursor.fetchone()[0]
    cursor.close()
    return max_price