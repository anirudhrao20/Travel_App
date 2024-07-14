import unittest
from datetime import datetime, timedelta
from db import connect_db, create_trip, get_all_trips, get_trip_by_id, add_flight_to_trip, add_hotel_to_trip, \
    add_activity_to_day, get_itinerary_for_trip, delete_trip


class TestTravelPlanner(unittest.TestCase):

    def setUp(self):
        # Create a test database connection
        self.conn = connect_db()
        self.conn.execute("DELETE FROM trips")
        self.conn.execute("DELETE FROM activities")
        self.conn.commit()

    def tearDown(self):
        # Close the database connection
        self.conn.close()

    def test_create_trip(self):
        title = "Test Trip"
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=7)
        create_trip(title, start_date, end_date)

        trips = get_all_trips()
        self.assertEqual(len(trips), 1)
        self.assertEqual(trips[0].title, title)
        self.assertEqual(trips[0].start_date, start_date.strftime("%Y-%m-%d"))
        self.assertEqual(trips[0].end_date, end_date.strftime("%Y-%m-%d"))

    def test_get_trip_by_id(self):
        title = "Another Test Trip"
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=5)
        create_trip(title, start_date, end_date)

        trips = get_all_trips()
        trip_id = trips[0].id

        retrieved_trip = get_trip_by_id(trip_id)
        self.assertIsNotNone(retrieved_trip)
        self.assertEqual(retrieved_trip.title, title)

    def test_add_flight_to_trip(self):
        create_trip("Flight Test Trip", datetime.now().date(), datetime.now().date() + timedelta(days=3))
        trip = get_all_trips()[0]
        flight_details = "Test Flight AA123"
        add_flight_to_trip(trip.id, flight_details)

        updated_trip = get_trip_by_id(trip.id)
        self.assertEqual(updated_trip.flight_details, flight_details)

    def test_add_hotel_to_trip(self):
        create_trip("Hotel Test Trip", datetime.now().date(), datetime.now().date() + timedelta(days=3))
        trip = get_all_trips()[0]
        hotel_details = "Test Hotel XYZ"
        add_hotel_to_trip(trip.id, hotel_details)

        updated_trip = get_trip_by_id(trip.id)
        self.assertEqual(updated_trip.hotel_details, hotel_details)

    def test_add_and_get_activity(self):
        create_trip("Activity Test Trip", datetime.now().date(), datetime.now().date() + timedelta(days=3))
        trip = get_all_trips()[0]
        activity_date = datetime.now().date().strftime("%Y-%m-%d")
        add_activity_to_day(trip.id, activity_date, "Test Activity", "10:00 AM", 50.0, None, "123 Test St", "ABC123")

        activities = get_itinerary_for_trip(trip.id, activity_date)
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]['name'], "Test Activity")
        self.assertEqual(activities[0]['time'], "10:00 AM")
        self.assertEqual(activities[0]['cost'], 50.0)

    def test_delete_trip(self):
        create_trip("Delete Test Trip", datetime.now().date(), datetime.now().date() + timedelta(days=3))
        trip = get_all_trips()[0]
        delete_trip(trip.id)

        trips = get_all_trips()
        self.assertEqual(len(trips), 0)


if __name__ == '__main__':
    unittest.main()
