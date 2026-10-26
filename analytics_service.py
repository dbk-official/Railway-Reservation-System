
from database import get_connection


def show_analytics():
    print("\n========== RAILWAY ANALYTICS ==========")

    connection = get_connection()

    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()

        # 1. Booking statistics
        cursor.execute("""
            SELECT
                COUNT(*) AS total_bookings,
                COALESCE(SUM(status = 'CONFIRMED'), 0)
                    AS confirmed_bookings,
                COALESCE(SUM(status = 'CANCELLED'), 0)
                    AS cancelled_bookings
            FROM bookings
        """)

        stats = cursor.fetchone()

        print("\n--- Booking Statistics ---")
        print(f"Total bookings     : {stats[0]}")
        print(f"Confirmed bookings : {stats[1]}")
        print(f"Cancelled bookings : {stats[2]}")

        # 2. Revenue from confirmed bookings
        cursor.execute("""
            SELECT COALESCE(SUM(total_fare), 0)
            FROM bookings
            WHERE status = 'CONFIRMED'
        """)

        revenue = cursor.fetchone()[0]

        print("\n--- Revenue ---")
        print(f"Confirmed booking value: Rs. {revenue:.2f}")

        # 3. Most popular routes
        cursor.execute("""
            SELECT
                t.source,
                t.destination,
                COUNT(*) AS booking_count
            FROM bookings AS b
            JOIN trains AS t ON b.train_id = t.train_id
            WHERE b.status = 'CONFIRMED'
            GROUP BY t.source, t.destination
            ORDER BY booking_count DESC, t.source
            LIMIT 5
        """)

        routes = cursor.fetchall()

        print("\n--- Popular Routes ---")

        if routes:
            for route in routes:
                print(
                    f"{route[0]} -> {route[1]}: "
                    f"{route[2]} confirmed booking(s)"
                )
        else:
            print("No confirmed bookings yet.")

        # 4. Complaint statistics
        cursor.execute("""
            SELECT
                COUNT(*) AS total_complaints,
                COALESCE(SUM(status = 'OPEN'), 0) AS open_complaints,
                COALESCE(SUM(status = 'IN_PROGRESS'), 0)
                    AS in_progress,
                COALESCE(SUM(status = 'RESOLVED'), 0)
                    AS resolved_complaints
            FROM complaints
        """)

        complaint_stats = cursor.fetchone()

        print("\n--- Complaint Statistics ---")
        print(f"Total complaints       : {complaint_stats[0]}")
        print(f"Open complaints        : {complaint_stats[1]}")
        print(f"In-progress complaints : {complaint_stats[2]}")
        print(f"Resolved complaints    : {complaint_stats[3]}")

        # 5. Booking summary by train
        cursor.execute("""
            SELECT
                t.train_no,
                t.train_name,
                COUNT(b.booking_id) AS confirmed_bookings
            FROM trains AS t
            LEFT JOIN bookings AS b
                ON t.train_id = b.train_id
                AND b.status = 'CONFIRMED'
            GROUP BY t.train_id, t.train_no, t.train_name
            ORDER BY confirmed_bookings DESC, t.train_no
        """)

        train_stats = cursor.fetchall()

        print("\n--- Bookings by Train ---")

        for train in train_stats:
            print(
                f"{train[0]} | {train[1]} | "
                f"{train[2]} confirmed booking(s)"
            )

        print("\n======================================")

    except Exception as error:
        print("Could not generate analytics:", error)

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


if __name__ == "__main__":
    show_analytics()