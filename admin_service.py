
from database import get_connection
from getpass import getpass

ADMIN_USERNAME = "darsh.railway"
ADMIN_PASSWORD = "Railway@123"


def admin_login():
    print("\n========== ADMIN LOGIN ==========")

    username = input("Username: ").strip()
    password = getpass("Password: ")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("\nLogin successful!")
        admin_menu()
    else:
        print("\nInvalid username or password.")


def view_all_trains():
    connection = get_connection()
    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT train_no, train_name, source, destination,
                   departure_time, arrival_time, fare,
                   total_seats, is_active
            FROM trains
            ORDER BY train_no
        """)

        trains = cursor.fetchall()

        print("\n========== ALL TRAINS ==========")

        for train in trains:
            print("-" * 45)
            print(f"Train number : {train[0]}")
            print(f"Train name   : {train[1]}")
            print(f"Route        : {train[2]} -> {train[3]}")
            print(f"Departure    : {train[4]}")
            print(f"Arrival      : {train[5]}")
            print(f"Fare         : Rs. {train[6]}")
            print(f"Total seats  : {train[7]}")
            print(f"Active       : {'Yes' if train[8] else 'No'}")

    except Exception as error:
        print("Could not retrieve trains:", error)

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def add_train():
    print("\n========== ADD TRAIN ==========")

    train_no = input("Train number: ").strip()
    train_name = input("Train name: ").strip()
    source = input("Source station: ").strip()
    destination = input("Destination station: ").strip()
    departure = input("Departure time (HH:MM:SS): ").strip()
    arrival = input("Arrival time (HH:MM:SS): ").strip()

    if not all([
        train_no, train_name, source, destination,
        departure, arrival
    ]):
        print("All fields are required.")
        return

    if source.casefold() == destination.casefold():
        print("Source and destination must differ.")
        return

    try:
        fare = float(input("Fare: Rs. "))
        seats = int(input("Total seats: "))

        if fare < 0 or seats <= 0:
            print("Fare cannot be negative and seats must be positive.")
            return

    except ValueError:
        print("Enter a valid fare and seat count.")
        return

    connection = get_connection()
    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO trains
                (train_no, train_name, source, destination,
                 departure_time, arrival_time, fare, total_seats)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            train_no, train_name, source, destination,
            departure, arrival, fare, seats
        ))

        connection.commit()
        print("Train added successfully!")

    except Exception as error:
        connection.rollback()
        print("Could not add train:", error)

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def deactivate_train():
    train_no = input("Enter train number to deactivate: ").strip()

    connection = get_connection()
    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE trains
            SET is_active = FALSE
            WHERE train_no = %s AND is_active = TRUE
        """, (train_no,))

        if cursor.rowcount == 1:
            connection.commit()
            print("Train deactivated successfully.")
        else:
            connection.rollback()
            print("Train not found or already inactive.")

    except Exception as error:
        connection.rollback()
        print("Could not deactivate train:", error)

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def view_complaints():
    connection = get_connection()
    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT c.complaint_id, p.name, c.category,
                   c.description, c.status, t.train_no
            FROM complaints AS c
            JOIN passengers AS p
                ON c.passenger_id = p.passenger_id
            LEFT JOIN trains AS t
                ON c.train_id = t.train_id
            ORDER BY c.created_at DESC
        """)

        complaints = cursor.fetchall()

        print("\n========== COMPLAINTS ==========")

        if not complaints:
            print("No complaints found.")

        for item in complaints:
            print("-" * 45)
            print(f"Complaint ID : {item[0]}")
            print(f"Passenger    : {item[1]}")
            print(f"Category     : {item[2]}")
            print(f"Description  : {item[3]}")
            print(f"Status       : {item[4]}")
            print(f"Train number : {item[5] or 'Not specified'}")

    except Exception as error:
        print("Could not retrieve complaints:", error)

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def update_complaint_status():
    try:
        complaint_id = int(input("Complaint ID: "))
        if complaint_id <= 0:
            print("Complaint ID must be positive.")
            return
    except ValueError:
        print("Enter a valid complaint ID.")
        return

    status = input(
        "New status (OPEN / IN_PROGRESS / RESOLVED): "
    ).strip().upper()

    allowed_statuses = {"OPEN", "IN_PROGRESS", "RESOLVED"}

    if status not in allowed_statuses:
        print("Invalid status.")
        return

    connection = get_connection()
    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE complaints
            SET status = %s
            WHERE complaint_id = %s
        """, (status, complaint_id))

        if cursor.rowcount > 0:
            connection.commit()
            print("Complaint status updated successfully.")
        else:
            connection.rollback()
            print("Complaint not found or status unchanged.")

    except Exception as error:
        connection.rollback()
        print("Could not update complaint:", error)

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def admin_menu():
    while True:
        print("\n========== ADMIN PANEL ==========")
        print("1. View all trains")
        print("2. Add train")
        print("3. Deactivate train")
        print("4. View complaints")
        print("5. Update complaint status")
        print("0. Logout")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_all_trains()
        elif choice == "2":
            add_train()
        elif choice == "3":
            deactivate_train()
        elif choice == "4":
            view_complaints()
        elif choice == "5":
            update_complaint_status()
        elif choice == "0":
            print("Logged out.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    admin_login()
