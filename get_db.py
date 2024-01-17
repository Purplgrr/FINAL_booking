import sqlite3 as sql

connection = sql.connect('hotel_database.sqlite')
cursor = connection.cursor()

# Таблица Отель
cursor.executescript(
    '''
        CREATE TABLE IF NOT EXISTS hotel (
            hotel_id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_name VARCHAR(50) NOT NULL,
            hotel_address VARCHAR(50) NOT NULL
        )
    '''
)

cursor.executescript(
    '''
        INSERT INTO hotel (hotel_name, hotel_address) 
        VALUES 
            ('Мина Арбат','ул.Черёмуховая, д.59'),
            ('Отель-Отель', 'ул.Светланская, д.17'),
            ('Отель "Авангард"', 'ул.Черёмуховая, д.60')
    '''
)

# Таблица Статус номера
cursor.executescript(
    '''
        CREATE TABLE IF NOT EXISTS room_status (
            room_status_id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_status_name TEXT NOT NULL
        )
    '''
)

cursor.executescript(
    '''
        INSERT INTO room_status (room_status_name) 
        VALUES 
            ('забронировано'),
            ('отмена'),
            ('проживают'),
            ('выселились')
    '''
)

# Таблица Тип номера
cursor.executescript(
    '''
        CREATE TABLE room_type (
            room_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_type_name VARCHAR(15) NOT NULL
        )
    '''
)

cursor.executescript(
    '''
        INSERT INTO room_type (room_type_name) 
        VALUES 
            ('люкс'),
            ('полулюкс'),
            ('стандарт')
    '''
)

# Таблица Номер
cursor.executescript(
    '''
        CREATE TABLE IF NOT EXISTS room (
            room_id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_type_id INTEGER NOT NULL,
            room_capacity INTEGER NOT NULL,
            room_price INTEGER NOT NULL,
            room_number INTEGER NOT NULL,
            hotel_id INTEGER NOT NULL,

            FOREIGN KEY (room_type_id) REFERENCES room_type(room_type_id) ON DELETE CASCADE,
            FOREIGN KEY (hotel_id) REFERENCES hotel(hotel_id) ON DELETE CASCADE
        )
    '''
)

cursor.executescript(
    '''
        INSERT INTO room (room_type_id, room_capacity, room_price, room_number, hotel_id) 
        VALUES
            (1, 5, 17000, 534, 1),
            (2, 3, 11000, 345, 1),
            (3, 2, 7000, 102, 1),
            (1, 5, 23000, 407, 2),
            (2, 3, 11000, 305, 1),
            (2, 4, 13000, 222, 2),
            (1, 5, 23000, 405, 2),
            (3, 2, 6000, 103, 2),
            (3, 2, 7000, 107, 1),
            (3, 2, 8000, 302, 3),
            (3, 3, 9000, 409, 3),
            (1, 4, 27000, 901, 3),
            (2, 4, 9000, 506, 3),
            (3, 2, 7000, 502, 1),
            (1, 4, 27000, 801, 3)
    '''
)

# Таблица Пользователь
cursor.executescript(
    '''
        CREATE TABLE IF NOT EXISTS user (
            user_id VARCHAR(11) PRIMARY KEY,
            user_name VARCHAR(50) NOT NULL
        )
    '''
)

cursor.executescript(
    '''
        INSERT INTO user (user_id, user_name) 
        VALUES
            ('89000000001', 'Васильков М.И.'),
            ('89000000002', 'Бингре Я.В.'),
            ('89000000003', 'Иванов Д.И.'),
            ('89000000004', 'Вознесенцев И.И.'),
            ('89000000005', 'Величаев И.И.'),
            ('89000000006', 'Васильева В.В.'),
            ('89000000007', 'Башинова М.А.'),
            ('89000000008', 'Ландова А.А.'),
            ('89000000009', 'Кузнецова А.Д.'),
            ('89000000010', 'Хохлова В.В.')
    '''
)

# Таблица Дополнительные услуги
cursor.executescript(
    '''
        CREATE TABLE IF NOT EXISTS additional_services (
            additional_services_id INTEGER PRIMARY KEY AUTOINCREMENT,
            additional_services_name VARCHAR(20) NOT NULL,
            additional_services_price INTEGER NOT NULL
        )
    '''
)

cursor.executescript(
    '''
        INSERT INTO additional_services (additional_services_name, additional_services_price) 
        VALUES
            ('завтрак', 5000),
            ('услуги прачечной', 2000),
            ('спа', 7000),
            ('тренажерный зал', 10000),
            ('бассейн', 6000)
    '''
)

#Таблица Бронь номера
cursor.executescript(
    '''
        CREATE TABLE IF NOT EXISTS booking (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id VARCHAR(11) NOT NULL,
            room_id INTEGER NOT NULL,
            check_in_date DATE NOT NULL,
            check_out_date DATE NOT NULL,
            room_status_id INTEGER NOT NULL,
            live_in_date DATE,
            live_out_date DATE,

            FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
            FOREIGN KEY (room_id) REFERENCES room(room_id) ON DELETE CASCADE,
            FOREIGN KEY (room_status_id) REFERENCES room_status(room_status_id) ON DELETE CASCADE
        )
    '''
)

# Даты и статусы номеров
cursor.executescript(
    '''
        INSERT INTO booking (user_id, room_id, check_in_date, check_out_date, room_status_id) 
        VALUES 
            ('89000000001', 1, '2024-01-15', '2024-01-25', 1),
            ('89000000002', 2, '2024-01-16', '2024-01-20', 1),
            ('89000000003', 3, '2024-01-15', '2024-01-24', 1),
            ('89000000004', 4, '2024-01-18', '2024-01-25', 1),
            ('89000000005', 5, '2024-01-16', '2024-02-01', 1)
    '''
)


cursor.executescript(
    '''
        CREATE TABLE IF NOT EXISTS booking_additional_services (
            booking_id INTEGER,
            additional_services_id INTEGER,

            PRIMARY KEY (booking_id, additional_services_id),
            FOREIGN KEY (booking_id) REFERENCES booking(booking_id) ON DELETE CASCADE,
            FOREIGN KEY (additional_services_id) REFERENCES additional_services(additional_services_id) ON DELETE CASCADE
        )
    '''
)


cursor.executescript(
    '''
        INSERT INTO booking_additional_services (booking_id, additional_services_id) 
        VALUES
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 1)
    '''
)

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()