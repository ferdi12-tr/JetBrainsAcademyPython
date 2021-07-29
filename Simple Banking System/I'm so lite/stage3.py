import sys
import random
import sqlite3


class BankingSys:
    identify_n = "400000"  # is default value of our card number system
    numbers = "0123456789"
    card_list = {}  # hold the card list for every user because we want unique card number
    total_card = -1  # the number of card that write to db

    def __init__(self):
        self.pin = 0  # initialize pin value
        self.balance = 0  # when initialize new user, they balance must be zero
        self.card_number = 0
        # connection to database
        self.conn = sqlite3.connect("card.s3db")
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        #sql0 = "DROP TABLE IF EXISTS card"
        sql = "CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, " \
              "number TEXT, pin TEXT, balance INTEGER DEFAULT 0);"
        #self.cur.execute(sql0)
        self.cur.execute(sql)
        self.conn.commit()

    def add_card(self):

        sql = "INSERT INTO card (number, pin, balance) VALUES (?, ?, ?);"
        self.cur.execute(sql, (str(self.card_number), str(self.pin), self.balance))
        self.conn.commit()

    def select_card(self, temp_cn, temp_pin):  # temp_cn: temporary card number for card number selections
        sql = "SELECT * FROM  card WHERE number IN ('{}') AND pin IN ('{}')".format(str(temp_cn), str(temp_pin))

        self.cur.execute(sql)
        self.conn.commit()
        raw = self.cur.fetchone()
        return raw

    def close_db(self):
        self.conn.close()

    def luhn_algorithm(self):
        summa = 0  # sum elements of card number
        cn1 = []
        cn = list(str(self.card_number))  # to change the self.card_number to cn list
        for count, item in enumerate(cn):  # if element index is odd, then multiply element by 2 otherwise left it same.
            if count % 2 == 1:
                cn1.append(int(item))
            else:
                cn1.append(2 * int(item))

        cn2 = [y - 9 if y > 9 else y for y in cn1]  # subtract 9 from numbers over 9

        for x in cn2:
            summa += x
        last_digit = (summa * 9) % 10  # calculate what the last digit must be (a.k.a checksum)

        return int(str(self.card_number) + str(last_digit))  # return the valid card number

    def create_account(self):
        while True:
            can = ""  # customer account number
            pinn = ""
            for i in range(0, 9):  # loop for creating 10 digit customer account number
                can += random.choice(self.numbers)

            for j in range(0, 4):  # loop for creating 4 digit pin number
                pinn += random.choice(self.numbers)

            self.card_number = self.identify_n + can  # card number without check sum digit
            self.card_number = self.luhn_algorithm()  # response of luhn_algorithm method
            self.pin = int(pinn)

            if self.select_card(self.card_number, self.pin):
                continue
            else:
                self.card_list.update({self.card_number: self.pin})
                print("Your card has been created")
                print(f"Your card number:\n{self.card_number}\nYour card PIN:\n{self.pin}")
                self.add_card()  # adding card to database
                break

    def log_account(self):
        print("Enter your card number:")
        log_card_n = int(input())
        print("Enter your PIN:")
        log_pin = int(input())
        raw = self.select_card(log_card_n, log_pin)
        print(raw)
        if not raw:
            print("Wrong card number or PIN!")
        else:
            print("You have successfully logged in!")
            while True:
                print("""1. Balance\n2. Log out\n0. Exit""")
                slc = int(input())
                if slc is 1:
                    print(f"Balance: {list(raw)[3]}")
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
            user.close_db()
            sys.exit()