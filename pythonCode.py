import sqlite3
from datetime import datetime # Use this to format date and time into ISO 8601

# The sqlite3.connect() function returns a Connection object that is used to interact with the SQLite
# database held in the file FlightManagement.db. The FlightManagement.db file is created automatically by sqlite3.connect()
# if it does not already exist on our computer.
connection = sqlite3.connect("FlightManagement.db")

# Cursor allows us to to send SQL statements to a SQLite database using cursor.execute()
cursor = connection.cursor()

# Create the tables in the database if they don't exist already (refer to ER diagram for entity structure and relations)
# Also set up primary and foreign keys
cursor.execute("""
CREATE TABLE IF NOT EXISTS Flights (
    Flight_ID INTEGER PRIMARY KEY, 
    Flight_Number INTEGER NOT NULL, 
    Airline_Name TEXT NOT NULL, 
    Aircraft_ID INTEGER NOT NULL, 
    Departure TEXT NOT NULL, 
    Arrival TEXT NOT NULL, 
    Flight_Status TEXT NOT NULL, 
    Departure_Airport_IATA TEXT NOT NULL, 
    Arrival_Airport_IATA TEXT NOT NULL, 
    FOREIGN KEY(Aircraft_ID) REFERENCES Aircraft(Aircraft_ID), 
    FOREIGN KEY(Departure_Airport_IATA) REFERENCES Airport(Airport_IATA), 
    FOREIGN KEY(Arrival_Airport_IATA) REFERENCES Airport(Airport_IATA)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Aircraft (
    Aircraft_ID INTEGER PRIMARY KEY, 
    Aircraft_Model TEXT NOT NULL, 
    Age INTEGER NOT NULL, 
    Registration_Number INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Airport (
    Airport_IATA TEXT PRIMARY KEY, 
    City TEXT NOT NULL, 
    Country TEXT NOT NULL, 
    Timezone TEXT NOT NULL
)
""")

# This table has a composite primary key
cursor.execute("""
CREATE TABLE IF NOT EXISTS Flight_Pilot (
    Flight_ID INTEGER, 
    Pilot_ID INTEGER, 
    Role TEXT NOT NULL, 
    PRIMARY KEY(Flight_ID, Pilot_ID) 
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Pilots (
    Pilot_ID INTEGER PRIMARY KEY, 
    Full_Name TEXT NOT NULL, 
    Licence_Number INTEGER NOT NULL, 
    Rank TEXT NOT NULL, 
    Years_Of_Experience INTEGER NOT NULL
)
""")

# Data for the tables are stored in a list, with each row being a tuple
airports = [
    ('JFK', 'New York', 'USA', 'UTC-05:00'),
    ('LAX', 'Los Angeles', 'USA', 'UTC-08:00'),
    ('ORD', 'Chicago', 'USA', 'UTC-06:00'),
    ('DFW', 'Dallas', 'USA', 'UTC-06:00'),
    ('DEN', 'Denver', 'USA', 'UTC-07:00'),
    ('ATL', 'Atlanta', 'USA', 'UTC-05:00'),
    ('SEA', 'Seattle', 'USA', 'UTC-08:00'),
    ('MIA', 'Miami', 'USA', 'UTC-05:00'),
    ('SFO', 'San Francisco', 'USA', 'UTC-08:00'),
    ('LAS', 'Las Vegas', 'USA', 'UTC-08:00')
]

aircrafts = [
    (1, 'Boeing 737', 10, 12345),
    (2, 'Airbus A320', 8, 23456),
    (3, 'Boeing 777', 12, 34567),
    (4, 'Airbus A380', 5, 45678),
    (5, 'Boeing 787', 7, 56789),
    (6, 'Airbus A350', 6, 67890),
    (7, 'Boeing 747', 15, 78901),
    (8, 'Airbus A330', 9, 89012),
    (9, 'Boeing 767', 11, 90123),
    (10, 'Airbus A340', 13, 12346)
]

