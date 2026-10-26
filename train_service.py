
from database import get_connection


def search_trains():
    print("\n========== TRAIN SEARCH ==========")

    source = input("Enter source station: ").strip()
    destination = input("Enter destination station: ").strip()

    if not source or not destination:
        print("Source and destination cannot be empty.")
        return

    connection = get_connection()

    if connection is None:
        return

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            SELECT train_no, train_name, source, destination,
                   departure_time, arrival_time, fare, total_seats
            FROM trains
            WHERE LOWER(source) = LOWER(%s)
              AND LOWER(destination) = LOWER(%s)
              AND is_active = TRUE
        """

        cursor.execute(query, (source, destination))
        trains = cursor.fetchall()

        if not trains:
            print("\nNo trains found for this route.")
            return

        print(f"\nTrains from {source} to {destination}")
        print("-" * 95)
        print(
            f"{'Train No.':<11}{'Train Name':<22}"
            f"{'Departure':<13}{'Arrival':<13}"
            f"{'Fare (Rs.)':<13}{'Seats':<8}"
        )
        print("-" * 95)

        for train in trains:
            print(
                f"{train[0]:<11}{train[1]:<22}"
                f"{str(train[4]):<13}{str(train[5]):<13}"
                f"{float(train[6]):<13.2f}{train[7]:<8}"
            )

        print("-" * 95)

    except Exception as error:
        print("Error searching for trains:", error)

    finally:
        if cursor is not None:
            cursor.close()
        connection.close()


if __name__ == "__main__":
    search_trains()