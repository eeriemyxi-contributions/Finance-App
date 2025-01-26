import sqlite3
import hashlib
from datetime import datetime

class Database:
    def __init__(self):
        # sqllite3 is a lightweight database
        # sqlite.connect will connect to the trading_app.db and if this dosent exist it will create a new one.
        # self.conn This stores the database connection as an instance variable
        self.conn = sqlite3.connect('trading_app.db', check_same_thread=False)  # on calling self.conn, it will connect to the trading_app.db database. and if it dosent exist's it will create a new one 
        self.create_tables()  # calling the function

    def create_tables(self):
        # Users table
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            balance REAL DEFAULT 100000.0
        )''')
        
        #   Explaination of the above table:
        #   self.conn.execute -> this will simply make a connection to the sql lite database
        #   PRIMARY KEY -> A universal value. This of it as someone's passport number.
        #   AUTOINCREMENT -> the id will initially start from 1 and than will be incremented automatically
        #   email -> should be a unique text inside the database.
        #   balance is a real number 
        #   DEFAULT is the value that all the users will get from the very start
        
        # Portfolio table
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            symbol TEXT NOT NULL,
            shares REAL NOT NULL,
            avg_price REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')

        # FOREIGN KEY -> Here you are establishing a connection from the users table 'id' and referencing it to foreign key.
        
        # Transactions table
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            symbol TEXT NOT NULL,
            transaction_type TEXT NOT NULL,
            shares REAL NOT NULL,
            price REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')

    
        self.conn.execute('''
        CREATE TABLE IF NOT EXISTS crypto_portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            symbol TEXT NOT NULL,
            crypto_amount REAL NOT NULL,
            avg_price REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )''')

        
        self.conn.commit()  # commit -> establishes connection

    # Function for adding a new user into the database
    def add_user(self, name, email, password):
        try:
            # Hashing the password to improve account security.
            # sha256 encoding cannot be reversed.
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            cursor = self.conn.execute(
                'INSERT INTO users (name, email, password) VALUES (?, ?, ?) RETURNING id',
                (name, email, hashed_password)
            )

            ''' Here the cursor is an object. When self.conn.execute is executed, it will return
            an object that contains the RETURNING id. And then we will use fetchone function to
            fetch the id contained inside the cursor object.
            '''

            user_id = cursor.fetchone()[0]  # this fetchone will fetch the things contained inside the cursor object
            self.conn.commit()  # Same as github. We need to commit the changes to the server
            return user_id
        except:
            return None

    # Function to verify the user by matching the password present in the database and the password entered by the user. 
    # Here since sha256 encoding is not reversible, to check the password, we are converting the password that entered 
    # by the user and checking the hashed password with the original hashed password stored in the database
    def verify_user(self, email, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        returned_id = self.conn.execute(
            'SELECT id, name, balance FROM users WHERE email=? AND password=?',
            (email, hashed_password)
        )

        result = returned_id.fetchone()

        # fetchone():
        # Returns a single row or record from the query result
        # Moves the cursor position by one row each time it's called

        # fetchall():
        # Retrieves all remaining rows from the query result set
        # Returns a list of tuples, with each tuple representing a row

        if result:
            return {'id': result[0], 'name': result[1], 'balance': result[2]}
        else:
            return None

    # Function to get the portfolio for the user . Here we are fetching the data from the database by searching it based on the user id.
    def get_portfolio(self, user_id):
        cursor = self.conn.execute(
            'SELECT symbol, shares, avg_price FROM portfolio WHERE user_id=?',
            (user_id,)
        )
        return cursor.fetchall()

    # Function to update the portfolio. When a user buys or sells a stock, update_portfolio function is called to change the user's portfolio.
    def update_portfolio(self, user_id, symbol, shares, price, is_buy):
        # Here the is_buy is a boolean. If it's a buy, then is_buy = True else False.
        cursor = self.conn.execute(
            'SELECT shares, avg_price FROM portfolio WHERE user_id = ? AND symbol=?',
            (user_id, symbol)
        )
        existing = cursor.fetchone()
        # We are storing the row into existing named list. 
        # If the user has buyed an existing stock's , then the existing list will contain that stock and the below 
        # if statement will be executed meaning that the stock values will be changed in the user's portfolio 
        # But if it's a complete new stock, then it will not be contained by the existing list, so the else condition will be called and a new stock will be added into the user's portfolio
        
        if is_buy:
            if existing:
                new_shares = existing[0] + shares  # existing is a list with elements [current_shares, avg_price]. Therefore existing[0] gives the current number of shares.
                old_shares = existing[1]
                only_new_share_price = new_shares * price  # caluculating the new price only for the stocks that were bought latest
                new_avg_price = ((old_shares + only_new_share_price)) / new_shares  # Calculating the average

                # Updating the portfolio
                self.conn.execute(
                    'UPDATE portfolio SET shares=?, avg_price=? WHERE user_id=? AND symbol=?',
                    (new_shares, new_avg_price, user_id, symbol)
                )
            else:
                self.conn.execute(
                    'INSERT INTO portfolio (user_id, symbol, shares, avg_price) VALUES (?, ?, ?, ?)',
                    (user_id, symbol, shares, price)
                )

        # If the order is for selling
        else:
            # If it's an existing stock already inside our database and the shares bought are less than the shares that the user wants to sell
            if existing and existing[0] >= shares:
                new_shares = existing[0] - shares
                # checking if the new shares are not less than 0 and if it is than delete entire stock row as the stock is no more inside the user's portfolio
                if new_shares > 0:
                    self.conn.execute(
                        'UPDATE portfolio SET shares=? WHERE user_id=? AND symbol=?',
                        (new_shares, user_id, symbol)
                    )
                else:
                    # Deleting the entire row for that particular user's particular stock
                    self.conn.execute(
                        'DELETE FROM portfolio WHERE user_id = ? AND symbol=?',
                        (user_id, symbol)
                    )
            else:
                # Returning false if the stock is not existing in the database. Since if there's no stock bought, it cannot be sold in the first place
                return False

        # recording the transaction
        self.conn.execute(
            'INSERT INTO transactions (user_id, symbol, transaction_type, shares, price) VALUES (?, ?, ?, ?, ?)',
            (user_id, symbol, 'BUY' if is_buy else 'SELL', shares, price)
        )

        # updating the user's balance
        transaction_value = shares * price
        self.conn.execute(
            'UPDATE users SET balance = balance + ? WHERE id=?',
            (-transaction_value if is_buy else transaction_value, user_id)
        )

        self.conn.commit()
        return True
    


    def update_crypto_portfolio(self, user_id, symbol, crypto_amount, current_price, is_buy):
        cursor = self.conn.execute(
            'SELECT crypto_amount, avg_price FROM crypto_portfolio WHERE user_id = ? AND symbol=?',
            (user_id, symbol)
        )
        
        existing = cursor.fetchone()

        if is_buy:
            if existing:
                new_amount = existing[0] + crypto_amount
                new_avg_price = ((existing[1] * existing[0]) + (current_price * crypto_amount)) / new_amount
                
                self.conn.execute(
                    'UPDATE crypto_portfolio SET crypto_amount=?, avg_price=? WHERE user_id = ? AND symbol = ?',
                    (new_amount, new_avg_price, user_id, symbol)
                )
            else:
                self.conn.execute(
                    'INSERT INTO crypto_portfolio (user_id, symbol, crypto_amount, avg_price) VALUES (?, ?, ?, ?)',
                    (user_id, symbol, crypto_amount, current_price)
                )
        else:
            if existing and existing[0] >= crypto_amount:
                new_amount = existing[0] - crypto_amount
                if new_amount > 0:
                    self.conn.execute(
                        'UPDATE crypto_portfolio SET crypto_amount=? WHERE user_id=? AND symbol=?',
                        (new_amount, user_id, symbol)
                    )
                else:
                    self.conn.execute(
                        'DELETE FROM crypto_portfolio WHERE user_id = ? AND symbol=?',
                        (user_id, symbol)
                    )
            else:
                return False
                
        self.conn.commit()
        return True