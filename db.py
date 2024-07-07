import sqlite3


def connect_db():
    conn = sqlite3.connect('trips.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            start_date TEXT,
            end_date TEXT,
            flight_details TEXT,
            hotel_details TEXT,
            itinerary TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER,
            date TEXT,
            name TEXT,
            time TEXT,
            cost REAL,
            file_path TEXT,
            address TEXT,
            confirmation TEXT,
            FOREIGN KEY (trip_id) REFERENCES trips (id)
        )
    ''')
    return conn


def create_trip(title, start_date, end_date):
    conn = connect_db()
    conn.execute('INSERT INTO trips (title, start_date, end_date) VALUES (?, ?, ?)',
                 (title, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()


def get_all_trips():
    conn = connect_db()
    cursor = conn.execute('SELECT * FROM trips')
    trips = cursor.fetchall()
    conn.close()
    return [
        Trip(id=row[0], title=row[1], start_date=row[2], end_date=row[3], flight_details=row[4], hotel_details=row[5],
             itinerary=row[6]) for row in trips]


def get_trip_by_id(trip_id):
    conn = connect_db()
    cursor = conn.execute('SELECT * FROM trips WHERE id = ?', (trip_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Trip(id=row[0], title=row[1], start_date=row[2], end_date=row[3], flight_details=row[4],
                    hotel_details=row[5], itinerary=row[6])
    return None


def add_flight_to_trip(trip_id, flight_details):
    conn = connect_db()
    conn.execute('UPDATE trips SET flight_details = ? WHERE id = ?', (flight_details, trip_id))
    conn.commit()
    conn.close()


def add_hotel_to_trip(trip_id, hotel_details):
    conn = connect_db()
    conn.execute('UPDATE trips SET hotel_details = ? WHERE id = ?', (hotel_details, trip_id))
    conn.commit()
    conn.close()


def add_activity_to_day(trip_id, date, name, time, cost, file_path, address, confirmation):
    conn = connect_db()
    conn.execute(
        'INSERT INTO activities (trip_id, date, name, time, cost, file_path, address, confirmation) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (trip_id, date, name, time, cost, file_path, address, confirmation))
    conn.commit()
    conn.close()


def get_itinerary_for_trip(trip_id, date):
    conn = connect_db()
    cursor = conn.execute('SELECT * FROM activities WHERE trip_id = ? AND date = ?', (trip_id, date))
    activities = cursor.fetchall()
    conn.close()
    return [
        {'name': row[3], 'time': row[4], 'cost': row[5], 'file_path': row[6], 'address': row[7], 'confirmation': row[8]}
        for row in activities]


def delete_trip(trip_id):
    conn = connect_db()
    conn.execute('DELETE FROM activities WHERE trip_id = ?', (trip_id,))
    conn.execute('DELETE FROM trips WHERE id = ?', (trip_id,))
    conn.commit()
    conn.close()


class Trip:
    def __init__(self, id, title, start_date, end_date, flight_details, hotel_details, itinerary):
        self.id = id
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.flight_details = flight_details
        self.hotel_details = hotel_details
        self.itinerary = itinerary
