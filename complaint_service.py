
from database import get_connection


def register_complaint():
    print("\n========== REGISTER COMPLAINT ==========")

    try:
        passenger_id = int(input("Enter your passenger ID: "))
        if passenger_id <= 0:
            print("Passenger ID must be positive.")
            return
    except ValueError:
        print("Please enter a valid passenger ID.")
        return

    train_no = input(
        "Enter train number (press Enter if station-related): "
    ).strip()

    category = input(
        "Category (Cleanliness/Water/Food/Staff/Other): "
    ).strip().title()

    description = input("Describe the issue: ").strip()

    if not category or not description:
        print("Category and description cannot be empty.")
        return

    connection = get_connection()

    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()

        # Verify that the passenger exists.
        cursor.execute(
            "SELECT passenger_id FROM passengers WHERE passenger_id = %s",
            (passenger_id,)
        )

        if cursor.fetchone() is None:
            print("Passenger not found. Please check the passenger ID.")
            return

        train_id = None

        if train_no:
            cursor.execute(
                "SELECT train_id FROM trains WHERE train_no = %s",
                (train_no,)
            )

            train = cursor.fetchone()

            if train is None:
                print("Train not found. Please check the train number.")
                return

            train_id = train[0]

        cursor.execute(
            """
            INSERT INTO complaints
                (passenger_id, train_id, category, description)
            VALUES (%s, %s, %s, %s)
            """,
            (passenger_id, train_id, category, description)
        )

        complaint_id = cursor.lastrowid
        connection.commit()

        print("\nComplaint registered successfully!")
        print(f"Complaint ID: {complaint_id}")
        print("Status: OPEN")

    except Exception as error:
        connection.rollback()
        print("Could not register complaint:", error)

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


def track_complaint():
    print("\n========== TRACK COMPLAINT ==========")

    try:
        complaint_id = int(input("Enter your complaint ID: "))
        if complaint_id <= 0:
            print("Complaint ID must be positive.")
            return
    except ValueError:
        print("Please enter a valid complaint ID.")
        return

    connection = get_connection()

    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT c.complaint_id, c.category, c.description,
                   c.status, c.created_at, t.train_name
            FROM complaints AS c
            LEFT JOIN trains AS t ON c.train_id = t.train_id
            WHERE c.complaint_id = %s
            """,
            (complaint_id,)
        )

        complaint = cursor.fetchone()

        if complaint is None:
            print("No complaint found with that ID.")
            return

        print("\nComplaint Details")
        print("-" * 40)
        print(f"Complaint ID: {complaint[0]}")
        print(f"Category: {complaint[1]}")
        print(f"Description: {complaint[2]}")
        print(f"Status: {complaint[3]}")
        print(f"Submitted: {complaint[4]}")
        print(f"Train: {complaint[5] or 'Not specified'}")

    except Exception as error:
        print("Could not retrieve complaint:", error)

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


if __name__ == "__main__":
    print("1. Register complaint")
    print("2. Track complaint")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        register_complaint()
    elif choice == "2":
        track_complaint()
    else:
        print("Invalid choice.")