pilots = [
    (1, 'John Doe', 11111, 'Captain', 20),
    (2, 'Jane Smith', 22222, 'First Officer', 15),
    (3, 'Jim Brown', 33333, 'Captain', 18),
    (4, 'Jake White', 44444, 'First Officer', 12),
    (5, 'Jill Green', 55555, 'Captain', 22),
    (6, 'Jerry Black', 66666, 'First Officer', 14),
    (7, 'Janet Blue', 77777, 'Captain', 19),
    (8, 'Jack Yellow', 88888, 'First Officer', 16),
    (9, 'Julie Red', 99999, 'Captain', 21),
    (10, 'Jason Purple', 10101, 'First Officer', 13)
]

# Function to format datetime in ISO 8601 format and convert to UTC
# This function will be used when users input data to ensure its in ISO 8601 format
def format_datetime_iso_8601(dt_str):
    dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S')
    return dt.isoformat()

# Use the function here to ensure all data is in ISO 8601 format (I manually entered it in ISO 8601 but this just double checks its in the format)
flights = [
    (1, 1001, 'Delta Airlines', 1, format_datetime_iso_8601('2023-01-01T08:00:00'), format_datetime_iso_8601('2023-01-01T12:00:00'), 'On Time', 'JFK', 'LAX'),
    (2, 1002, 'American Airlines', 2, format_datetime_iso_8601('2023-01-02T09:00:00'), format_datetime_iso_8601('2023-01-02T13:00:00'), 'Delayed', 'LAX', 'ORD'),
    (3, 1003, 'United Airlines', 3, format_datetime_iso_8601('2023-01-03T10:00:00'), format_datetime_iso_8601('2023-01-03T14:00:00'), 'Cancelled', 'ORD', 'DFW'),
    (4, 1004, 'Southwest Airlines', 4, format_datetime_iso_8601('2023-01-04T11:00:00'), format_datetime_iso_8601('2023-01-04T15:00:00'), 'On Time', 'DFW', 'DEN'),
    (5, 1005, 'Alaska Airlines', 5, format_datetime_iso_8601('2023-01-05T12:00:00'), format_datetime_iso_8601('2023-01-05T16:00:00'), 'Delayed', 'DEN', 'ATL'),
    (6, 1006, 'JetBlue Airways', 6, format_datetime_iso_8601('2023-01-06T13:00:00'), format_datetime_iso_8601('2023-01-06T17:00:00'), 'On Time', 'ATL', 'SEA'),
    (7, 1007, 'Spirit Airlines', 7, format_datetime_iso_8601('2023-01-07T14:00:00'),format_datetime_iso_8601('2023-01-07T18:00:00'), 'Cancelled', 'SEA', 'MIA'),
    (8, 1008, 'Frontier Airlines', 8, format_datetime_iso_8601('2023-01-08T15:00:00'), format_datetime_iso_8601('2023-01-08T19:00:00'), 'On Time', 'MIA', 'SFO'),
    (9, 1009, 'Hawaiian Airlines', 9, format_datetime_iso_8601('2023-01-09T16:00:00'), format_datetime_iso_8601('2023-01-09T20:00:00'), 'Delayed', 'SFO', 'LAS'),
    (10, 1010, 'Allegiant Air', 10, format_datetime_iso_8601('2023-01-10T17:00:00'), format_datetime_iso_8601('2023-01-10T21:00:00'), 'On Time', 'LAS', 'JFK')
]

flight_pilots = [
    (1, 1, 'Captain'),
    (1, 2, 'First Officer'),
    (2, 3, 'Captain'),
    (2, 4, 'First Officer'),
    (3, 5, 'Captain'),
    (3, 6, 'First Officer'),
    (4, 7, 'Captain'),
    (4, 8, 'First Officer'),
    (5, 9, 'Captain'),
    (5, 10, 'First Officer')
]

# Insert data into the tables
cursor.executemany("INSERT INTO Airport VALUES (?, ?, ?, ?)", airports)
cursor.executemany("INSERT INTO Aircraft VALUES (?, ?, ?, ?)", aircrafts)
cursor.executemany("INSERT INTO Pilots VALUES (?, ?, ?, ?, ?)", pilots)
cursor.executemany("INSERT INTO Flights VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", flights)
cursor.executemany("INSERT INTO Flight_Pilot VALUES (?, ?, ?)", flight_pilots)

# Commit the changes and close the connection
connection.commit()
connection.close()