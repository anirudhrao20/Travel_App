import streamlit as st
from db import create_trip, get_all_trips, get_trip_by_id, add_flight_to_trip, add_hotel_to_trip, add_activity_to_day, \
    get_itinerary_for_trip, delete_trip, get_flights_for_trip, get_hotels_for_trip
from datetime import datetime, timedelta

# Hide the sidebar and set the app to fullscreen
st.set_page_config(layout="wide")


@st.experimental_dialog("Create a New Trip")
def create_trip_modal():
    """
    Display a modal dialog for creating a new trip.

    This function allows users to input trip details such as title, start date, and end date.
    It then creates a new trip with the provided information.
    """
    trip_title = st.text_input('Trip Title')
    start_date = st.date_input('Start Date', value=datetime.now())
    end_date = st.date_input('End Date', value=datetime.now())

    if not trip_title:
        st.warning("Trip title is required.")
        add_trip_button_disabled = True
    else:
        add_trip_button_disabled = False

    if st.button('Add Trip', key='add_trip', disabled=add_trip_button_disabled):
        create_trip(trip_title, start_date, end_date)
        st.success('Trip added successfully!')
        st.session_state['show_trip_modal'] = False
        st.rerun()


@st.experimental_dialog("Add Activity")
def add_activity_dialog(trip_id, date):
    """
    Display a dialog for adding a new activity to a trip.

    Args:
        trip_id (int): The ID of the trip to add the activity to.
        date (str): The date of the activity in 'YYYY-MM-DD' format.

    This function allows users to input activity details and adds the activity to the specified trip and date.
    """
    activity_name = st.text_input('Activity Name')
    activity_time = st.time_input('Time')
    activity_cost = st.number_input('Cost', min_value=0.0, step=0.01)
    activity_address = st.text_input('Address (Optional)')
    activity_confirmation = st.text_input('Confirmation Number (Optional)')

    if not activity_name or activity_time is None:
        st.warning("Activity name and time are required.")
        add_activity_button_disabled = True
    else:
        add_activity_button_disabled = False

    activity_time_str = activity_time.strftime('%I:%M %p')

    if st.button('Add Activity', key=f'add_activity_dialog_btn_{trip_id}_{date}',
                 disabled=add_activity_button_disabled):
        add_activity_to_day(trip_id, date, activity_name, activity_time_str, activity_cost, None, activity_address,
                            activity_confirmation)
        st.success('Activity added successfully!')
        st.session_state['show_activity_dialog'] = False
        st.rerun()


@st.experimental_dialog("Add Flight")
def add_flight_dialog(trip_id):
    """
    Display a dialog for adding flight details to a trip.

    Args:
        trip_id (int): The ID of the trip to add the flight details to.

    This function allows users to input flight information and adds it to the specified trip.
    """
    flight_cost = st.number_input('Cost', min_value=0.0, step=0.01)
    flight_seat = st.text_input('Seat Number')
    flight_airline = st.text_input('Airline')
    flight_number = st.text_input('Flight Number')
    flight_confirmation = st.text_input('Confirmation Number')

    if not flight_airline or not flight_confirmation or not flight_number:
        st.warning("Airline, flight number, and confirmation number are required.")
        add_flight_button_disabled = True
    else:
        add_flight_button_disabled = False

    if st.button('Add Flight', key=f'add_flight_dialog_btn_{trip_id}', disabled=add_flight_button_disabled):
        add_flight_to_trip(trip_id, flight_cost, flight_seat, flight_airline, flight_number, flight_confirmation)
        st.success('Flight added successfully!')
        st.session_state['show_flight_dialog'] = False
        st.rerun()


@st.experimental_dialog("Add Hotel")
def add_hotel_dialog(trip_id):
    """
    Display a dialog for adding hotel details to a trip.

    Args:
        trip_id (int): The ID of the trip to add the hotel details to.

    This function allows users to input hotel information and adds it to the specified trip.
    """
    hotel_cost = st.number_input('Cost', min_value=0.0, step=0.01)
    hotel_name = st.text_input('Hotel Name')
    hotel_address = st.text_input('Address')
    hotel_rooms = st.number_input('Number of Rooms', min_value=1, step=1)
    hotel_confirmation = st.text_input('Confirmation Number')

    if not hotel_name or not hotel_address or not hotel_confirmation:
        st.warning("Hotel name, address, and confirmation number are required.")
        add_hotel_button_disabled = True
    else:
        add_hotel_button_disabled = False

    if st.button('Add Hotel', key=f'add_hotel_dialog_btn_{trip_id}', disabled=add_hotel_button_disabled):
        add_hotel_to_trip(trip_id, hotel_cost, hotel_name, hotel_address, hotel_rooms, hotel_confirmation)
        st.success('Hotel added successfully!')
        st.session_state['show_hotel_dialog'] = False
        st.rerun()


