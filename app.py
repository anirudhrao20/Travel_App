import streamlit as st
from db import create_trip, get_all_trips, get_trip_by_id, add_flight_to_trip, add_hotel_to_trip, add_activity_to_day, \
    get_itinerary_for_trip, delete_trip
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import st_folium

# Hide the sidebar and set the app to fullscreen
st.set_page_config(layout="wide")

# Initialize geolocator
geolocator = Nominatim(user_agent="travel_planner")


# Function to handle the trip creation modal
@st.experimental_dialog("Create a New Trip")
def create_trip_modal():
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
    manual_entry = st.radio("Choose an option", ("Add Manually", "Search via API"))

    if manual_entry == "Add Manually":
        flight_cost = st.number_input('Cost', min_value=0.0, step=0.01)
        flight_seat = st.text_input('Seat Number')
        flight_airline = st.text_input('Airline')
        flight_number = st.text_input('Flight Number')
        flight_confirmation = st.text_input('Confirmation Number')
        if st.button('Add Flight', key=f'add_flight_dialog_btn_{trip_id}'):
            flight_details = f"Cost: ${flight_cost}, Seat: {flight_seat}, Airline: {flight_airline}, Flight Number: {flight_number}, Confirmation: {flight_confirmation}"
            add_flight_to_trip(trip_id, flight_details)
            st.success('Flight added successfully!')
            st.session_state['show_flight_dialog'] = False
            st.rerun()
    else:
        # API search implementation here
        st.write("API search functionality to be implemented.")


@st.experimental_dialog("Add Hotel")
def add_hotel_dialog(trip_id):
    manual_entry = st.radio("Choose an option", ("Add Manually", "Search via API"))

    if manual_entry == "Add Manually":
        hotel_cost = st.number_input('Cost', min_value=0.0, step=0.01)
        hotel_name = st.text_input('Hotel Name')
        hotel_address = st.text_input('Address')
        hotel_rooms = st.number_input('Number of Rooms', min_value=1, step=1)
        hotel_confirmation = st.text_input('Confirmation Number')
        if st.button('Add Hotel', key=f'add_hotel_dialog_btn_{trip_id}'):
            hotel_details = f"Cost: ${hotel_cost}, Name: {hotel_name}, Address: {hotel_address}, Rooms: {hotel_rooms}, Confirmation: {hotel_confirmation}"
            add_hotel_to_trip(trip_id, hotel_details)
            st.success('Hotel added successfully!')
            st.session_state['show_hotel_dialog'] = False
            st.rerun()
    else:
        # API search implementation here
        st.write("API search functionality to be implemented.")


def show_trip_detail(trip_id):
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

    if num_days is 1:
        st.write(f'**Dates:** {start_date.strftime("%m/%d/%Y")} - {end_date.strftime("%m/%d/%Y")} ({num_days} day)')
    else:
        st.write(f'**Dates:** {start_date.strftime("%m/%d/%Y")} - {end_date.strftime("%m/%d/%Y")} ({num_days} days)')
    st.write(f'**Flight Details:** {trip.flight_details}')
    if st.button('Add Flight', key=f'add_flight_{trip_id}'):
        st.session_state['show_flight_dialog'] = True
        add_flight_dialog(trip.id)
    st.write(f'**Hotel Details:** {trip.hotel_details}')
    if st.button('Add Hotel', key=f'add_hotel_{trip_id}'):
        st.session_state['show_hotel_dialog'] = True
        add_hotel_dialog(trip.id)

    if st.button('Delete Trip', key=f'delete_trip_{trip_id}'):
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
        if activities:
            for activity in activities:
                activity_info = []
                if activity['time']:
                    activity_info.append(f"**{activity['time']}:**")
                if activity['name']:
                    activity_info.append(f"{activity['name']}\n")
                if activity['cost']:
                    activity_info.append(f"**Cost:** ${activity['cost']}\n")
                if activity['address']:
                    activity_info.append(f"**Address:** {activity['address']}\n")
                    location = geolocator.geocode(activity['address'])
                    if location:
                        map_ = folium.Map(location=[location.latitude, location.longitude], zoom_start=15)
                        folium.Marker([location.latitude, location.longitude], popup=activity['address']).add_to(map_)
                        st_folium(map_, width=700, height=500)
                if activity['confirmation']:
                    activity_info.append(f"**Confirmation:** {activity['confirmation']}\n")
                if activity['file_path']:
                    activity_info.append(f"[View Attachment]({activity['file_path']})")

                st.write('\n'.join(activity_info))

        if st.button('Add Activity', key=f'add_activity_btn_{trip_id}_{current_date.strftime("%Y-%m-%d")}'):
            st.session_state['show_activity_dialog'] = True
            add_activity_dialog(trip.id, current_date.strftime("%Y-%m-%d"))

        current_date += timedelta(days=1)


# Main content
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
