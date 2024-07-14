import sqlite3

def connect_db():
    """
    Establish a connection to the SQLite database.

    Returns:
        sqlite3.Connection: A connection object to the database.
    """
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
    """
    Create a new trip in the database.

    Args:
        title (str): The title of the trip.
        start_date (datetime.date): The start date of the trip.
        end_date (datetime.date): The end date of the trip.
    """
    conn = connect_db()
    conn.execute('INSERT INTO trips (title, start_date, end_date) VALUES (?, ?, ?)',
                 (title, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def get_all_trips():
    """
    Retrieve all trips from the database.

    Returns:
        list: A list of Trip objects representing all trips in the database.
    """
    conn = connect_db()
    cursor = conn.execute('SELECT * FROM trips')
    trips = cursor.fetchall()
    conn.close()
    return [
        Trip(id=row[0], title=row[1], start_date=row[2], end_date=row[3], flight_details=row[4], hotel_details=row[5],
             itinerary=row[6]) for row in trips]

def get_trip_by_id(trip_id):
    """
    Retrieve a specific trip from the database by its ID.

    Args:
        trip_id (int): The ID of the trip to retrieve.

    Returns:
        Trip: A Trip object representing the requested trip, or None if not found.
    """
    conn = connect_db()
    cursor = conn.execute('SELECT * FROM trips WHERE id = ?', (trip_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Trip(id=row[0], title=row[1], start_date=row[2], end_date=row[3], flight_details=row[4],
                    hotel_details=row[5], itinerary=row[6])
    return None

def add_flight_to_trip(trip_id, flight_details):
    """
    Add flight details to a specific trip.

    Args:
        trip_id (int): The ID of the trip to update.
        flight_details (str): The flight details to add.
    """
    conn = connect_db()
    conn.execute('UPDATE trips SET flight_details = ? WHERE id = ?', (flight_details, trip_id))
    conn.commit()
    conn.close()

def add_hotel_to_trip(trip_id, hotel_details):
    """
    Add hotel details to a specific trip.

    Args:
        trip_id (int): The ID of the trip to update.
        hotel_details (str): The hotel details to add.
    """
    conn = connect_db()
    conn.execute('UPDATE trips SET hotel_details = ? WHERE id = ?', (hotel_details, trip_id))
    conn.commit()
    conn.close()

def add_activity_to_day(trip_id, date, name, time, cost, file_path, address, confirmation):
    """
    Add an activity to a specific day of a trip.

    Args:
        trip_id (int): The ID of the trip.
        date (str): The date of the activity.
        name (str): The name of the activity.
        time (str): The time of the activity.
        cost (float): The cost of the activity.
        file_path (str): The file path for any attached documents.
        address (str): The address of the activity.
        confirmation (str): The confirmation number for the activity.
    """
    conn = connect_db()
    conn.execute(
        'INSERT INTO activities (trip_id, date, name, time, cost, file_path, address, confirmation) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (trip_id, date, name, time, cost, file_path, address, confirmation))
    conn.commit()
    conn.close()

def get_itinerary_for_trip(trip_id, date):
    """
    Retrieve the itinerary for a specific trip and date.

    Args:
        trip_id (int): The ID of the trip.
        date (str): The date for which to retrieve the itinerary.

    Returns:
        list: A list of dictionaries containing activity details.
    """
    conn = connect_db()
    cursor = conn.execute('SELECT * FROM activities WHERE trip_id = ? AND date = ?', (trip_id, date))
    activities = cursor.fetchall()
    conn.close()
    return [
        {'name': row[3], 'time': row[4], 'cost': row[5], 'file_path': row[6], 'address': row[7], 'confirmation': row[8]}
        for row in activities]

def delete_trip(trip_id):
    """
    Delete a trip and all its associated activities from the database.

    Args:
        trip_id (int): The ID of the trip to delete.
    """
    conn = connect_db()
    conn.execute('DELETE FROM activities WHERE trip_id = ?', (trip_id,))
    conn.execute('DELETE FROM trips WHERE id = ?', (trip_id,))
    conn.commit()
    conn.close()

class Trip:
    """
    Represents a trip with its details.

    Attributes:
        id (int): The unique identifier of the trip.
        title (str): The title of the trip.
        start_date (str): The start date of the trip.
        end_date (str): The end date of the trip.
        flight_details (str): Details about the flight.
        hotel_details (str): Details about the hotel.
        itinerary (str): The itinerary of the trip.
    """
    def __init__(self, id, title, start_date, end_date, flight_details, hotel_details, itinerary):
        self.id = id
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.flight_details = flight_details
        self.hotel_details = hotel_details
        self.itinerary = itinerary