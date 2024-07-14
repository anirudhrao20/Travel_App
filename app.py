import streamlit as st
from db import create_trip, get_all_trips, get_trip_by_id, add_flight_to_trip, add_hotel_to_trip, add_activity_to_day, \
    get_itinerary_for_trip, delete_trip
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium
from api import search_flights, search_hotels

"""
Travel Planner Application

This Streamlit application allows users to create and manage travel plans,
including trips, activities, flights, and hotel bookings.
"""

# Hide the sidebar and set the app to fullscreen
st.set_page_config(layout="wide")

# Initialize geolocator
geolocator = Nominatim(user_agent="travel_planner")


@st.experimental_dialog("Create a New Trip")
def create_trip_modal():
    """
    Display a modal dialog for creating a new trip.

    This function handles the user interface for inputting trip details
    and creates a new trip in the database upon submission.
    """
    trip_title = st.text_input('Trip Title')
    start_date = st.date_input('Start Date', value=datetime.now(), format="MM/DD/YYYY")
    end_date = st.date_input('End Date', value=datetime.now(), format="MM/DD/YYYY")

    if st.button('Add Trip', key='add_trip'):
        create_trip(trip_title, start_date, end_date)
        st.success('Trip added successfully!')
        st.session_state['show_trip_modal'] = False
        st.rerun()


@st.experimental_dialog("Add Activity")
def add_activity_dialog(trip_id, date):
    """
    Display a dialog for adding an activity to a trip.

    Args:
        trip_id (int): The ID of the trip to add the activity to.
        date (str): The date for which to add the activity.
    """
    activity_name = st.text_input('Activity Name')
    activity_time = st.text_input('Time (e.g., 8:00 AM, 7:00 PM)', value='')
    activity_cost = st.number_input('Cost', min_value=0.0, step=0.01)
    activity_file = st.file_uploader('Upload File (Optional)', type=['pdf', 'jpg', 'jpeg', 'png'])
    activity_address = st.text_input('Address (Optional)')
    activity_confirmation = st.text_input('Confirmation Number (Optional)')
    if st.button('Add Activity', key=f'add_activity_dialog_btn_{trip_id}_{date}'):
        file_path = None
        if activity_file is not None:
            file_path = f"uploads/{activity_file.name}"
            with open(file_path, "wb") as f:
                f.write(activity_file.getbuffer())
        add_activity_to_day(trip_id, date, activity_name, activity_time, activity_cost, file_path, activity_address,
                            activity_confirmation)
        st.success('Activity added successfully!')
        st.session_state['show_activity_dialog'] = False
        st.rerun()


@st.experimental_dialog("Add Flight")
def add_flight_dialog(trip_id):
    """
    Display a dialog for adding flight details to a trip.

    Args:
        trip_id (int): The ID of the trip to add the flight to.
    """
    trip = get_trip_by_id(trip_id)
    origin = st.text_input('Origin', value='Enter origin IATA code')
    destination = st.text_input('Destination', value='Enter destination IATA code')
    departure_date = st.date_input('Departure Date', value=datetime.strptime(trip.start_date, "%Y-%m-%d"))

    if st.button('Search Flights', key='search_flights'):
        flights = search_flights(origin, destination, departure_date.strftime("%Y-%m-%d"))
        st.write(flights)  # Display the flights or customize the display as needed


@st.experimental_dialog("Add Hotel")
def add_hotel_dialog(trip_id):
    """
    Display a dialog for adding hotel details to a trip.

    Args:
        trip_id (int): The ID of the trip to add the hotel to.
    """
    trip = get_trip_by_id(trip_id)
    location = st.text_input('Location', value='Enter location ID')
    check_in_date = st.date_input('Check-in Date', value=datetime.strptime(trip.start_date, "%Y-%m-%d"))
    check_out_date = st.date_input('Check-out Date', value=datetime.strptime(trip.end_date, "%Y-%m-%d"))

    if st.button('Search Hotels', key='search_hotels'):
        hotels = search_hotels(location, check_in_date.strftime("%Y-%m-%d"), check_out_date.strftime("%Y-%m-%d"))
        st.write(hotels)  # Display the hotels or customize the display as needed


def show_trip_detail(trip_id):
    """
    Display detailed information about a specific trip.

    Args:
        trip_id (int): The ID of the trip to display.
    """
    trip = get_trip_by_id(trip_id)
    st.header(trip.title)
    st.subheader(f"{trip.start_date} to {trip.end_date}")
    itinerary = get_itinerary_for_trip(trip_id)
    current_date = datetime.strptime(trip.start_date, "%Y-%m-%d")

    while current_date <= datetime.strptime(trip.end_date, "%Y-%m-%d"):
        st.write(f"### {current_date.strftime('%A, %B %d, %Y')}")
        activities = itinerary.get(current_date.strftime("%Y-%m-%d"), [])
        for activity in activities:
            st.write(f"**{activity['name']}** at {activity['time']} - ${activity['cost']:.2f}")
            if activity['address']:
                st.write(f"**Address:** {activity['address']}")
                location = geolocator.geocode(activity['address'])
                if location:
                    map_ = folium.Map(location=[location.latitude, location.longitude], zoom_start=15)
                    folium.Marker([location.latitude, location.longitude], popup=activity['address']).add_to(map_)
                    st_folium(map_, width=700, height=500)
            if activity['confirmation']:
                st.write(f"**Confirmation:** {activity['confirmation']}")
            if activity['file_path']:
                st.write(f"[View Attachment]({activity['file_path']})")

        if st.button('Add Activity', key=f'add_activity_btn_{trip_id}_{current_date.strftime("%Y-%m-%d")}'):
            st.session_state['show_activity_dialog'] = True
            add_activity_dialog(trip.id, current_date.strftime("%Y-%m-%d"))

        current_date += timedelta(days=1)


def main():
    """
    Main function to run the Streamlit application.

    This function sets up the main page layout and handles the primary
    user interactions for the Travel Planner app.
    """
    st.title('Travel Planner')

    if 'selected_trip_id' not in st.session_state:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.header('Travel Planner')
        with col2:
            if st.button("Create Trip", key="create_trip_btn"):
                st.session_state['show_trip_modal'] = True

        if 'show_trip_modal' in st.session_state and st.session_state['show_trip_modal']:
            create_trip_modal()

        trips = get_all_trips()

        if trips:
            st.header('Saved Trips')
            for trip in trips:
                trip_date = datetime.strptime(trip.start_date, "%Y-%m-%d")
                if st.button(f'{trip.title} ({trip_date.year})', key=f'trip_{trip.id}'):
                    st.session_state['selected_trip_id'] = trip.id
                    st.rerun()
        else:
            st.write("No trips available.")
    else:
        show_trip_detail(st.session_state['selected_trip_id'])

        if st.button('Add Flight', key='add_flight'):
            add_flight_dialog(st.session_state['selected_trip_id'])

        if st.button('Add Hotel', key='add_hotel'):
            add_hotel_dialog(st.session_state['selected_trip_id'])


if __name__ == "__main__":
    main()