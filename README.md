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

## How to Run the Program

### Install Dependencies
Ensure Python is installed along with the required libraries:
```bash
pip install tabulate

## Set Up the Database

The following options can be used to create a database

### 1. Use databaseCreation
