
from train_service import search_trains
from booking_service import book_ticket
from ticket_service import view_ticket
from cancellation_service import cancel_ticket
from complaint_service import register_complaint, track_complaint
from admin_service import admin_login
from analytics_service import show_analytics

def main():
    while True:
        print("\n" + "=" * 40)
        print("       RAILWAY RESERVATION SYSTEM")
        print("=" * 40)
        print("1. Search Trains")
        print("2. Book Ticket")
        print("3. View Ticket / PNR")
        print("4. Cancel Ticket")
        print("5. Register Complaint")
        print("6. Admin Panel")
        print("7. Reports and Analytics")
        print("0. Exit")
        print("=" * 40)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            search_trains()

        elif choice == "2":
            book_ticket()

        elif choice == "3":
            view_ticket()

        elif choice == "4":
            cancel_ticket()

        elif choice == "5":
            print("\n1. Register Complaint")
            print("2. Track Complaint")

            complaint_choice = input("Enter your choice: ").strip()

            if complaint_choice == "1":
                register_complaint()
            elif complaint_choice == "2":
                track_complaint()
            else:
                print("Invalid choice.")

        elif choice == "6":
            admin_login()

        elif choice == "7":
            show_analytics()

        elif choice == "0":
            print("\nThank you for using Railway Reservation System!")
            break

        else:
            print("\nInvalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
