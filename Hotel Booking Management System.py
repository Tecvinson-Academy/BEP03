import re
from datetime import datetime
 
class Hotel:
    def __init__(self):
        self.available_rooms = {
            'supreme': [501, 502, 503, 504, 505],
            'delux': [601, 602, 603, 604, 605],
            'luxury': [701, 702, 703, 704, 705],
            'twin_bedroom': [801, 802, 803, 804, 805],
            'executive': [901, 902, 903, 904, 905]
        }
        self.reservations = {}
        self.room_rate = {
            'supreme': 30000,
            'delux': 25000,
            'luxury': 50000,
            'twin_bedroom': 20000,
            'executive': 100000
        }
 
    def check_availability(self):
        available_rooms_count = {room_type: len(rooms) for room_type, rooms in self.available_rooms.items()}
        return available_rooms_count
 
    def is_valid_email(self, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None
 
    def get_credit_card_details(self):
        while True:
            card_number = input("Enter your credit card number (16 digits): ")
            if len(card_number) == 16 and card_number.isdigit():
                break
            else:
                print("Invalid card number. Please enter a 16-digit number.")
        expiry_date = input("Enter expiry date (MM/YY): ")
        cvv = input("Enter CVV (3 digits): ")
 
    def make_reservation(self):
        try:
            guest_name = input("Enter guest name: ")
            phone_number = input("Enter phone number: ")
            email_address = input("Enter email address: ")
 
            if not self.is_valid_email(email_address):
                return "Invalid email address format."
 
            room_selections = {}
            while True:
                room_type = input("Enter room type (supreme, delux, luxury, twin_bedroom, executive): ").lower()
                number_of_rooms = int(input("Enter number of rooms for this type: "))
                if room_type not in self.available_rooms:
                    return "Invalid room type."
                if len(self.available_rooms[room_type]) < number_of_rooms:
                    return f"Not enough rooms available in the {room_type} category."
                room_selections[room_type] = number_of_rooms
                more_rooms = input("Would you like to add another room type? (yes/no): ").lower()
                if more_rooms != 'yes':
                    break
 
            num_adults = int(input("Enter the number of adults: "))
            num_kids = int(input("Enter the number of kids: "))
 
            check_in_date_str = input("Enter check-in date (YYYY-MM-DD): ")
            check_out_date_str = input("Enter check-out date (YYYY-MM-DD): ")
 
            try:
                check_in_date = datetime.strptime(check_in_date_str, "%Y-%m-%d")
                check_out_date = datetime.strptime(check_out_date_str, "%Y-%m-%d")
            except ValueError:
                return "Invalid date format. Please use YYYY-MM-DD."
 
            if check_in_date >= check_out_date:
                return "Check-out date must be after check-in date."
            if check_in_date < datetime.now():
                return "Check-in date cannot be in the past."
 
            duration = (check_out_date - check_in_date).days
            total_amount_due = sum(self.room_rate[room_type] * num_rooms * duration for room_type, num_rooms in room_selections.items())
            print(f"Amount due is: ₦{total_amount_due:.2f}")
 
            payment_method = input("Enter payment method (credit card, cash): ").lower()
            if payment_method == "credit card":
                self.get_credit_card_details()
 
            payment_amount = float(input("Enter payment amount: ₦"))
            if payment_amount < total_amount_due:
                return "Insufficient payment."
            elif payment_method == "cash" and payment_amount > total_amount_due:
                excess_amount = payment_amount - total_amount_due
                print(f"Excess amount: ₦{excess_amount:.2f}. Returning excess.")
            else:
                print('Enter valid option')
 
 
            for room_type, number_of_rooms in room_selections.items():
                reserved_rooms = self.available_rooms[room_type][:number_of_rooms]
                self.available_rooms[room_type] = self.available_rooms[room_type][number_of_rooms:]
                self.reservations.setdefault(guest_name, []).append({
                    'room_type': room_type,
                    'rooms': reserved_rooms,
                    'number_of_rooms': number_of_rooms,
                    'phone_number': phone_number,
                    'email_address': email_address,
                    'check_in_date': check_in_date,
                    'check_out_date': check_out_date,
                    'duration': duration,
                    'num_adults': num_adults,
                    'num_kids': num_kids,
                    'payment_method': payment_method,
                    'payment_amount': payment_amount,
                    'total_amount_due': total_amount_due
                })
 
            return self.show_reservation_details(guest_name)
 
        except Exception as e:
            return f"An error occurred: {e}"
 
    def show_reservation_details(self, guest_name):
        details = self.reservations.get(guest_name)
        if not details:
            return "No reservation found under this name."
        reservation_details = f"Reservation details for {guest_name}:\n"
        for detail in details:
            reservation_details += (
                f"Room Type: {detail['room_type'].capitalize()}\n"
                f"Rooms Reserved: {', '.join(map(str, detail['rooms']))}\n"
                f"Phone: {detail['phone_number']}\n"
                f"Email: {detail['email_address']}\n"
                f"Adults: {detail['num_adults']}, Kids: {detail['num_kids']}\n"
                f"Check-in Date: {detail['check_in_date'].strftime('%Y-%m-%d')}\n"
                f"Check-out Date: {detail['check_out_date'].strftime('%Y-%m-%d')}\n"
                f"Duration: {detail['duration']} nights\n"
                f"Total Amount Due: ₦{detail['total_amount_due']:.2f}\n"
                f"Payment Method: {detail['payment_method'].capitalize()}\n"
                f"Payment Received: ₦{detail['payment_amount']:.2f}\n"
                "-------------------------------------\n"
            )
        return reservation_details
 
    def cancel_reservation(self):
        guest_name = input("Enter guest name: ")
        if guest_name not in self.reservations:
            return "No reservation found under this name."
 
        room_type = input("Enter the room type to cancel (supreme, delux, luxury, twin_bedroom, executive): ").lower()
        guest_reservations = self.reservations.get(guest_name)
        for reservation in guest_reservations:
            if reservation['room_type'] == room_type:
                reserved_rooms = reservation['rooms']
                payment_amount = reservation['payment_amount']
                refund_amount = payment_amount
 
                guest_reservations.remove(reservation)
                self.available_rooms[room_type] += reserved_rooms
 
                if not guest_reservations:
                    del self.reservations[guest_name]
 
                return (f"Reservation for {guest_name} in {room_type.capitalize()} has been canceled.\n"
                        f"Total amount refunded: ₦{refund_amount:.2f}")
        return f"No reservation found under {room_type} for {guest_name}."
 
    def show_reservations(self):
        if not self.reservations:
            return "No reservations at the moment."
        return '\n'.join([
            f"{guest_name}: {len(details)} types of rooms reserved.\n"
            for guest_name, details in self.reservations.items()
        ])
 
def main():
    hotel = Hotel()
 
    while True:
        print("\n--- Hotel Reservation System ---")
        print("1. Check availability")
        print("2. Make a reservation")
        print("3. Cancel a reservation")
        print("4. Show all reservations")
        print("5. Exit")
 
        choice = input("Enter your choice: ")
 
        if choice == '1':
            print("Available rooms:")
            availability = hotel.check_availability()
            for room_type, count in availability.items():
                print(f"{room_type.capitalize()}: {count} rooms available")
        elif choice == '2':
            print(hotel.make_reservation())
        elif choice == '3':
            print(hotel.cancel_reservation())
        elif choice == '4':
            print(hotel.show_reservations())
        elif choice == '5':
            break
        else:
            print("Invalid choice, please select a valid option.")
 
if __name__ == "__main__":
    main()