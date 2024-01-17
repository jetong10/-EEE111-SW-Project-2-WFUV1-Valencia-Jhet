from BankDb import BankDb
from BankGuiCtk import BankGuiCtk

def main():
    db = BankDb(init=False, dbName='BankDb.csv')
    app = BankGuiCtk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()