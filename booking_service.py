
from database import get_connection
from datetime import date
import secrets
import string


def generate_pnr():
    """Generate a unique 10-digit PNR."""
    return "".join(secrets.choice(string.digits) for _ in range(10))


def book_ticket():
    print("\n========== TICKET BOOKING ==========")

    name = input("Passenger name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    try:
        age = int(input("Passenger age: "))
        if not 1 <= age <= 120:
            print("Please enter an age between 1 and 120.")
            return
    except ValueError:
        print("Age must be a number.")
        return

    gender = input("Gender (optional): ").strip() or None
    phone = input("Phone number (optional): ").strip() or None
    train_no = input("Train number: ").strip()
    journey_text = input("Journey date (YYYY-MM-DD): ").strip()

    try:
        journey_date = date.fromisoformat(journey_text)
        if journey_date < date.today():
            print("Journey date cannot be in the past.")
            return
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    connection = get_connection()

    if connection is None:
        return

    cursor = None

    try:
        connection.start_transaction()
        cursor = connection.cursor()

        # Lock the selected train row during the seat check.
        cursor.execute(
            """
            SELECT train_id, fare, total_seats
            FROM trains
            WHERE train_no = %s AND is_active = TRUE
            FOR UPDATE
            """,
            (train_no,)
        )
        train = cursor.fetchone()

        if train is None:
            connection.rollback()
            print("Train not found or inactive.")
            return

        train_id, fare, total_seats = train

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM bookings
            WHERE train_id = %s
              AND journey_date = %s
              AND status = 'CONFIRMED'
            """,
            (train_id, journey_date)
        )
        booked_seats = cursor.fetchone()[0]

        if booked_seats >= total_seats:
            connection.rollback()
            print("Sorry, this train is fully booked for that date.")
            return

        cursor.execute(
            """
            INSERT INTO passengers (name, age, gender, phone)
            VALUES (%s, %s, %s, %s)
            """,
            (name, age, gender, phone)
        )
        passenger_id = cursor.lastrowid

        # Retry if a rare PNR collision occurs.
        for _ in range(5):
            pnr = generate_pnr()
            try:
                cursor.execute(
                    """
                    INSERT INTO bookings
                    (pnr, passenger_id, train_id, journey_date, total_fare)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (pnr, passenger_id, train_id, journey_date, fare)
                )
                break
            except Exception as error:
                if getattr(error, "errno", None) != 1062:
                    raise
        else:
            raise RuntimeError("Could not generate a unique PNR.")

        connection.commit()

        print("\nTicket booked successfully!")
        print(f"PNR: {pnr}")
        print(f"Passenger: {name}")
        print(f"Train number: {train_no}")
        print(f"Journey date: {journey_date}")
        print(f"Fare: Rs. {fare}")

    except Exception as error:
        connection.rollback()
        print("Booking failed:", error)

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


if __name__ == "__main__":
    book_ticket()
