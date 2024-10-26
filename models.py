import sqlite3

DATABASE = 'atm.db'

def db_init():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            balance REAL DEFAULT 0.0
        )
    ''')
    conn.commit()
    conn.close()

class Customer:
    def __init__(self, id, username, password, balance):
        self.id = id
        self.username = username
        self.password = password
        self.balance = balance
    
    @staticmethod
    def login(username, password):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM customers WHERE username=? AND password=?", (username, password))
        data = c.fetchone()
        conn.close()
        
        if data:
            return Customer(*data)
        return None
    
    @staticmethod
    def get_customer(username):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM customers WHERE username=?", (username,))
        data = c.fetchone()
        conn.close()
        
        if data:
            return Customer(*data)
        return None
    
    def deposit(self, amount):
        self.balance += amount
        self.update_balance()
    
    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.update_balance()
            return True
        return False
    
    def update_balance(self):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("UPDATE customers SET balance=? WHERE id=?", (self.balance, self.id))
        conn.commit()
        conn.close()
