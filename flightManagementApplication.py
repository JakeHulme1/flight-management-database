import sqlite3
from datetime import datetime

# Connect to the database
def connect_to_db():
    return sqlite3.connect("FlightManagement.db")

# Function to format datetime in ISO 8601 format and convert to UTC
# This function will be used when users input data to ensure its in ISO 8601 format
# def format_datetime_iso_8601(dt_str):
#     dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S')
#     return dt.isoformat()

# Function to view flights by criteria
def view_flights():

    # Establish connection with database
    connection = connect_to_db()

    # Create cursor object to execute SQL commands and queries
    cursor = connection.cursor()

    # Get user input for criteria
    print("The available criteria for flights are:\n - Flight_ID\n - Flight_Number\n - Airline_Name\n - Aircraft_ID\n - Departure\n - Arrival\n - Flight_Status\n - Departure_Airport_IATA\n - Arrival_Airport_IATA\n\n")
    criteria = input(f"Please enter a criteria or type 'ALL' to see all flights. Note, ensure your criteria matches with one of the above crieria:\n ")
    

    # Print all flights if user types 'ALL'
    if (criteria.upper() == 'ALL'):

        # Use the cursor object to run SQL commands. execute() runs it as a string literal so we can directly type the SQL command
        cursor.execute("SELECT * FROM Flights;")

        # Store all the flights
        flights = cursor.fetchall()

        # Check if any flights were found
        if flights:
            # Print all the flights
            for flight in flights:
                print(flight)

        else:
            print("No flights found for the given criteria.")

        # Close connection to database and cursor - note close cursor first so that the connection cannot be closed while the cursor is in use
        cursor.close()
        connection.close()
        print("\n\n")

    # If user didn't type 'ALL'
    else:

        #  Check that criteria exists as a column header in the Flights table
        valid_criteria = ["Flight_ID", "Flight_Number", "Airline_Name", "Aircraft_ID", 
        "Departure", "Arrival", "Flight_Status", "Departure_Airport_IATA", "Arrival_Airport_IATA"]
        if (criteria in valid_criteria):

            # Instruct user to input any datetime strings in ISO 8601 format
            if ((criteria == 'Arrival') or (criteria == 'Departure')):
                print(f"Ensure you type the date and time of {criteria} in ISO8601 format: YYYY-MM-DDThh:mm")

            # Get specific criteria user wants to see (e.g., all flights going to New York)
            # Note we use a formatted string 
            criteriaSelection = input(f"Please enter the specific value for the {criteria}. E.g., for Destination_Airport_IATA you could select 'LGW' for London Gatwick Airport:\n")

            # Ensure date is in ISO8601 format
            # if ((criteria == "Departure") or (criteria == "Arrival")):
            #     criteriaSelection = format_datetime_iso_8601(criteriaSelection)

            # Formulate the SQL Query - note the formatted string to pass in the criteria
            query = f"SELECT * FROM Flights WHERE {criteria} = ?"

            # Pass the SQL Query into the execute function where the place holder value is the criteria selection the user chooses
            cursor.execute(query, (criteriaSelection,))

            # Print the flights 
            flights = cursor.fetchall()
            if flights:
                for flight in flights:
                    print(flight)
            else:
                print("No flights exist for the given criteria.")

        else:
            print("That criteria does not exist! Make sure you type the criteria exactly as it appears in the Flights table.")

        # Close cursor then connection to database
        cursor.close()
        connection.close()
        print("\n\n")

# Function to create new flight id - obeys the constraint of flight_ID being a primary key so must be unique
def create_new_flight_id():

     # Establish connection and creat cursor
    connection = connect_to_db()
    cursor = connection.cursor()

    # SQL Query returns the maximum value of Flight_ID
    cursor.execute("SELECT MAX(Flight_ID) FROM Flights")

    # Store the previous flight ID by fetching the value produced by the cursor.execute
    previous_ID = cursor.fetchone[0]

    # Return the next Flight_ID or return 1 if there are none
    if previous_ID is None:
        return 1
    else:
        return previous_ID + 1

# Function to add flights
def add_flight():

    # Establish connection and creat cursor
    connection = connect_to_db()
    cursor = connection.cursor()

    new_flight_id = input("")

    # Generate a new Flight_ID
    new_flight_id = create_new_flight_id()

    # Get user to input flight info
    new_flight_number = input("Enter flight number: ")
    new_airline_name = input("Enter airline name: ")
    new_aircraft_id = input("Enter aircraft ID: ")
    new_departure_airport = input("Enter departure airport IATA code: ")
    new_arrival_airport = input("Enter arrival airport IATA code: ")
    new_departure_time = input("Enter departure date and time in ISO 8601 format(YYYY-MM-DDThh:mm): ")
    formatted_new_departure_time = new_departure_time.strftime('%Y-%m-%dT%H:%M') # Formats it into ISO 8601 if user didn't
    new_arrival_time = input("Enter arrival date and time (YYYY-MM-DDThh:mm): ")
    formatted_new_arrival_time = new_arrival_time.strftime('%Y-%m-%dT%H:%M') # Formats it into ISO 8601 if user didn't
    new_flight_status = input("Enter flight status: ")

    # Add all of this data to a new row in the Flights table
    cursor.execute("""
        INSERT INTO FLIGHTS"""

# Function to remove flights
def remove_flight():
    return



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


def main():
    # Menu is constantly printed until user exits
    while True:
        # Options
        print("Options for the Flight Management Database:\n")
        print("1) View flights by criteria")
        print("2) Add a new flight to the database")
        print("3) Remove a flight from the database")
        print("4) INSERT OPTION")
        print("5) INSERT OPTION")
        print("4) INSERT OPTION")
        print("7) Quit\n")

        # Get user input
        choice = input("Enter the number of the option you wish to execute: ")
        choice = choice.strip()  # Takes off any leading or trailing white space

        # Call the function relating to the option that user selected
        if choice == "1":
            view_flights()
        elif choice == "2":
            add_flight()
        elif choice == "3":
            remove_flight()
        elif choice == "7":
            print("Exitted Program")
            break
        else:
            print("Invalid Input! Make sure you enter the number as a digit for the option you wish to execute.")

# Ensures the main function is called
if __name__ == "__main__":
    main()