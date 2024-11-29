import sqlite3
from datetime import datetime, timedelta # Use this to format date and time into ISO 8601 and perform date calculations
import random # Used to randomly populate database

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
    FOREIGN KEY(Aircraft_ID) REFERENCES Aircrafts(Aircraft_ID), 
    FOREIGN KEY(Departure_Airport_IATA) REFERENCES Airport(Airport_IATA), 
    FOREIGN KEY(Arrival_Airport_IATA) REFERENCES Airport(Airport_IATA)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Aircrafts (
    Aircraft_ID INTEGER PRIMARY KEY, 
    Aircraft_Model TEXT NOT NULL, 
    Age INTEGER NOT NULL, 
    Registration_Number INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Airports (
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
    ("JFK", "New York", "USA", "-05:00"),
    ("LHR", "London", "UK", "+00:00"),
    ("CDG", "Paris", "France", "+01:00"),
    ("HND", "Tokyo", "Japan", "+09:00"),
    ("DXB", "Dubai", "UAE", "+04:00"),
    ("SYD", "Sydney", "Australia", "+10:00"),
    ("FRA", "Frankfurt", "Germany", "+01:00"),
    ("SIN", "Singapore", "Singapore", "+08:00"),
    ("AMS", "Amsterdam", "Netherlands", "+01:00"),
    ("HKG", "Hong Kong", "Hong Kong SAR China", "+08:00"),
    ("LAX", "Los Angeles", "USA", "-08:00"),
    ("ORD", "Chicago", "USA", "-06:00"),
    ("GRU", "Sao Paulo", "Brazil", "-03:00"),
    ("YYZ", "Toronto", "Canada", "-05:00"),
    ("ICN", "Seoul", "South Korea", "+09:00")
]

aircrafts = [
    (1, "Boeing 737", 5, "N73701"),
    (2, "Airbus A320", 3, "A32002"),
    (3, "Boeing 777", 7, "N77703"),
    (4, "Airbus A380", 2, "A38004"),
    (5, "Boeing 787", 4, "N78705"),
    (6, "Airbus A350", 6, "A35006"),
    (7, "Boeing 747", 10, "N74707"),
    (8, "Airbus A330", 8, "A33008"),
    (9, "Boeing 767", 9, "N76709"),
    (10, "Airbus A340", 11, "A34010"),
    (11, "Boeing 757", 12, "N75711"),
    (12, "Airbus A321", 1, "A32112"),
    (13, "Boeing 727", 15, "N72713"),
    (14, "Airbus A319", 13, "A31914"),
    (15, "Boeing 737 MAX", 2, "N737M15")
]

pilots = [
    (1, 'John Doe', 'LN12345', 'Captain', 15),
    (2, 'Jane Smith', 'LN23456', 'First Officer', 10),
    (3, 'Jim Brown', 'LN34567', 'Captain', 20),
    (4, 'Jake White', 'LN45678', 'First Officer', 8),
    (5, 'Jill Green', 'LN56789', 'Captain', 12),
    (6, 'Jack Black', 'LN67890', 'First Officer', 7),
    (7, 'Jerry Blue', 'LN78901', 'Captain', 18),
    (8, 'Janet Yellow', 'LN89012', 'First Officer', 9),
    (9, 'Jordan Purple', 'LN90123', 'Captain', 14),
    (10, 'Jasmine Orange', 'LN01234', 'First Officer', 6),
    (11, 'Jason Red', 'LN12346', 'Captain', 16),
    (12, 'Jessica Pink', 'LN23457', 'First Officer', 11),
    (13, 'Jeremy Gray', 'LN34568', 'Captain', 19),
    (14, 'Julia Brown', 'LN45679', 'First Officer', 5),
    (15, 'Jeff White', 'LN56780', 'Captain', 13)
]

# Generate sample data for Flights table
# Create the list
flights = []
flight_id = 1

for i in range(15):

    # Randomly select the flight no, airline, aircraft ID (from list of aircrafts), departure and arrival airport
    flight_number = random.randint(1000, 9999)
    airline_name = random.choice(["British Airways", "Emirates", "Singapore Airlines"])
    aircraft_id = random.randint(1, len(aircrafts))
    departure_airport = random.choice(airports)[0]

    # Chooses arrival airport so long as the departure != arrival
    arrival_airport = random.choice([airport[0] for airport in airports if airport[0] != departure_airport])

    # Randomly select the departure and calculate the arrival using time delta
    departure_time = datetime.now() + timedelta(days=random.randint(1, 30))
    arrival_time = departure_time + timedelta(hours=random.randint(2, 12))
    
    # Format the departure and arrival times to not include seconds (this is unnecessary)
    formatted_departure_time = departure_time.strftime('%Y-%m-%dT%H:%M')
    formatted_arrival_time = arrival_time.strftime('%Y-%m-%dT%H:%M')

    # Randomyly select the flight status
    flight_status = random.choice(["On Time", "Delayed", "Cancelled"])
    
    # Ensure all departure and arrivals are in ISO 8601 format and add the above info into a tuple in the flights list
    flights.append((flight_id, flight_number, airline_name, aircraft_id, formatted_departure_time, formatted_arrival_time, flight_status, departure_airport, arrival_airport))
    
    # Increment the ID for next row
    flight_id += 1

# Generate data for flight_pilot data
flight_pilot = [
    (1, 1, 'Captain'), (1, 2, 'First Officer'), (1, 3, 'First Officer'),
    (2, 4, 'Captain'), (2, 5, 'First Officer'),
    (3, 6, 'Captain'), (3, 7, 'First Officer'), (3, 8, 'First Officer'),
    (4, 9, 'Captain'), (4, 10, 'First Officer'),
    (5, 11, 'Captain'), (5, 12, 'First Officer'), (5, 13, 'First Officer'),
    (6, 14, 'Captain'), (6, 15, 'First Officer'),
    (7, 1, 'Captain'), (7, 4, 'First Officer'), (7, 6, 'First Officer'),
    (8, 2, 'Captain'), (8, 5, 'First Officer'),
    (9, 3, 'Captain'), (9, 7, 'First Officer'), (9, 8, 'First Officer'),
    (10, 9, 'Captain'), (10, 10, 'First Officer'),
    (11, 11, 'Captain'), (11, 12, 'First Officer'), (11, 13, 'First Officer'),
    (12, 14, 'Captain'), (12, 15, 'First Officer'),
    (13, 1, 'Captain'), (13, 2, 'First Officer'), (13, 3, 'First Officer'),
    (14, 4, 'Captain'), (14, 5, 'First Officer'),
    (15, 6, 'Captain'), (15, 7, 'First Officer'), (15, 8, 'First Officer')
]



# Insert data into the tables, replace repeated data to avoid defying unique constraints for primary keys
cursor.executemany("INSERT OR REPLACE INTO Airports VALUES (?, ?, ?, ?)", airports)
cursor.executemany("INSERT OR REPLACE INTO Aircrafts VALUES (?, ?, ?, ?)", aircrafts)
cursor.executemany("INSERT OR REPLACE INTO Pilots VALUES (?, ?, ?, ?, ?)", pilots)
cursor.executemany("INSERT OR REPLACE INTO Flights VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", flights)
cursor.executemany("INSERT OR REPLACE INTO Flight_Pilot VALUES (?, ?, ?)", flight_pilot)

# Commit the changes and close the connection
connection.commit()
connection.close()