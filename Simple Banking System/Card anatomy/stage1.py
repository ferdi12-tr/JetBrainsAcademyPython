import sys
import random


class BankingSys:
    identify_n = "400000"  # is default value of our card number system
    numbers = "0123456789"
    card_list = {}  # hold the every user card list that contain card number and pin.

    def __init__(self):
        self.balance = 0  # when initialize new user, they balance must be zero

    def create_account(self):
        while True:
            can = ""  # customer account number
            pin = ""
            for i in range(0, 10):  # loop for creating 10 digit customer account number
                can += random.choice(self.numbers)

            for j in range(0, 4):  # loop for creating 4 digit pin number
                pin += random.choice(self.numbers)

            card_number = int(self.identify_n + can)
            pin = int(pin)

            if card_number in self.card_list.keys():
                continue
            else:
                self.card_list.update({card_number: pin})
                break

        print("Your card has been created")
        print(f"Your card number:\n{card_number}\nYour card PIN:\n{pin}")

    def log_account(self):
        print("Enter your card number:")
        log_card_n = int(input())
        print("Enter your PIN:")
        log_pin = int(input())
        if not (log_card_n in self.card_list.keys()) or not (log_pin in self.card_list.values()):
            print("Wrong card number or PIN!")
        else:
            print("You have successfully logged in!")
            while True:
                print("""1. Balance\n2. Log out\n0. Exit""")
                slc = int(input())
                if slc is 1:
                    print(f"Balance: {self.balance}")
                    continue
                elif slc is 2:
                    print("You have successfully logged out!")
                    break
                else:
                    sys.exit()


if __name__ == "__main__":
    user = BankingSys()
    while True:
        print("""1. Create an account\n2. Log into account\n0. Exit""")
        cvp = int(input())
        if cvp == 1:
            user.create_account()
            continue
        elif cvp == 2:
            user.log_account()
            continue
        else:
            print("Bye!")
            sys.exit()
