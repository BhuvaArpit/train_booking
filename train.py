import random

class User:
    def _init_(self, username, password):
        self.username = username
        self.password = password

class Ticket:
    def _init_(self, train_number, passenger_name, source, destination, quantity, fare):
        self.train_number = train_number
        self.passenger_name = passenger_name
        self.source = source
        self.destination = destination
        self.quantity = quantity
        self.fare = fare

class PaymentGateway:
    def process_payment(self, card_number, cvv, amount):
        # Simulating payment processing
        if self.validate_card_number(card_number) and self.validate_cvv(cvv):
            print(f"Processing payment of amount {amount}...")
            if random.random() < 0.9:  # 90% success rate simulation
                print("Payment successful.")
                return True
            else:
                print("Payment failed.")
                return False
        else:
            print("Invalid card number or CVV.")
            return False

    def validate_card_number(self, card_number):
        return len(card_number) == 12 and card_number.isdigit()

    def validate_cvv(self, cvv):
        return len(cvv) == 3 and cvv.isdigit()

class Train:
    def _init_(self, train_number, source, destination, fare_per_ticket, total_seats):
        self.train_number = train_number
        self.source = source
        self.destination = destination
        self.fare_per_ticket = fare_per_ticket
        self.total_seats = total_seats
        self.available_seats = total_seats

class IRCTC:
    def _init_(self):
        self.users = []
        self.tickets = []
        self.trains = [
            Train("12345", "Delhi", "Kolkata", 100, 50),
            Train("54321", "Mumbai", "Hyderabad", 150, 60),
            Train("98765", "Chennai", "Bangalore", 200, 70)
        ]
        self.payment_gateway = PaymentGateway()
        self.logged_in_user = None

    def register_user(self, username, password):
        self.users.append(User(username, password))
        print("User registered successfully.")

    def authenticate_user(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None

    def book_ticket(self):
        print("Available Trains:")
        for train in self.trains:
            print(f"Train Number: {train.train_number}, Source: {train.source}, Destination: {train.destination}, Fare: {train.fare_per_ticket}")

        train_number = input("Enter train number: ")
        train = next((train for train in self.trains if train.train_number == train_number), None)
        if train:
            quantity = int(input("Enter quantity: "))
            if train.available_seats >= quantity:
                fare = train.fare_per_ticket
                train.available_seats -= quantity
                total_fare = fare * quantity
                passenger_name = input("Enter passenger name: ")

                # Payment
                card_number = input("Enter 12-digit card number: ")
                cvv = input("Enter 3-digit CVV: ")

                if self.payment_gateway.process_payment(card_number, cvv, total_fare):
                    self.tickets.append(Ticket(train_number, passenger_name, train.source, train.destination, quantity, total_fare))
                    print("Ticket booked successfully.")
                    print("Your booked ticket details:")
                    print(f"From: {train.source} To: {train.destination}")
                    print(f"Train Number: {train_number}")
                    print(f"Passenger Name: {passenger_name}")
                    print(f"Quantity: {quantity}")
                    print(f"Total Fare: {total_fare}")
                else:
                    print("Ticket booking failed. Payment was not successful.")
                    train.available_seats += quantity  # Rollback seats
            else:
                print("Seats not available.")
        else:
            print("Train not found.")

    def check_seat_availability(self):
        print("Available Seats for All Trains:")
        for train in self.trains:
            print(f"Train Number: {train.train_number}, Available Seats: {train.available_seats}")

    def check_reservation_status(self, train_number):
        train = next((train for train in self.trains if train.train_number == train_number), None)
        if train and train.available_seats == 0:
            print("Reservation not available.")
        else:
            print("Reservation status checked successfully.")

    def cancel_ticket(self, ticket):
        # Logic to cancel ticket
        if ticket in self.tickets:
            self.tickets.remove(ticket)
            print("Ticket cancelled successfully.")
            train = next((train for train in self.trains if train.train_number == ticket.train_number), None)
            if train:
                train.available_seats += ticket.quantity
        else:
            print("Ticket not found.")

    def display_menu(self):
        print("\nWelcome to IRCTC")
        print("1. Book Ticket")
        print("2. Check Seat Availability")
        print("3. Check Reservation Status")
        print("4. Cancel Ticket")
        print("5. Show Booked Tickets")
        print("6. Logout")

    def run(self):
        while True:
            if self.logged_in_user is None:
                print("\n1. Register")
                print("2. Login")
                print("3. Exit")
                choice = input("Enter your choice: ")

                if choice == "1":
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    self.register_user(username, password)
                elif choice == "2":
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    user = self.authenticate_user(username, password)
                    if user:
                        print("Login successful.")
                        self.logged_in_user = user
                    else:
                        print("Invalid credentials.")
                elif choice == "3":
                    print("Thank you for using IRCTC. Goodbye!")
                    break
                else:
                    print("Invalid choice. Please enter a valid option.")
            else:
                self.display_menu()
                choice = input("Enter your choice: ")

                if choice == "1":
                    self.book_ticket()
                elif choice == "2":
                    self.check_seat_availability()
                elif choice == "3":
                    train_number = input("Enter train number: ")
                    self.check_reservation_status(train_number)
                elif choice == "4":
                    if not self.tickets:
                        print("No tickets booked.")
                        continue
                    print("Your booked tickets:")
                    for i, ticket in enumerate(self.tickets, 1):
                        print(f"{i}. From: {ticket.source} To: {ticket.destination}, "
                              f"Train: {ticket.train_number}, Passenger: {ticket.passenger_name}, "
                              f"Quantity: {ticket.quantity}, Total Fare: {ticket.fare}")
                    ticket_index = int(input("Enter ticket number to cancel: ")) - 1
                    if 0 <= ticket_index < len(self.tickets):
                        self.cancel_ticket(self.tickets[ticket_index])
                    else:
                        print("Invalid ticket number.")
                elif choice == "5":
                    if not self.tickets:
                        print("No tickets booked.")
                    else:
                        print("Your booked tickets:")
                        for i, ticket in enumerate(self.tickets, 1):
                            print(f"{i}. From: {ticket.source} To: {ticket.destination}, "
                                  f"Train: {ticket.train_number}, Passenger: {ticket.passenger_name}, "
                                  f"Quantity: {ticket.quantity}, Total Fare: {ticket.fare}")
                elif choice == "6":
                    print("Logged out successfully.")
                    self.logged_in_user = None
                else:
                    print("Invalid choice. Please enter a valid option.")

# Sample usage
irctc = IRCTC()
irctc.run()