def show_trip_detail(trip_id):
    """
    Display detailed information about a specific trip.

    Args:
        trip_id (int): The ID of the trip to display.

    This function shows trip details, including dates, flight and hotel information, and the itinerary.
    It also provides options to add activities, flights, hotels, and delete the trip.
    """
    trip = get_trip_by_id(trip_id)
    start_date = datetime.strptime(trip.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(trip.end_date, "%Y-%m-%d")
    num_days = (end_date - start_date).days + 1
    header_title = f'{trip.title} ({start_date.year})'

    col1, col2 = st.columns([4, 1])
    with col1:
        st.header(header_title)
    with col2:
        if st.button('Back to all trips', key='back_to_all_trips'):
            del st.session_state['selected_trip_id']
            st.rerun()

    st.write(
        f'**Dates:** {start_date.strftime("%m/%d/%Y")} - {end_date.strftime("%m/%d/%Y")} ({num_days} day{"s" if num_days > 1 else ""})')

    flights = get_flights_for_trip(trip_id)
    if flights:
        st.write('**Flight Details:**')
        for flight in flights:
            st.write(
                f'Cost: ${flight["cost"]}, Seat: {flight["seat"]}, Airline: {flight["airline"]}, Flight Number: {flight["flight_number"]}, Confirmation: {flight["confirmation"]}')

    hotels = get_hotels_for_trip(trip_id)
    if hotels:
        st.write('**Hotel Details:**')
        for hotel in hotels:
            st.write(
                f'Cost: ${hotel["cost"]}, Name: {hotel["name"]}, Address: {hotel["address"]}, Rooms: {hotel["rooms"]}, Confirmation: {hotel["confirmation"]}')

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('Add Flight', key=f'add_flight_{trip_id}'):
            st.session_state['show_flight_dialog'] = True
            add_flight_dialog(trip.id)
    with col2:
        if st.button('Add Hotel', key=f'add_hotel_{trip_id}'):
            st.session_state['show_hotel_dialog'] = True
            add_hotel_dialog(trip.id)
    with col3:
        if st.button('Delete Trip', key=f'delete_trip_{trip_id}', type="primary"):
            delete_trip(trip_id)
            del st.session_state['selected_trip_id']
            st.success('Trip deleted successfully!')
            st.rerun()

    # Display the itinerary as a calendar view
    st.header('Itinerary')
    current_date = start_date
    while current_date <= end_date:
        st.subheader(current_date.strftime("%A, %B %d, %Y"))
        activities = get_itinerary_for_trip(trip.id, current_date.strftime("%Y-%m-%d"))

        # Sort activities by time
        if activities:
            sorted_activities = sorted(activities, key=lambda x: datetime.strptime(x['time'], '%I:%M %p') if x[
                'time'] else datetime.max.time())
            for activity in sorted_activities:
                activity_info = []
                if activity['time']:
                    activity_info.append(f"**{activity['time']}:**")
                if activity['name']:
                    activity_info.append(f"{activity['name']}\n")
                if activity['cost']:
                    activity_info.append(f"**Cost:** ${activity['cost']}\n")
                if activity['address']:
                    activity_info.append(f"**Address:** {activity['address']}\n")
                if activity['confirmation']:
                    activity_info.append(f"**Confirmation:** {activity['confirmation']}\n")

                st.write('\n'.join(activity_info))

        if st.button('Add Activity', key=f'add_activity_btn_{trip_id}_{current_date.strftime("%Y-%m-%d")}'):
            st.session_state['show_activity_dialog'] = True
            add_activity_dialog(trip.id, current_date.strftime("%Y-%m-%d"))

        current_date += timedelta(days=1)


# Main content

if 'selected_trip_id' not in st.session_state:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title('Travel Planner')
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