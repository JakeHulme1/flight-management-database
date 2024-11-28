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
    previous_ID = cursor.fetchone()[0]

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

    # Generate a new Flight_ID
    new_flight_id = create_new_flight_id()

    # Get user to input flight info
    new_flight_number = input("Enter flight number: ")
    new_airline_name = input("Enter airline name: ")
    new_aircraft_id = input("Enter aircraft ID: ")
    new_departure_airport = input("Enter departure airport IATA code: ")
    new_arrival_airport = input("Enter arrival airport IATA code: ")
    new_departure_time = input("Enter departure date and time in ISO 8601 format(YYYY-MM-DDThh:mm): ")
    new_arrival_time = input("Enter arrival date and time (YYYY-MM-DDThh:mm): ")
    new_flight_status = input("Enter flight status: ")

    # Add all of this data to a new row in the Flights table
    # Need to ensure that the names of the values to be inserted are in the same order as the column names in the Flights table
    cursor.execute("""
        INSERT INTO FLIGHTS (Flight_ID, Flight_Number, Airline_Name, Aircraft_ID, Departure, Arrival, Flight_Status, 
                   Departure_Airport_IATA, Arrival_Airport_IATA)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (new_flight_id, new_flight_number, new_airline_name, new_aircraft_id, new_departure_time,
        new_arrival_time, new_flight_status, new_departure_airport, new_arrival_airport))
    
    # Commit the changes and close the connection
    connection.commit()
    print("Flight added successfully!")
    cursor.close()
    connection.close()

# Function to remove flights
def remove_flight():
    
    # Establish connection and creat cursor
    connection = connect_to_db()
    cursor = connection.cursor()

    # Get user input, ask for flight_ID as this is unique for every flight and avoids removing multiple flights
    flight_id_remove = input("Please enter the ID of the flight that you wish to remove: ")

    # CHeck that flight ID exists
    cursor.execute("SELECT 1 FROM Flights WHERE Flight_ID = ?", (flight_id_remove,))
    flight_exists = cursor.fetchone() # This returns none if no flight ID exists for user input

    #Proceed with update if flight exists
    if flight_exists:

        cursor.execute("DELETE FROM Flights WHERE Flight_ID = ?",
                    (flight_id_remove,))

        # Commit the changes and close the connection
        connection.commit()
        print("Flight removed successfully!")

    else:
        print(f"No flight found with ID {flight_id_remove}. Please check the ID and try again.")
    
    cursor.close()
    connection.close()

# Function to update flight information
def update_flight_info():

    # Establish connection and create cursor
    connection = connect_to_db()
    cursor = connection.cursor()

    # Prompt user to input ID of flight they are updating
    flight_id = input("Please enter the ID of the flight you are updating the information for: ")

     # CHeck that flight ID exists
    cursor.execute("SELECT 1 FROM Flights WHERE Flight_ID = ?", (flight_id,))
    flight_exists = cursor.fetchone() # This returns none if no flight ID exists for user input

     #Proceed with update if flight exists
    if flight_exists:

        # Prompt user to enter what criteria they are updating
        criteria = input("The criteria you can update are: \n - Flight_ID\n - Flight_Number\n - Airline_Name\n - Aircraft_ID\n - Departure\n - Arrival\n - Flight_Status\n - Departure_Airport_IATA\n - Arrival_Airport_IATA\n\nPlease enter the criteria you are updating: ")

        #  Check that criteria exists as a column header in the Flights table
        valid_criteria = ["Flight_ID", "Flight_Number", "Airline_Name", "Aircraft_ID", 
            "Departure", "Arrival", "Flight_Status", "Departure_Airport_IATA", "Arrival_Airport_IATA"]
        if (criteria in valid_criteria):

            # Instruct user to input any datetime strings in ISO 8601 format
            if ((criteria == 'Arrival') or (criteria == 'Departure')):
                print(f"Ensure you type the date and time of {criteria} in ISO8601 format: YYYY-MM-DDThh:mm")

            # Prompt user to enter the new value for the specified criteria
            new_value = input(f"Please enter the new value for {criteria}: ")

            cursor.execute(f"UPDATE Flights SET {criteria} = ? WHERE Flight_ID = ?",
                        (new_value, flight_id,))
        
            # Commit the changes and close the connection
            connection.commit()
            print("Flight updated successfully!")

        else:
            print("That criteria does not exist! Make sure you type the criteria exactly as it appears in the Flights table.")
    
    else:
        print(f"No flight found with ID {flight_id}. Please check the ID and try again.")
    
    cursor.close()
    connection.close()

# Function to assign a pilot to a flight
def assign_pilot_to_flight():
    
    # Establish connection and create cursor
    connection = connect_to_db()
    cursor = connection.cursor()

    # Get user to input flight
    flight_id = input("Enter the ID number of the flight you are assigning a pilot to: ")

     # CHeck that flight ID exists
    cursor.execute("SELECT 1 FROM Flights WHERE Flight_ID = ?", (flight_id,))
    flight_exists = cursor.fetchone() # This returns none if no flight ID exists for user input

    # If flight exists for that ID
    if flight_exists:

        # Get user to input Pilot info
        pilot_id = input(f"Enter the ID number of the pilot which you are assigning to flight {flight_id}: ")

        # Check an ID for this pilot exists
        cursor.execute("SELECT 1 FROM Pilots WHERE Pilot_ID = ?", (pilot_id,))
        pilot_exists = cursor.fetchone()

        # Get the pilot role for this flight
        role = input(f"Input Pilot {pilot_id}'s role for this flight (Captain or First Officer): ")

        # If it does, assign pilot to flight
        if pilot_exists:
            
            # Check if the pilot has already been assigned to flight so we don't break composite primary key constraint
            cursor.execute("SELECT 1 FROM Flight_Pilot WHERE Flight_ID = ? AND Pilot_ID = ?", (flight_id, pilot_id))
            assignment_exists = cursor.fetchone()

            # If there is no existing assignment of pilot to flight, perfomr the assignment
            if not assignment_exists:

                cursor.execute("""INSERT INTO Flight_Pilot (Flight_ID, Pilot_ID, Role)
                            VALUES(?, ?, ?)""",
                            (flight_id, pilot_id, role))
                connection.commit()
                print(f"Pilot {pilot_id} successfully assigned to flight {flight_id}")

            # If this assignment already exists, tell the user
            else:
                print(f"Pilot {pilot_id} is already assigned to flight {flight_id}.")

        else:
            print(f"No pilot found with ID {pilot_id}. Please check the ID and try again.")

    else:
        print(f"No flight found with ID {flight_id}. Please check the ID and try again.")

    # Close cursor and connection
    cursor.close()
    connection.close()

    # # Use the cursor object to run SQL commands. execute() runs it as a string literal so we can directly type the SQL command
    #     cursor.execute("SELECT * FROM Flights;")

    #     # Store all the flights
    #     flights = cursor.fetchall()

    #     # Check if any flights were found
    #     if flights:
    #         # Print all the flights
    #         for flight in flights:
    #             print(flight)

    #     else:
    #         print("No flights found for the given criteria.")

def view_pilot_schedule():
    
    # Establish connection and create cursor
    connection = connect_to_db()
    cursor = connection.cursor()

    #Get user input and check that pilot_ID exists
    pilot_id = input("Enter 'ALL' to see all pilot's schedules or enter the pilot ID number for the pilot who you wish to see the schedule for: ")

    # If user types 'ALL' show whole schedule
    if pilot_id == "ALL":

        cursor.execute("""SELECT Pilot_ID, Full_Name, Flight_ID, Flight_Number, Departure, Arrival, Flight_Status,
                       Departure_Airport_IATA, Arrival_Airport_IATA
                       FROM (Pilots NATURAL JOIN Flight_Pilot NATURAL JOIN Flights)
                       ORDER BY Pilot_ID, Flight_ID""")
        schedule = cursor.fetchall()

        # Check if there is a schedule and print is there is
        if schedule:
            for item in schedule:
                print(item)
        else:
            print("There is currently no flight schedule") 
        
        # Close cursor and connection
        cursor.close()
        connection.close()

    # Check an ID for this pilot exists
    cursor.execute("SELECT 1 FROM Pilots WHERE Pilot_ID = ?", (pilot_id,))
    pilot_exists = cursor.fetchone()

    # If pilot exists, display their sechedule
    if pilot_exists:

        # Grab all the relevant items from the tables
        cursor.execute("""SELECT Pilot_ID, Full_Name, Flight_ID, Flight_Number, Departure, Arrival, Flight_Status,
                       Departure_Airport_IATA, Arrival_Airport_IATA
                       FROM (Pilots NATURAL JOIN Flight_Pilot NATURAL JOIN Flights)
                       WHERE Pilot_ID = ?
                       ORDER BY Pilot_ID, Flight_ID""", (pilot_id,))
        # Store all of these in the schedule list
        schedule = cursor.fetchall()

        # If data has been collected it print it, if not, no data exists for that pilot
        if schedule:
            for item in schedule:
                print(item)
        else:
            print(f"Pilot with ID number {pilot_id} has no schedule.")
    else:
        print(f"Pilot with ID number {pilot_id} does not exist! Check the ID and try again")

    # Close connection and cursor
    cursor.close()
    connection.close()
    
def view_destination_info():
    
    # Create connection and cursor object
    connection = connect_to_db()
    cursor = connection.cursor()

    # Ask user what destination they want to see flights for
    destination = input("Enter the IATA of the destination airport (e.g. Sydney is SYD): ")

    # Grab all relevant items from table by joining Airport_IATA in Airport with Arrival_Airport_IATA in FLights
    cursor.execute("""SELECT 
                   Flight.Flight_Number
                   Flight.Departure_Airport_IATA AS "Origin"
                   Flight.Airline_Name, 
                   Flight.Arrival
                   Flight.Flight_Status
                   FROM""")



# Main function to display terminal and implement functions
def main():
    # Menu is constantly printed until user exits
    while True:
        # Options
        print("Options for the Flight Management Database:\n")
        print("1) View flights by criteria")
        print("2) Add a new flight to the database")
        print("3) Remove a flight from the database")
        print("4) Update flight information")
        print("5) Assign a pilot to a flight")
        print("6) View pilot schedule")
        print("7) View destination information (shows all flights to a particular destination)")
        print("8) Update destination information")
        print("9) Quit\n")

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
        elif choice == "4":
            update_flight_info()
        elif choice == "5":
            assign_pilot_to_flight()
        elif choice == "6":
            view_pilot_schedule()
        elif choice == "9":
            print("Exitted Program")
            break
        else:
            print("Invalid Input! Make sure you enter the number as a digit for the option you wish to execute.")

# Ensures the main function is called
if __name__ == "__main__":
    main()