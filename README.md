# Flight Management System

This repository contains a Python-based Flight Management System that interacts with an SQLite database to manage and query information about flights, pilots, and destinations. The system implements functionalities like viewing flights, adding flights, assigning pilots, and more, all while prioritizing data security through parameterized queries to prevent SQL injection attacks.

## Features

### Core Functionalities

- **View Flights by Criteria**: Query flights based on user-defined criteria or display all flights.
- **Add a New Flight**: Insert new flight details into the database.
- **Remove a Flight**: Delete a specific flight using its unique Flight_ID.
- **Update Flight Information**: Modify details of an existing flight.
- **Assign a Pilot to a Flight**: Assign pilots to specific flights with designated roles.
- **View Pilot Schedules**: Display flight schedules for individual pilots or all pilots.
- **View Destination Information**: Show all flights to a specific destination.
- **Count Flights to a Destination**: Retrieve the total number of flights to a specified airport.

### Security Features

- **Parameterized Queries**: All SQL queries use parameterized inputs to prevent SQL injection attacks, ensuring robust data security.
- **Validation Checks**: Includes checks to verify the existence of flight IDs, pilot IDs, and airport IATA codes before performing database operations.

## Database Schema

### Flights Table

| Column                | Description                             |
|-----------------------|-----------------------------------------|
| Flight_ID             | Unique identifier for each flight       |
| Flight_Number         | The flight number                       |
| Airline_Name          | Name of the airline                     |
| Aircraft_ID           | Unique identifier for the aircraft      |
| Departure             | Departure date and time (ISO 8601 format)|
| Arrival               | Arrival date and time (ISO 8601 format) |
| Flight_Status         | Status of the flight                    |
| Departure_Airport_IATA| IATA code of the departure airport      |
| Arrival_Airport_IATA  | IATA code of the arrival airport        |

### Pilots Table

| Column   | Description          |
|----------|----------------------|
| Pilot_ID | Unique identifier for each pilot |
| Full_Name| Name of the pilot    |

### Flight_Pilot Table

| Column   | Description          |
|----------|----------------------|
| Flight_ID| Identifier of the assigned flight |
| Pilot_ID | Identifier of the assigned pilot  |
| Role     | Role of the pilot (e.g., Captain) |

### Airports Table

| Column                | Description                             |
|-----------------------|-----------------------------------------|
| Airport_IATA          | IATA code of the airport                |
| Airport_Name          | Name of the airport                     |
| City                  | City where the airport is located       |
| Country               | Country where the airport is located    |

### Aircrafts Table

| Column                | Description                             |
|-----------------------|-----------------------------------------|
| Aircraft_ID           | Unique identifier for each aircraft     |
| Aircraft_Model        | Model of the aircraft                   |
| Airline_Name          | Name of the airline operating the aircraft|

## How to Run the Program

### Install Dependencies
Ensure Python is installed along with the required libraries:
```bash
pip install tabulate
```

## Set Up the Database
1. Create an SQLite database named FlightManagement.db.
2. Use the schema provided in the Database Schema section to create the tables.
3. Run the databaseCreation&Population.py script to populate the database with initial data.

## Run the script

Execute the Python script:
```bash
python flightManagementApplication.py
```

## Interact with the Menu

Follow the terminal prompts to perform various operations.

### Example: Parameterized Query for Security
# Example of parameterized query to prevent SQL injection
```bash
cursor.execute("SELECT * FROM Flights WHERE Flight_ID = ?", (flight_id,))
```

## Key Notes
- Ensure all date and time inputs are in ISO 8601 format (YYYY-MM-DDThh:mm).
- The program validates user inputs to align with the database schema.
- To extend the functionality, modify the existing menu options or add new database operations.
