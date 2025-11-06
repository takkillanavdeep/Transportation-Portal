#Transportation portal
#Menu Driven program using kaggle dataset and Mysql database

#importing the module
import mysql.connector
import pandas as pd

# ---------- DATABASE CONNECTION ----------
def db_connection():
    return mysql.connector.connect(host="localhost",user="root",password="scope",database="transportation_portal")

#Login
def login():
    print("========== LOGIN ==========")
    user = input("Enter username: ")
    pwd = input("Enter password: ")
    if user=="admin" and pwd=="scope":
        print("Login successful!\n")
    else:
        print("Access Denied!")
        exit()

 # ---------- IMPORT KAGGLE DATA ----------
def import_kaggle_data():
    try:
        con = db_connection()
        cur = con.cursor()
        df = pd.read_csv("transport.csv")  # CSV must include driver_id, Vehicle_type, Vehicle_number, Origin, Destination, Distance, Amount
        cur.execute("SET FOREIGN_KEY_CHECKS=0;")
        for _, row in df.iterrows():
            driver_id = int(row['driver_id'])
            cur.execute("SELECT Name FROM drivers WHERE driver_id = %s", (driver_id,))
            result = cur.fetchone()
            if result:
                driver_name = result[0]
            else:
                print(f"Driver ID {driver_id} not found in drivers table. Skipping this row.")
                continue

            cur.execute("""
                INSERT INTO trips (driver_id, Driver_name, Vehicle_type, Vehicle_number, Origin, Destination, Distance, Amount)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (driver_id, driver_name, row['Vehicle_type'], row['Vehicle_number'], row['Origin'], row['Destination'], row['Distance'], row['Amount']))
        cur.execute("SET FOREIGN_KEY_CHECKS=1;")
        con.commit()
        print("Dataset imported successfully into MySQL!")
        con.close()
    except FileNotFoundError:
        print("CSV file not found.")
    except Exception as E:
        print("Error importing dataset:", E)

# ---------- DRIVERS FUNCTIONS ----------
#Add driver into the table drivers
def add_driver():
    try:
        con = db_connection()
        cur = con.cursor()
        name = input("Enter Driver Name: ")
        gender = input("Enter Gender (M/F/O): ")
        rating = float(input("Enter Rating (0.0 - 5.0): "))
        state = input("Enter State: ")
        phone = input("Enter Phone Number: ")

        cur.execute("""
            INSERT INTO drivers (Name, Gender, Rating, State, Phone_number)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, gender, rating, state, phone))
        con.commit()
        print("Driver added successfully!")
        con.close()
        
    except Exception as E:
        print("Error adding driver:", E)

#View all the drivers present in the table
def view_all_drivers():
    con = db_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM drivers")
    rows = cur.fetchall()
    print("\n------> Display of all drivers <------")
    for r in rows:
        print(r)
    con.close()

#Search the driver
def search_driver():
    con = db_connection()
    cur = con.cursor()
    driver_id = int(input("Enter Driver ID to search: "))
    cur.execute("SELECT * FROM drivers WHERE driver_id = %s", (driver_id,))
    row = cur.fetchone()
    if row:
        print("\n-----> Driver found <-----")
        print(row)
    else:
        print("Driver not found.")
    con.close()

#Update the rating using the driver's id
def update_driver_rating():
    try:
        con = db_connection()
        cur = con.cursor()
        driver_id = int(input("Enter Driver ID to update rating: "))
        new_rating = float(input("Enter new rating (0.0 - 5.0): "))
        cur.execute("UPDATE drivers SET Rating = %s WHERE driver_id = %s", (new_rating, driver_id))
        con.commit()
        print("Rating updated successfully!")
        con.close()
    except Exception as E:
        print("Error updating rating:", E)

#Delete the driver record
def delete_driver():
    try:
        con = db_connection()
        cur = con.cursor()
        driver_id = int(input("Enter Driver ID to delete: "))
        cur.execute("DELETE FROM drivers WHERE driver_id = %s", (driver_id,))
        con.commit()
        print("Driver deleted successfully!")
        con.close()
    except Exception as E:
        print("Error deleting driver:", E)

# ---------- TRIPS FUNCTIONS ----------
#Add new trip record 
def add_trip():
    try:
        con = db_connection()
        cur = con.cursor()
        driver_id = int(input("Enter Driver ID (must exist in drivers): "))
        cur.execute("SELECT Name FROM drivers WHERE driver_id = %s", (driver_id,))
        result = cur.fetchone()
        if result:
            driver_name = result[0]
        else:
            print("Driver ID not found. Trip cannot be added.")
            con.close()
            return

        Vtype = input("Enter Vehicle Type: ")
        Vno = input("Enter Vehicle Number: ")
        Org = input("Enter Origin: ")
        Dest = input("Enter Destination: ")
        Dist = float(input("Enter Distance (in km): "))
        Amt = float(input("Enter Amount: "))

        cur.execute("""
            INSERT INTO trips (driver_id, Driver_name, Vehicle_type, Vehicle_number, Origin, Destination, Distance, Amount)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (driver_id, driver_name, Vtype, Vno, Org, Dest, Dist, Amt))
        con.commit()
        print("Trip record added successfully!")
        con.close()
    except Exception as E:
        print("Error adding new trip:", E)

#View all the trip records
def view_all_trips():
    con = db_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT t.trip_id, t.driver_id, t.Driver_name, d.Gender, d.Rating, d.State,
               t.Vehicle_type, t.Vehicle_number, t.Origin, t.Destination, t.Distance, t.Amount
        FROM trips t
        LEFT JOIN drivers d ON t.driver_id = d.driver_id
    """)
    rows = cur.fetchall()
    print("\n------> Display of all trips <------")
    for r in rows:
        print(r)
    con.close()

