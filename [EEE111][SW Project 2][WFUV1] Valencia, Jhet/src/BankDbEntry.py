class BankDbEntry:
    def __init__(self,
                 account=1,
                 name='Name',
                 address='address',
                 balance='balance',
                 status='Active'):
        self.account = account
        self.name = name
        self.address = address
        self.balance = balance
        self.status = status
