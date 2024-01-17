'''
This is the interface to an SQLite Database
'''

import sqlite3

class BankDbSqlite:
    def __init__(self, dbName='Accounts.db'):
        super().__init__()
        self.dbName = dbName
        self.csvFile = self.dbName.replace('.db', '.csv')
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Accounts (
                account TEXT PRIMARY KEY,
                name TEXT,
                address TEXT,
                balance TEXT,
                status TEXT)''')
        self.conn.commit()
        self.conn.close()

    def connect_cursor(self):
        self.conn = sqlite3.connect(self.dbName)
        self.cursor = self.conn.cursor()        

    def commit_close(self):
        self.conn.commit()
        self.conn.close()        

    def create_table(self):
        self.connect_cursor()
        self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Accounts (
                    account TEXT PRIMARY KEY,
                    name TEXT,
                    address TEXT,
                    balance TEXT,
                    status TEXT)''')
        self.commit_close()

    def fetch_accounts(self):
        self.connect_cursor()
        self.cursor.execute('SELECT * FROM Accounts')
        accounts =self.cursor.fetchall()
        self.conn.close()
        return accounts

    def insert_account(self, account, name, address, balance, status):
        self.connect_cursor()
        self.cursor.execute('INSERT INTO Accounts (account, name, address, balance, status) VALUES (?, ?, ?, ?, ?)',
                    (account, name, address, balance, status))
        self.commit_close()

    def delete_account(self, account):
        self.connect_cursor()
        self.cursor.execute('DELETE FROM Accounts WHERE account = ?', (account,))
        self.commit_close()

    def update_account(self, new_name, new_address, new_balance, new_status, account):
        self.connect_cursor()
        self.cursor.execute('UPDATE Accounts SET name = ?, address = ?, balance = ?, status = ? WHERE account = ?',
                    (new_name, new_address, new_balance, new_status, account))
        self.commit_close()

    def account_exists(self, account):
        self.connect_cursor()
        self.cursor.execute('SELECT COUNT(*) FROM Accounts WHERE account = ?', (account,))
        result =self.cursor.fetchone()
        self.conn.close()
        return result[0] > 0

    def export_csv(self):
        with open(self.csvFile, "w") as filehandle:
            dbEntries = self.fetch_accounts()
            for entry in dbEntries:
                print(entry)
                filehandle.write(f"{entry[0]},{entry[1]},{entry[2]},{entry[3]},{entry[4]}\n")

def test_BankDb():
    iBankDb = BankDbSqlite(dbName='BankDbSql.db')

    for entry in range(30):
        iBankDb.insert_account(entry, f'Name{entry} Surname{entry}', f'Address {entry}', f'Balance {entry}', 'Active')
        assert iBankDb.account_exists(entry)

    all_entries = iBankDb.fetch_accounts()
    assert len(all_entries) == 30

    for entry in range(10, 20):
        iBankDb.update_account(f'Name{entry} Surname{entry}', f'Address {entry}', f'Balance {entry}', 'Terminated', entry)
        assert iBankDb.account_exists(entry)

    all_entries = iBankDb.fetch_accounts()
    assert len(all_entries) == 30

    for entry in range(10):
        iBankDb.delete_account(entry)
        assert not iBankDb.account_exists(entry) 

    all_entries = iBankDb.fetch_accounts()
    assert len(all_entries) == 20