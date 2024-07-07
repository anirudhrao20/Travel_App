# Travel Planner App

A comprehensive web-based travel planner application built using Streamlit and SQLite. This application allows users to create and manage trips, including detailed itineraries with activities, flight details, and hotel reservations. Users can manually input details or search via API for flight and hotel information.

## Overview

The Travel Planner App is designed to help users organize their trips efficiently. Users can create trips by specifying the trip title and dates. For each trip, users can add activities for each day, including details like time, cost, and confirmation numbers. The app also allows users to manage flight and hotel details, either by manual entry or via API search.

## Features

- **Trip Management**: Create, view, and manage trips.
- **Detailed Itinerary**: Add activities for each day, including optional details like time, cost, address, and confirmation numbers.
- **Flight Details**: Add flight details manually or search via API.
- **Hotel Reservations**: Add hotel details manually or search via API.
- **File Uploads**: Attach files to activities for reference.

## Sections Breakdown

### 1. Setup

#### 1.1. Requirements

Ensure you have the required packages installed. You can install them using the `requirements.txt` file provided:

```bash
pip install -r requirements.txt
```

2. Application Structure
2.1. app.py

The main application file that sets up the Streamlit interface and handles user interactions.

Trip Creation: Users can create new trips by providing a title and date range. This is handled through a modal dialog.
Trip Details View: Once a trip is selected, users can view and manage trip details, including activities, flights, and hotels.
Activity Management: Users can add activities to each day of the trip through a modal dialog.
Flight and Hotel Management: Users can add flight and hotel details either manually or via an API search.
2.2. db.py

Handles database operations using SQLite. It includes functions to create trips, add activities, and retrieve trip and activity details.

Database Connection: Establishes a connection to the SQLite database and sets up the schema if it doesn't already exist.
Trip Operations: Functions to create a trip, get all trips, and get a trip by ID.
Activity Operations: Functions to add an activity to a day and retrieve the itinerary for a trip.
Flight and Hotel Operations: Functions to add flight and hotel details.
3. Detailed Guide
3.1. Running the Application

To run the application, execute the following command in your terminal:

```bash
streamlit run app.py
```
3.2. Creating a Trip

Click on the "Create Trip" button.
Enter the trip title, start date, and end date.
Click "Add Trip" to save the trip.
3.3. Viewing and Managing Trips

Select a trip from the list of saved trips.
View trip details including dates, flight, and hotel information.
Add activities for each day by clicking on "Add Activity".
Add flight details by clicking on "Add Flight".
Add hotel details by clicking on "Add Hotel".
3.4. Adding Activities

Click on "Add Activity" for a specific day.
Enter the activity name, time, cost, and other optional details.
Click "Add Activity" to save the activity.
3.5. Adding Flight Details

Click on "Add Flight".
Choose to add details manually or search via API.
If adding manually, enter the flight cost, seat number, airline, flight number, and confirmation number.
Click "Add Flight" to save the details.
3.6. Adding Hotel Details

Click on "Add Hotel".
Choose to add details manually or search via API.
If adding manually, enter the hotel cost, name, address, number of rooms, and confirmation number.
Click "Add Hotel" to save the details.
Conclusion

The Travel Planner App is a robust tool for organizing and managing trips, providing a user-friendly interface to add detailed trip information. Whether planning a simple vacation or a complex itinerary, this app offers the features needed to ensure every detail is accounted for.