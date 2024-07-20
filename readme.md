
# Travel Planner App

## Overview
The Travel Planner App is a comprehensive web-based application designed to assist users in organizing and managing their trips efficiently. The application enables users to create trips, add detailed itineraries for each day, and manage flight and hotel details. Users can input information manually, catering to their trip needs. The primary objective of this project is to provide a user-friendly and simple platform for trip planning and management, ensuring all trip details are organized in one place and accessible.

## Features
- **Create and Manage Trips:** Easily create trips and add details such as itineraries, flights, and hotel reservations.
- **User-Friendly Interface:** Built using Streamlit, providing an interactive and responsive design.
- **Data Persistence:** All trip details are stored in an SQLite database, ensuring data is saved and retrievable.

## Intended Audience
- Travelers who want to manage and organize their trip details.
- Travel agencies that manage trips for clients.
- Individuals who frequently travel for business or leisure and need an organized way to plan their trips.

## Requirements
- **Libraries and Dependencies:** The necessary libraries for this project are:
  - `streamlit`
  - `sqlite3`
  - `datetime`

## Usage
1. **Run the application:**
    ```sh
    streamlit run app.py
    ```
2. **Interact with the application through the Streamlit interface:**
    - **Create Trip:** Use the "Create Trip" menu to add new trips with details such as title, start date, end date, flight details, and hotel details.
    - **View Trips:** Use the "View Trips" menu to see all trips, delete trips, and view associated activities.

## Project Structure
- `app.py`: Main application file that integrates the frontend and backend, handles user interactions, and displays the interface.
- `db.py`: Manages the SQLite database, including creating tables, inserting, retrieving, and deleting data.
- `test_db.py`: Contains unit tests for the database operations.
- `requirements.txt`: List of required libraries.

## Data Design
- **Trip:**
  ```json
  {
      "id": Integer,
      "title": String,
      "start_date": String,
      "end_date": String,
      "flight_details": String,
      "hotel_details": String,
      "itinerary": String
  }
  ```
- **Activity:**
  ```json
  {
      "id": Integer,
      "trip_id": Integer,
      "date": String,
      "name": String,
      "time": String,
      "cost": Float,
      "file_path": String,
      "address": String,
      "confirmation": String
  }
  ```

## Testing
1. **Run the tests:**
    ```sh
    python -m unittest test_db.py
    ```
2. **Testing Methods:**
    - Unit Testing: Test individual functions for correctness.
    - Integration Testing: Ensure different parts of the application work together correctly.
    - User Acceptance Testing: Validate the application with real users to ensure it meets their needs.

## Implementation Plan
- **Week 1:** Project setup and database operations.
- **Week 2:** Develop the user interface.
- **Week 3:** Integrate frontend and backend.
- **Week 4:** Testing and debugging.
- **Week 5:** Final deployment and user acceptance testing.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgements
Special thanks to the course instructors and fellow students for their support and guidance throughout the project.
