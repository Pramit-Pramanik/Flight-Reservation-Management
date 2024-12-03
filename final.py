import pickle as pic
import mysql.connector
import random
import string

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mantu123',
    'database': 'airport_book'
}

# File to store user data
USER_DATA_FILE = "user_data.dat"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def admin_dashboard():
    """Dashboard for the admin user."""
    while True:
        print("\nAdmin Dashboard:")
        print("1. View Airline Data")
        print("2. Add Airline")
        print("3. Delete Airline")
        print("4. View Destination Data")
        print("5. Add Destination")
        print("6. Delete Destination")
        print("7. Change flight prices")
        print("8. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            view_airline_data()
        elif choice == "2":
            add_airline()
        elif choice == "3":
            delete_airline()
        elif choice == "4":
            view_destination_data()
        elif choice == "5":
            add_destination()
        elif choice == "6":
            delete_destination()
        elif choice == "7":
            admin_change_price()
        elif choice == "8":
            print("Logged out from admin account.")
            break
        else:
            print("Invalid choice. Please try again.")

# Admin Functions
def admin_login():
    """Admin login function."""
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Admin login successful!")
        admin_dashboard()
    else:
        print("Invalid admin credentials.")

def view_airline_data():
    """View all records in airline_data."""
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM airline_data;")
        records = cursor.fetchall()
        print("\nAirline Data:")
        for record in records:
            print(f"A_No: {record[0]}, A_Name: {record[1]}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_airline():
    """Add a new airline to airline_data."""
    a_no = input("Enter Airline Number (A_No): ")
    a_name = input("Enter Airline Name (A_Name): ")
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "INSERT INTO airline_data (A_No, A_Name) VALUES (%s, %s);"
        cursor.execute(query, (a_no, a_name))
        connection.commit()
        print("Airline added successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def admin_change_price():
    """Allow admin to change the prices of flights."""
    try:
        # Establish a connection to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Fetch and display all flights with current prices
        query = """
            SELECT destination_data.Dest_Name, airline_data.A_name, destination_data.Price
            FROM destination_data
            INNER JOIN airline_data ON destination_data.A_No = airline_data.A_no;
        """
        cursor.execute(query)
        flights = cursor.fetchall()

        if not flights:
            print("No flights available to update.")
            return

        print("\nAvailable Flights and Current Prices:")
        for index, (destination, airline, price) in enumerate(flights, start=1):
            print(f"{index}. Destination: {destination}, Airline: {airline}, Current Price: {price}")

        # Select a flight to update
        choice = int(input("\nEnter the number of the flight to update the price: "))
        if choice < 1 or choice > len(flights):
            print("Invalid choice. Please try again.")
            return

        selected_flight = flights[choice - 1]
        destination, airline, current_price = selected_flight

        print(f"\nYou selected: Destination - {destination}, Airline - {airline}, Current Price - {current_price}")

        # Input the new price
        new_price = float(input("Enter the new price: "))
        if new_price <= 0:
            print("Invalid price. Price must be greater than 0.")
            return

        # Update the price in the database
        update_query = """
            UPDATE destination_data
            SET Price = %s
            WHERE Dest_Name = %s AND A_No = (
                SELECT A_no FROM airline_data WHERE A_name = %s
            );
        """
        cursor.execute(update_query, (new_price, destination, airline))
        connection.commit()

        print(f"\nPrice updated successfully! New price for {destination} by {airline}: {new_price}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def delete_airline():
    """Delete an airline from airline_data."""
    a_no = input("Enter Airline Number (A_No) to delete: ")
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "DELETE FROM airline_data WHERE A_No = %s;"
        cursor.execute(query, (a_no,))
        connection.commit()
        print("Airline deleted successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def view_destination_data():
    """View all records in destination_data."""
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM destination_data;")
        records = cursor.fetchall()
        print("\nDestination Data:")
        for record in records:
            print(f"D_No: {record[0]}, A_No: {record[1]}, Dest_Name: {record[2]}, Total_Seats: {record[3]}, Price: {record[4]}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_destination():
    """Add a new destination to destination_data."""
    d_no = input("Enter Destination Number (D_No): ")
    a_no = input("Enter Airline Number (A_No): ")
    dest_name = input("Enter Destination Name: ")
    total_seats = int(input("Enter Total Seats: "))
    price = float(input("Enter Price: "))
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = """
            INSERT INTO destination_data (D_No, A_No, Dest_Name, Total_Seats, Price) 
            VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(query, (d_no, a_no, dest_name, total_seats, price))
        connection.commit()
        print("Destination added successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def delete_destination():
    """Delete a destination from destination_data."""
    d_no = input("Enter Destination Number (D_No) to delete: ")
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "DELETE FROM destination_data WHERE D_No = %s;"
        cursor.execute(query, (d_no,))
        connection.commit()
        print("Destination deleted successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Utility Functions
def load_user_data():
    """Load user data from a binary file."""
    try:
        with open(USER_DATA_FILE, "rb") as file:
            return pic.load(file)
    except (FileNotFoundError, EOFError):
        return {}

def save_user_data(data):
    """Save user data to a binary file."""
    with open(USER_DATA_FILE, "wb") as file:
        pic.dump(data, file)

def generate_pnr():
    """Generate a unique 10-character alphanumeric PNR."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# User Functions
def register_user(username, password):
    """Register a new user."""
    user_data = load_user_data()
    if username in user_data:
        print("Username already exists. Please choose a different username.")
        return False

    user_data[username] = password
    save_user_data(user_data)
    print("User registered successfully!")
    return True

def login_user(username, password):
    """Log in an existing user."""
    user_data = load_user_data()
    if username in user_data and user_data[username] == password:
        print("Login successful!")
        user_dashboard(username)  # Redirect to dashboard
        return True
    else:
        print("Invalid username or password.")
        return False

# Database Functions


def check_and_create_databases():
    """Check if airline_data and destination_data exist; create and populate them if not."""
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check and create airline_data table
        cursor.execute("SHOW TABLES LIKE 'airline_data';")
        if not cursor.fetchone():
            print("Creating airline_data table...")
            cursor.execute("""
                CREATE TABLE airline_data (
                    A_No INT PRIMARY KEY,
                    A_name VARCHAR(255) NOT NULL
                );
            """)
            print("airline_data table created.")
            populate_table_from_csv("airline_data", "/mnt/data/Airline_Data.csv", cursor)

        # Check and create destination_data table
        cursor.execute("SHOW TABLES LIKE 'destination_data';")
        if not cursor.fetchone():
            print("Creating destination_data table...")
            cursor.execute("""
                CREATE TABLE destination_data (
                    D_No INT PRIMARY KEY,
                    A_No INT,
                    Dest_Name VARCHAR(255) NOT NULL,
                    Total_Seats INT,
                    Price FLOAT,
                    FOREIGN KEY (A_No) REFERENCES airline_data(A_No)
                );
            """)
            print("destination_data table created.")
            populate_table_from_csv("destination_data", "/mnt/data/Destination_Data.csv", cursor)

        # Commit changes
        connection.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def populate_table_from_csv(table_name, file_path, cursor):
    """Populate the given table with data from the specified CSV file."""
    try:
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            rows = list(csv_reader)

            if table_name == "airline_data":
                query = "INSERT INTO airline_data (A_No, A_name) VALUES (%s, %s);"
                data = [(int(row["A_No"]), row["A_name"]) for row in rows]

            elif table_name == "destination_data":
                query = """
                    INSERT INTO destination_data (D_No, A_No, Dest_Name, Total_Seats, Price)
                    VALUES (%s, %s, %s, %s, %s);
                """
                data = [
                    (int(row["D_No"]), int(row["A_No"]), row["Dest_Name"], int(row["Total_Seats"]), float(row["Price"]))
                    for row in rows
                ]
            else:
                print(f"Unknown table: {table_name}")
                return

            cursor.executemany(query, data)
            print(f"{len(data)} records inserted into {table_name}.")

    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"Error populating {table_name} from {file_path}: {e}")


def fetch_distinct_destinations():
    """Fetch distinct destinations from the database."""
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT Dest_name FROM destination_data;")
        destinations = cursor.fetchall()
        return {index + 1: name[0] for index, name in enumerate(destinations)}
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def fetch_A_names():
    """Fetch airline names from the database."""
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT A_name FROM airline_data;")
        airlines = cursor.fetchall()
        return {index + 1: name[0] for index, name in enumerate(airlines)}
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def show_available_seats(destination, airline):
    """Display available seats for a specific destination and airline."""
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Step 1: Fetch the A_no for the given airline
        query_airline_no = "SELECT A_no FROM airline_data WHERE A_name = %s;"
        cursor.execute(query_airline_no, (airline,))
        result = cursor.fetchone()

        if not result:
            print("Error: Airline not found in the database.")
            return False

        airline_no = result[0]

        # Step 2: Fetch available seats for the destination and airline
        query_seats = """
            SELECT Total_Seats FROM destination_data 
            WHERE Dest_Name = %s AND A_No = %s;
        """
        cursor.execute(query_seats, (destination, airline_no))
        result = cursor.fetchone()

        if not result:
            print("Error: No matching destination and airline found.")
            return False

        available_seats = result[0]
        print(f"Total available seats for {destination} by {airline}: {available_seats}")
        return available_seats

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_ticket_price(destination, airline):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = """
            SELECT Price FROM destination_data
            WHERE Dest_Name = %s AND A_No = (
                SELECT A_No FROM airline_data WHERE A_name = %s
            );
        """
        cursor.execute(query, (destination, airline))
        result = cursor.fetchone()
        return result[0] if result else None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def search_booked_flight(username):
    """Search for booked flights by username or PNR."""
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Display options for searching
        print("\nSearch Options:")
        print("1. Search by PNR")
        print("2. View all bookings by your username")
        choice = input("Enter your choice: ")

        if choice == "1":
            pnr = input("Enter the PNR: ").strip().upper()
            query = "SELECT * FROM user_booking WHERE PNR = %s;"
            cursor.execute(query, (pnr,))
        elif choice == "2":
            query = "SELECT * FROM user_booking WHERE Username = %s;"
            cursor.execute(query, (username,))
        else:
            print("Invalid choice.")
            return

        results = cursor.fetchall()
        if not results:
            print("No bookings found.")
        else:
            print("\nYour Booked Flights:")
            for row in results:
                print(f"PNR: {row[0]}, Username: {row[1]}, Destination: {row[2]}, Airline: {row[3]}, Seats: {row[4]}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def cancel_booked_flight(username):
    """Cancel a booked flight using PNR."""
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        pnr = input("Enter the PNR of the flight you want to cancel: ").strip().upper()

        # Step 1: Fetch the booking details for the given PNR
        query_fetch = """
            SELECT Destination, Airline, Seats FROM user_booking 
            WHERE PNR = %s AND Username = %s;
        """
        cursor.execute(query_fetch, (pnr, username))
        booking = cursor.fetchone()

        if not booking:
            print("Error: No matching booking found or you do not have permission to cancel this booking.")
            return

        destination, airline, booked_seats = booking

        # Step 2: Update the total seats in destination_data
        update_query = """
            UPDATE destination_data
            SET Total_Seats = Total_Seats + %s
            WHERE Dest_Name = %s AND A_No = (
                SELECT A_No FROM airline_data WHERE A_name = %s
            );
        """
        cursor.execute(update_query, (booked_seats, destination, airline))

        # Step 3: Delete the booking record
        delete_query = "DELETE FROM user_booking WHERE PNR = %s AND Username = %s;"
        cursor.execute(delete_query, (pnr, username))

        # Commit the transaction
        connection.commit()

        print(f"Booking with PNR {pnr} has been successfully canceled.")
        print(f"{booked_seats} seats have been added back to the available seats for {destination} by {airline}.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        if connection.is_connected():
            connection.rollback()  # Rollback in case of error
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def user_dashboard(username):
    """Dashboard for logged-in users."""
    while True:
        print(f"\nWelcome, {username}!")
        print("1. Book a flight")
        print("2. Search for booked flights")
        print("3. Cancel a booked flight")
        print("4. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            access_main_program(username)  # Existing booking function
        elif choice == "2":
            search_booked_flight(username)
        elif choice == "3":
            cancel_booked_flight(username)
        elif choice == "4":
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice. Please try again.")

def book_flight(username, destination, airline, seats_requested, total_cost):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        pnr = generate_pnr()
        query = """
            INSERT INTO user_booking (PNR, Username, Destination, Airline, Seats, Total_Cost) 
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(query, (pnr, username, destination, airline, seats_requested, total_cost))
        connection.commit()
        print(f"\nBooking successful! Your PNR is: {pnr}")
        print(f"Booking Summary: Destination - {destination}, Airline - {airline}, Seats - {seats_requested}, Total Cost - {total_cost}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def access_main_program(username):
    """Main program after user login."""
    print(f"\nWelcome, {username}!")

    # Destination Selection
    destinations = fetch_distinct_destinations()
    if not destinations:
        print("No destinations available.")
        return
    print("\nAvailable destinations:")
    for key, value in destinations.items():
        print(f"{key}. {value}")
    destination = None
    while destination is None:
        try:
            choice = int(input("Select your destination: "))
            destination = destinations.get(choice)
            if destination:
                print(f"You selected: {destination}")
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Enter a valid number.")

    # Airline Selection
    airlines = fetch_A_names()
    if not airlines:
        print("No airlines available.")
        return
    print("\nAvailable airlines:")
    for key, value in airlines.items():
        print(f"{key}. {value}")
    airline = None
    ticket_price = 0
    while airline is None:
        try:
            choice = int(input("Select your airline: "))
            airline = airlines.get(choice)
            if airline:
                print(f"You selected: {airline}")
                # Fetch the ticket price for the selected airline and destination
                try:
                    connection = mysql.connector.connect(**db_config)
                    cursor = connection.cursor()
                    query = """
                        SELECT Price FROM destination_data
                        WHERE Dest_Name = %s AND A_No = (
                            SELECT A_No FROM airline_data WHERE A_name = %s
                        );
                    """
                    cursor.execute(query, (destination, airline))
                    result = cursor.fetchone()
                    if result:
                        ticket_price = result[0]
                        print(f"The ticket price for {destination} by {airline} is: {ticket_price}")
                    else:
                        print("Error: Price data not found for the selected destination and airline.")
                        return
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                    return
                finally:
                    if connection.is_connected():
                        cursor.close()
                        connection.close()
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Enter a valid number.")

    # Check Available Seats
    seats_available = show_available_seats(destination, airline)
    if not seats_available:
        return

    # Seats Selection
    seats_requested = 0
    while seats_requested <= 0:
        try:
            seats_requested = int(input("Enter the number of seats you want to book: "))
            if seats_requested <= 0:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")

    # Booking Process
    if seats_requested > seats_available:
        print("Error: Not enough seats available.")
        return

    # Generate PNR
    pnr = generate_pnr()

    # Calculate Total Cost
    total_cost = seats_requested * ticket_price

    # Save Booking to Database and Update Seats
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Start a transaction
        connection.start_transaction()

        # Insert booking details
        insert_query = """
            INSERT INTO user_booking (PNR, Username, Destination, Airline, Seats, Total_Cost) 
            VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_query, (pnr, username, destination, airline, seats_requested, total_cost))

        # Update available seats in destination_data
        update_query = """
            UPDATE destination_data
            SET Total_Seats = Total_Seats - %s
            WHERE Dest_Name = %s AND A_No = (
                SELECT A_No FROM airline_data WHERE A_name = %s
            );
        """
        cursor.execute(update_query, (seats_requested, destination, airline))

        # Commit the transaction
        connection.commit()

        print(f"\nBooking successful! Your PNR is: {pnr}")
        print(f"Booking Summary: Destination - {destination}, Airline - {airline}, Seats - {seats_requested}, Total Cost - {total_cost}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        connection.rollback()  # Rollback in case of any error
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def main():
    """Main function to handle registration, user login, and admin login."""
     
    while True:
        print("\nWelcome! Please choose an option:")
        print("1. Register as User")
        print("2. User Login")
        print("3. Admin Login")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter a username: ")
            password = input("Enter a password (must be alphanumeric and at least 8 characters long): ")
            if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
                print("Invalid password. Please try again.")
            else:
                register_user(username, password)
        elif choice == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            login_user(username, password)
        elif choice == "3":
            admin_login()
        elif choice == "4":
            print("Thank you! Goodbye.")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    check_and_create_databases()
    main()
