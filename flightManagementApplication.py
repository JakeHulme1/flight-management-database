import sqlite3
from datetime import datetime

# Connect to the database
def connnect_to_db():
    return sqlite3.connect("FlightManagement.db")

# Function to format datetime in ISO 8601 format and convert to UTC
# This function will be used when users input data to ensure its in ISO 8601 format
def format_datetime_iso_8601(dt_str):
    dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S')
    return dt.isoformat()



#   SQL Queries and Databse Interaction
#  - Flight Retrieval: Retrieve flights based on multiple criteria, such as destination, status, or departure date.
#  - Schedule Modification: Update flight schedules (e.g., change departure time or status).
#  - Pilot Assignment: Assign pilots to flights and retrieve information about pilot schedules.
#  - Destination Management: View and update destination information as required.
#  - Include additional queries that summarise data, such as the number of flights to each destination or the
#   number of flights assigned to a pilot

# SQL QUERIES:
# Flight retrieval:
# - All flights: 
#       SELECT * FROM FLights;
# - Show all destinations (doesn't repeat any location): 
#       SELECT DISTINCT City AS 'City', Country AS 'Country' FROM (Flights NATURAL JOIN Airports); 
# - Show all cancelled flights:
#       SELECT * FROM Flights WHERE Flight_Status = 'Cancelled';
# - Show all flights in date order:
#       SELECT * FROM Flights

#   Application Development in Python (using SQLite3)
#  - Develop a command-line interface (CLI) in Python using the sqlite3 library to interact with your SQLite
#    database.
#  - The application should present a menu with options such as:
#     - Add a New Flight
#     - View Flights by Criteria - destination, status, departure date
#     - Update Flight Information - change departure time, arrival time and status
#     - Assign Pilot to Flight - add/remove pilots, retrieve info about schedules
#     - View Pilot Schedule
#     - View/Update Destination Information
#     - Ensure the interface displays results clearly and allows users to make changes based on input.

# Command line interface design