import sqlite3
from crud_oop import BaseCRUD
from contextlib import closing
from random import randint
#
#
# connection = sqlite3.connect("Transactions.db")
# cursor = connection.cursor()
#
# cursor.execute("""CREATE TABLE IF NOT EXISTS transfers(
#     id INTEGER NOT NULL PRIMARY KEY,
#     from_acc_id INTEGER NOT NULL,
#     to_acc_id INTEGER NOT NULL,
#     quantity INTEGER NOT NULL,
#     FOREIGN KEY (from_acc_id) REFERENCES users(id),
#     FOREIGN KEY (to_acc_id) REFERENCES users(id)
# );
# """)
# # cursor.execute("""
# # INSERT INTO transfers(from_acc_id,to_acc_id,quantity) VALUES(
# #     1,
# #     2,
# #     200
# # );
# # """)
#
# for i in cursor.execute("SELECT * FROM transfers;"):
#     print(i)
#
#
# connection.commit()
# cursor.close()
# connection.close()

# HOMEWORK  (small bank system)
pysql = BaseCRUD("Transactions.db", "users")
pysql_transfers = BaseCRUD("Transactions.db","transfers")

def new_user(name,balance):
    pysql.insert(name=name,balance=balance)
def deposit(user_id,quantity):
    conn= sqlite3.connect("Transactions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE id=?",(user_id,))
    current_balance = cursor.fetchone()[0]
    new_balance = current_balance + float(quantity)
    cursor.close()
    conn.close()
    pysql.update(id=user_id,id_column="id",balance=new_balance)

def get_all():
    with closing(sqlite3.connect("Transactions.db")) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
    for i in result:
        print(i)
def delete_user(user_id):
    with closing(sqlite3.connect("Transactions.db")) as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE id=?",(user_id,))
        connection.commit()
def transfer(from_user_id:int,to_user_id:int,amount:int):
    if amount < 0:
        print("Incorrect transfer amount!!!")
        return
    def current_balance(id):
        with closing(sqlite3.connect("Transactions.db")) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT balance FROM users WHERE id=?;",(id,))
            current_balance = cursor.fetchall()
        return current_balance
    pysql.update(id=from_user_id,id_column="id",balance=current_balance(from_user_id)[0][0]-float(amount))
    pysql.update(id=to_user_id,id_column="id",balance=current_balance(to_user_id)[0][0]+float(amount))
    pysql_transfers.insert(from_acc_id=from_user_id,to_acc_id=to_user_id,quantity=amount)
def tranfers_info():
    with closing(sqlite3.connect("Transactions.db")) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM transfers;")
        result = cursor.fetchall()
    for i in result:
        print(i)
def withdraw(user_id:int,amount:int):
    def current_balance(id):
        with closing(sqlite3.connect("Transactions.db")) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT balance FROM users WHERE id=?;",(id,))
            current_balance = cursor.fetchall()
        return current_balance
    pysql.update(user_id,id_column="id",balance=current_balance(user_id)[0][0]-amount)
def user_interface():
    print("Welcome to mini Payment system by A.Husniyor")
    while True:
        command = input("__Choose the command__\n...1 - add new user🙌\n...2 - deposit👇\n...3 - transfer💱\n...4 - withdraw💰\n...5 - delete user✖️\n...6 - all users infoℹ️\n...7 - transfers history⌚\n...0 - exit👌\n>>")
        if command == '1':
            name = input("Input new user's name: ")
            balance = input("Input new user's balance: ")
            new_user(name=name,balance=balance)
            print("New user is succesfully created✅")
        elif command == '2':
            userid = input("Input user's id: ")
            amount = input("Input deposit amount: ")
            deposit(user_id=userid,quantity=amount)
            print("Deposit was succesful✅")
        elif command == '3':
            from_user = int(input("Input sender's id: "))
            to_user = int(input("Input purchaser's id: "))
            amount = int(input("Input an amount of transfer: "))
            transfer(from_user_id=from_user,to_user_id=to_user,amount=amount)
            print("Transfer succes✅")
        elif command == '4':
            user_id = int(input("Input user id: "))
            amount = int(input("Input withdraw amount: "))
            withdraw(user_id=user_id,amount=amount)
            print(f'User {user_id} succesfully withdrawed {amount} dollars✅')
        elif command == '5':
            id = int(input("Input deletable id: "))
            delete_user(id)
            with closing(sqlite3.connect("Transactions.db")) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT name FROM users WHERE id=?;",(id,))
                username = cursor.fetchone()
            print(f'User {username} is succesfully deleted✅')
        elif command == '6':
            print("---Users info:")
            get_all()
        elif command=='7':
            print('---All transfers:')
        elif command =='0':
            print("Exiting from app...")
            break

# with closing(sqlite3.connect("Transactions.db")) as connection:
#     cursor = connection.cursor()
#     cursor.execute("UPDATE users SET name='Husniyor' WHERE id=3")
#     connection.commit()

if __name__ == '__main__':
    try:
        user_interface()
    except Exception:
        print("Xatolik!!",Exception)