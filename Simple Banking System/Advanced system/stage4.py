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
        # sql0 = "DROP TABLE IF EXISTS card"
        sql = "CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, " \
              "number TEXT, pin TEXT, balance INTEGER DEFAULT 0);"
        # self.cur.execute(sql0)
        self.cur.execute(sql)
        self.conn.commit()

    def add_card(self, card_num, pin):

        sql = "INSERT INTO card (number, pin, balance) VALUES (?, ?, ?);"
        self.cur.execute(sql, (str(card_num), str(pin), self.balance))
        self.conn.commit()

    def select_card(self, temp_cn, temp_pin=None):  # temp_cn: temporary card number for card number selections
        sql = "SELECT * FROM  card WHERE number IN ('{}') AND pin IN ('{}')".format(str(temp_cn), str(temp_pin))
        sql2 = "SELECT * FROM card WHERE number IN ('{}')".format(str(temp_cn))
        if temp_pin is None:  # this is for account for transfer money, we mustn't ask pin
            self.cur.execute(sql2)
            self.conn.commit()
            raw = self.cur.fetchone()
        else:
            self.cur.execute(sql)
            self.conn.commit()
            raw = self.cur.fetchone()
        return raw

    def close_db(self):
        self.conn.close()

    @staticmethod
    def luhn_algorithm(cn):
        summa = 0  # sum elements of card number
        cn1 = []
        cn3 = list(str(cn))  # to change the self.card_number(arg cn) in cn1 list
        _ = cn3.pop()  # get rid of the last element of card number
        for count, item in enumerate(cn3):  # if element index is odd, then multiply element by 2 otherwise left same.
            if count % 2 == 1:
                cn1.append(int(item))
            else:
                cn1.append(2 * int(item))

        cn2 = [y - 9 if y > 9 else y for y in cn1]  # subtract 9 from numbers over 9

        for x in cn2:
            summa += x
        last_digit = (summa * 9) % 10  # calculate what the last digit must be (a.k.a checksum)

        return int(str(cn[:-1]) + str(last_digit))  # return the valid card number

    def create_account(self):
        while True:
            can = ""  # customer account number
            pinn = ""  # initial pin number
            for i in range(0, 10):  # loop for creating 10 digit customer account number
                can += random.choice(self.numbers)

            for j in range(0, 4):  # loop for creating 4 digit pin number
                pinn += random.choice(self.numbers)

            self.card_number = self.identify_n + can  # card number that have 16 digit element
            self.card_number = self.luhn_algorithm(self.card_number)  # response of luhn_algorithm method
            self.pin = int(pinn)

            if self.select_card(self.card_number, self.pin):  # select_card return empty list
                continue
            else:
                self.card_list.update({self.card_number: self.pin})
                print("Your card has been created")
                print(f"Your card number:\n{self.card_number}\nYour card PIN:\n{self.pin}")
                self.add_card(self.card_number, self.pin)  # adding card to database
                break

    def log_account(self):
        print("Enter your card number:")
        log_card_n = int(input())
        print("Enter your PIN:")
        log_pin = int(input())
        raw = self.select_card(log_card_n, log_pin)
        if not raw:
            print("Wrong card number or PIN!")
        else:
            print("You have successfully logged in!")

            while True:
                raw = self.select_card(log_card_n, log_pin)  # after every update, get updated card info
                print("""1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit""")
                slc = int(input()) # for select option
                if slc is 1:
                    print(f"Balance: {raw[3]}")
                    continue
                elif slc is 2:
                    print("Enter income:")
                    income = int(input())
                    sql = "UPDATE card SET Balance = {} WHERE number = {}".format((raw[3] + income), raw[1])
                    self.cur.execute(sql)
                    self.conn.commit()
                    print("Income was added!")
                    continue
                elif slc is 3:
                    print("Transfer\nEnter card number:")
                    trnsf = input()
                    if int(trnsf) != self.luhn_algorithm(trnsf):
                        print("Probably you made a mistake in the card number. Please try again!")
                        continue
                    elif not self.select_card(trnsf):
                        print("Such a card does not exist.")
                        continue
                    else:  # if transfer card number is true
                        print("Enter how much money you want to transfer:")
                        tr_money = int(input())  # the amount of money that we want to transfer
                        if tr_money > raw[3]:
                            print("Not enough money!")
                            continue
                        else:
                            tr_raw = self.select_card(trnsf)
                            # the account we will send money from
                            sql1 = "UPDATE card SET Balance = {} WHERE number = {}".format((raw[3] - tr_money), log_card_n)
                            # the account that must receive money
                            sql2 = "UPDATE card SET Balance = {} WHERE number = {}".format(tr_raw[3] + tr_money, trnsf)
                            self.cur.execute(sql1)
                            self.conn.commit()
                            self.cur.execute(sql2)
                            self.conn.commit()
                            print("Success!")
                            continue
                elif slc is 4:
                    sql = "DELETE FROM card WHERE number = {}".format(log_card_n)
                    self.cur.execute(sql)
                    self.conn.commit()
                    print("The account has been closed!")
                    break
                elif slc is 5:
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
