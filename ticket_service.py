
from database import get_connection


def view_ticket():
    print("\n========== VIEW TICKET ==========")

    pnr = input("Enter your 10-digit PNR: ").strip()

    if not pnr.isdigit() or len(pnr) != 10:
        print("Invalid PNR. Please enter a 10-digit number.")
        return

    connection = get_connection()

    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                b.pnr,
                p.name,
                p.age,
                p.gender,
                t.train_no,
                t.train_name,
                t.source,
                t.destination,
                t.departure_time,
                t.arrival_time,
                b.journey_date,
                b.total_fare,
                b.status,
                b.booking_time
            FROM bookings AS b
            JOIN passengers AS p
                ON b.passenger_id = p.passenger_id
            JOIN trains AS t
                ON b.train_id = t.train_id
            WHERE b.pnr = %s
        """

        cursor.execute(query, (pnr,))
        ticket = cursor.fetchone()

        if ticket is None:
            print("No booking found for this PNR.")
            return

        print("\n" + "=" * 45)
        print("           RAILWAY E-TICKET")
        print("=" * 45)
        print(f"PNR             : {ticket[0]}")
        print(f"Passenger       : {ticket[1]}")
        print(f"Age             : {ticket[2]}")
        print(f"Gender          : {ticket[3] or 'Not provided'}")
        print(f"Train Number    : {ticket[4]}")
        print(f"Train Name      : {ticket[5]}")
        print(f"From            : {ticket[6]}")
        print(f"To              : {ticket[7]}")
        print(f"Departure       : {ticket[8]}")
        print(f"Arrival         : {ticket[9]}")
        print(f"Journey Date    : {ticket[10]}")
        print(f"Fare            : Rs. {ticket[11]}")
        print(f"Status          : {ticket[12]}")
        print(f"Booking Time    : {ticket[13]}")
        print("=" * 45)

    except Exception as error:
        print("Could not retrieve ticket:", error)

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


if __name__ == "__main__":
    view_ticket()