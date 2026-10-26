
from database import get_connection


def cancel_ticket():
    print("\n========== TICKET CANCELLATION ==========")

    pnr = input("Enter the 10-digit PNR: ").strip()

    if not pnr.isdigit() or len(pnr) != 10:
        print("Invalid PNR. Please enter a 10-digit number.")
        return

    connection = get_connection()

    if connection is None:
        return

    cursor = None

    try:
        connection.start_transaction()
        cursor = connection.cursor()

        # Lock the booking while cancellation is processed.
        cursor.execute(
            """
            SELECT b.status, p.name, t.train_name,
                   b.journey_date, b.total_fare
            FROM bookings AS b
            JOIN passengers AS p
                ON b.passenger_id = p.passenger_id
            JOIN trains AS t
                ON b.train_id = t.train_id
            WHERE b.pnr = %s
            FOR UPDATE
            """,
            (pnr,)
        )

        ticket = cursor.fetchone()

        if ticket is None:
            connection.rollback()
            print("No ticket found for this PNR.")
            return

        status, name, train_name, journey_date, fare = ticket

        print("\nTicket Details")
        print("-" * 35)
        print(f"Passenger: {name}")
        print(f"Train: {train_name}")
        print(f"Journey date: {journey_date}")
        print(f"Fare: Rs. {fare}")
        print(f"Status: {status}")

        if status == "CANCELLED":
            connection.rollback()
            print("\nThis ticket has already been cancelled.")
            return

        confirm = input(
            "\nAre you sure you want to cancel? (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            connection.rollback()
            print("Cancellation aborted.")
            return

        cursor.execute(
            """
            UPDATE bookings
            SET status = 'CANCELLED'
            WHERE pnr = %s AND status = 'CONFIRMED'
            """,
            (pnr,)
        )

        if cursor.rowcount != 1:
            connection.rollback()
            print("Could not cancel the ticket. Please try again.")
            return

        connection.commit()

        print("\nTicket cancelled successfully!")
        print("The booking record has been preserved.")

    except Exception as error:
        connection.rollback()
        print("Cancellation failed:", error)

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


if __name__ == "__main__":
    cancel_ticket()
