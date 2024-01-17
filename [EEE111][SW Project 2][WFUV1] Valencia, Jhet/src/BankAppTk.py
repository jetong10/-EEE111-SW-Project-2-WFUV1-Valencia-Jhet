from BankDb import BankDb
from BankGuiTk import BankGuiTk

def main():
    db = BankDb(init=False, dbName='BankDb.csv')
    app = BankGuiTk(dataBase=db)
    app.mainloop()

if __name__ == "__main__":
    main()