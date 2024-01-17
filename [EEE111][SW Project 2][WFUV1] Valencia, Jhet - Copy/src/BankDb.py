from BankDbEntry import BankDbEntry
import json
import csv

class BankDb:
    """
    - simple database to store BankDbEntry objects
    """    

    def __init__(self, init=False, dbName='BankDb.csv'):
        """
        - initialize database variables here
        - mandatory :
            - any type can be used to store database entries for BankDbEntry objects
            - e.g. list of class, list of dictionary, list of tuples, dictionary of tuples etc.
        """
        # CSV filename         
        self.dbName = dbName
        # initialize container of database entries
        self.entries = []
        print('TODO: __init__')


    def fetch_accounts(self):
        print('TODO: fetch_accounts')
        tupleList = []

        # Append entries from self.entries to tupleList
        tupleList += [(entry.account, entry.name, entry.address, entry.balance, entry.status) for entry in self.entries]

        return tupleList

    def insert_account(self, account, name, address, balance, status):
        """
        - inserts an entry in the database
        - no return value
        """
        newEntry = BankDbEntry(account=account, name=name, address=address, balance=balance, status=status)
        self.entries.append(newEntry)
        print('TODO: insert_account')

    def delete_account(self, account):
        """
        - deletes the corresponding entry in the database as specified by 'account'
        - no return value
        """
        for entry in self.entries:
            if entry.account == account:
                self.entries.remove(entry)
        print('TODO: delete_account')

    def update_account(self, update_name, update_address, update_balance, update_status, account):
        """
        - updates the corresponding entry in the database as specified by 'account'
        - no return value
        """
        for entry in self.entries:
            if entry.account == account:
                entry.name = update_name
                entry.address = update_address
                entry.balance = update_balance
                entry.status = update_status
        print('TODO: update_account')     
              

    def export_csv(self):
        with open(self.dbName, 'w') as file:
            for entry in self.entries:
                file.write(f"{entry.account},{entry.name},{entry.address},{entry.balance},{entry.status}\n")
        print('TODO: export_csv')
    
    def import_csv(self, csv_filename):
        try:
            if not csv_filename.lower().endswith('.csv'):
                csv_filename += '.csv'

            with open(csv_filename, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    account_no, account_name, account_address, account_balance, account_status = row
                    # Add logic to handle the data, e.g., insert into your database
                    self.insert_account(account_no, account_name, account_address, account_balance, account_status)
            print('Data imported successfully')
            return True
        except FileNotFoundError:
            print(f'Error importing data: File not found - {csv_filename}')
            return False
        except Exception as e:
            print(f'Error importing data: {e}')
            return False

    def export_json(self, json_filename='BankDb.json'):
        data = [{'Account': entry.account,
                 'Name': entry.name,
                 'Address': entry.address,
                 'Balance': entry.balance,
                 'Status': entry.status} for entry in self.entries]

        with open(json_filename, 'w') as json_file:
            json.dump(data, json_file, indent=2)

    def account_exists(self, account):
        """
        - returns True if an entry exists for the specified 'account'
        - else returns False
        """
        return any(entry.account == account for entry in self.entries)