#Search the trips record by  driver id
def search_trip_by_driver():
    con = db_connection()
    cur = con.cursor()
    driver_id = int(input("Enter Driver ID to view trips: "))
    cur.execute("SELECT * FROM trips WHERE driver_id = %s", (driver_id,))
    rows = cur.fetchall()
    if rows:
        print("\n-----> Trips for the given driver <-----")
        for r in rows:
            print(r)
    else:
        print("No trips found for this driver.")
    con.close()

#Update the trip amount by trip id
def update_trip_amount():
    try:
        con = db_connection()
        cur = con.cursor()
        trip_id = int(input("Enter Trip ID to update amount: "))
        new_amount = float(input("Enter new amount: "))
        cur.execute("UPDATE trips SET Amount = %s WHERE trip_id = %s", (new_amount, trip_id))
        con.commit()
        print("Amount updated successfully!")
        con.close()
    except Exception as E:
        print("Error updating amount:", E)

#Delete the trip record
def delete_trip():
    try:
        con = db_connection()
        cur = con.cursor()
        trip_id = int(input("Enter Trip ID to delete: "))
        cur.execute("DELETE FROM trips WHERE trip_id = %s", (trip_id,))
        con.commit()
        print("Trip record deleted successfully!")
        con.close()
    except Exception as E:
        print("Error deleting trip:", E)

#total records, average amount, and distance summary
def analytics():
    con = db_connection()
    cur = con.cursor()
    print("\n-----> Analytics <-----")
    cur.execute("SELECT COUNT(*), AVG(Amount), SUM(Amount) FROM trips")
    count, avg_amount, total_amount = cur.fetchone()
    cur.execute("SELECT MAX(Distance), MIN(Distance) FROM trips")
    max_dist, min_dist = cur.fetchone()
    print(f"Total trips: {count}")
    print(f"Average amount: ₹{avg_amount:.2f}")
    print(f"Total amount collected: ₹{total_amount:.2f}")
    print(f"Longest distance: {max_dist} km")
    print(f"Shortest distance: {min_dist} km")
    con.close()

#Deleting the entire records in the database
def delete_all_trips():
    confirm = input("Do you want to delete all trips? (y/n): ")
    if confirm.lower() == 'y':
        con = db_connection()
        cur = con.cursor()
        cur.execute("TRUNCATE TABLE trips")
        con.commit()
        print("All trips deleted successfully!")
        con.close()

# ---------- TEMPORARY DRIVERS (Dictionary-based) ----------
# Dictionary to store temporary drivers
temporary_drivers = {}

def add_temp_driver():
    print("\n-----> Add Temporary Driver <-----")
    driver_id = input("Enter Temporary Driver ID: ")
    name = input("Enter Driver Name: ")
    gender = input("Enter Gender (M/F/O): ")
    rating = float(input("Enter Rating (0.0 - 5.0): "))
    state = input("Enter State: ")
    phone = input("Enter Phone Number: ")

    # Add to dictionary
    temporary_drivers[driver_id] = {
        "Name": name,
        "Gender": gender,
        "Rating": rating,
        "State": state,
        "Phone": phone
    }

    print("Temporary driver added successfully!")

def view_temp_drivers():
    print("\n-----> Temporary Drivers List <-----")
    if not temporary_drivers:
        print("No temporary drivers found.")
    else:
        # Convert dictionary values to list format for display
        temp_list = [
            [driver_id, info["Name"], info["Gender"], info["Rating"], info["State"], info["Phone"]]
            for driver_id, info in temporary_drivers.items()
        ]
        for driver in temp_list:
            print(driver)


if __name__ == "__main__":
    login() 

# ---------- MAIN MENU ----------
 
def main_menu():
    while True:
        print("\n========== TRANSPORTATION PORTAL ==========")
        print("1. Import Kaggle Dataset (CSV → MySQL)")
        print("------ DRIVER MANAGEMENT ------")
        print("2. Add Driver")
        print("3. View All Drivers")
        print("4. Search Driver by ID")
        print("5. Update Driver Rating")
        print("6. Delete Driver")
        print("------ TRIPS MANAGEMENT ------")
        print("7. Add New Trip")
        print("8. View All Trips")
        print("9. Search Trips by Driver ID")
        print("10. Update Trip Amount")
        print("11. Delete Trip")
        print("12. Show Analytics")
        print("13.Delete All Trips")
        print("------ TEMPORARY DRIVERS ------")
        print("14. Add Temporary Driver")
        print("15. View Temporary Drivers")
        print("16.Exit")
        print("===========================================")

        opt = input("Enter your choice (1-16): ")

        if opt == '1':
            import_kaggle_data()
        elif opt == '2':
            add_driver()
        elif opt == '3':
            view_all_drivers()
        elif opt == '4':
            search_driver()
        elif opt == '5':
            update_driver_rating()
        elif opt == '6':
            delete_driver()
        elif opt == '7':
            add_trip()
        elif opt == '8':
            view_all_trips()
        elif opt == '9':
            search_trip_by_driver()
        elif opt == '10':
            update_trip_amount()
        elif opt == '11':
            delete_trip()
        elif opt == '12':
            analytics()
        elif opt == '13':
            delete_all_trips()
        elif opt == '14':
            add_temp_driver()
        elif opt == '15':
            view_temp_drivers()
        elif opt == '16':
            print("Exiting Transportation Portal. Thank you!")
            break
        else:
            print("Invalid choice!")
if __name__ == "__main__":
    main_menu()
