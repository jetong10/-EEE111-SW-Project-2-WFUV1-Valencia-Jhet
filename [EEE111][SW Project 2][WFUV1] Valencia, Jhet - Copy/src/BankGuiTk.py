from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from BankDbSqlite import BankDbSqlite
import json
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from BankDbSqlite import BankDbSqlite

class BankGuiTk(Tk):

    def __init__(self, dataBase=BankDbSqlite('AppDb.db')):
        super().__init__()
        self.db = dataBase

        self.title('Bank Management System')
        self.geometry('1500x500')
        self.config(bg='#161C25')
        self.resizable(False, False)

        self.font1 = ('Arial', 20, 'bold')
        self.font2 = ('Arial', 12, 'bold')

        # Data Entry Form
        # 'Account' Label and Entry Widgets
        self.account_label = self.newCtkLabel('Account')
        self.account_label.place(x=20, y=40)
        self.account_entryVar = StringVar()
        self.account_entry = self.newCtkEntry(entryVariable=self.account_entryVar)
        self.account_entry.place(x=100, y=40)

        # 'Name' Label and Entry Widgets
        self.name_label = self.newCtkLabel('Name')
        self.name_label.place(x=20, y=100)
        self.name_entryVar = StringVar()
        self.name_entry = self.newCtkEntry(entryVariable=self.name_entryVar)
        self.name_entry.place(x=100, y=100)

        # 'Address' Label and Entry Widgets
        self.address_label = self.newCtkLabel('Address')
        self.address_label.place(x=20, y=160)
        self.address_entryVar = StringVar()
        self.address_entry = self.newCtkEntry(entryVariable=self.address_entryVar)
        self.address_entry.place(x=100, y=160)

        # 'Balance' Label and Combo Box Widgets
        self.balance_label = self.newCtkLabel('Balance')
        self.balance_label.place(x=20, y=220)
        self.balance_entryVar = StringVar()
        self.balance_entry = self.newCtkEntry(entryVariable=self.balance_entryVar)
        self.balance_entry.place(x=100, y=220)

        # 'Status' Label and Combo Box Widgets
        self.status_label = self.newCtkLabel('Status')
        self.status_label.place(x=20, y=280)
        self.status_cboxVar = StringVar()
        self.status_cboxOptions = ['Active', 'Terminated']
        self.status_cbox = self.newCtkComboBox(options=self.status_cboxOptions, 
                                    entryVariable=self.status_cboxVar)
        self.status_cbox.place(x=100, y=280)


        self.add_button = self.newCtkButton(text='Add Account',
                                onClickHandler=self.add_entry,
                                fgColor='#05A312',
                                hoverColor='#00850B',
                                borderColor='#05A312')
        self.add_button.place(x=50,y=350)

        self.new_button = self.newCtkButton(text='New Account',
                                onClickHandler=lambda:self.clear_form(True))
        self.new_button.place(x=50,y=400)

        self.update_button = self.newCtkButton(text='Update Account',
                                    onClickHandler=self.update_entry)
        self.update_button.place(x=360,y=400)

        self.delete_button = self.newCtkButton(text='Delete Account',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#E40404',
                                    hoverColor='#AE0000',
                                    borderColor='#E40404')
        self.delete_button.place(x=670,y=400)

        self.export_button = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv)
        self.export_button.place(x=980,y=400)

        # Tree View for Database Entries
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#fff',
                        background='#000',
                        fieldlbackground='#313837')

        self.style.map('Treeview', background=[('selected', '#1A8F2D')])

        self.tree = ttk.Treeview(self, height=15)
        self.tree['columns'] = ('Account', 'Name', 'Address', 'Balance', 'Status')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Account', anchor=tk.CENTER, width=10)
        self.tree.column('Name', anchor=tk.CENTER, width=150)
        self.tree.column('Address', anchor=tk.CENTER, width=150)
        self.tree.column('Balance', anchor=tk.CENTER, width=10)
        self.tree.column('Status', anchor=tk.CENTER, width=150)

        self.tree.heading('Account', text='Account No.')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Address', text='Address')
        self.tree.heading('Balance', text='Balance')
        self.tree.heading('Status', text='Status')

        self.tree.place(x=360, y=20, width=1000, height=350)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    # new Label Widget
    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_BgColor='#161C25'

        widget = ttk.Label(self, 
                        text=text)
        return widget

    # new Entry Widget
    def newCtkEntry(self, text = 'CTK Label', entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=25

        widget = ttk.Entry(self, textvariable=entryVariable, width=widget_Width)
        return widget

    # new Combo Box Widget
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_DropdownHoverColor='#0C9295'
        widget_ButtonColor='#0C9295'
        widget_ButtonHoverColor='#0C9295'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=25
        widget_Options=options

        widget = ttk.Combobox(self, 
                              textvariable=entryVariable,
                              width=widget_Width)
        
        # set default value to 1st option
        widget['values'] = tuple(options)
        widget.current(1)
        return widget

    # new Button Widget
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#161C25', hoverColor='#FF5002', bgColor='#161C25', borderColor='#F15704'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=25
        widget_Function=onClickHandler

        widget = ttk.Button(self,
                            text=text,
                            command=widget_Function,
                            width=widget_Width)
       
        return widget

    # Handles
    def add_to_treeview(self):
        accounts = self.db.fetch_accounts()
        self.tree.delete(*self.tree.get_children())
        for account in accounts:
            print(account)
            self.tree.insert('', END, values=account)

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.account_entryVar.set('')
        self.name_entryVar.set('')
        self.address_entryVar.set('')
        self.balance_entryVar.set('')
        self.status_cboxVar.set('Active')

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.account_entryVar.set(row[0])
            self.name_entryVar.set(row[1])
            self.address_entryVar.set(row[2])
            self.balance_entryVar.set(row[3])
            self.status_cboxVar.set(row[4])
        else:
            pass

    def add_entry(self):
        account=self.account_entryVar.get()
        name=self.name_entryVar.get()
        address=self.address_entryVar.get()
        balance=self.balance_entryVar.get()
        status=self.status_cboxVar.get()

        if not (account and name and address and balance and status):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.account_exists(account):
            messagebox.showerror('Error', 'Account already exists')
        else:
            self.db.insert_account(account, name, address, balance, status)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Account has been inserted')

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an Account to delete')
        else:
            account = self.account_entryVar.get()
            self.db.delete_account(account)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Account has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an Account to update')
        else:
            account=self.account_entryVar.get()
            name=self.name_entryVar.get()
            address=self.address_entryVar.get()
            balance=self.balance_entryVar.get()
            status=self.status_cboxVar.get()
            self.db.update_account(name, address, balance, status, account)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Account has been updated')

    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.csv')
    
    def import_from_csv(self):

        file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", ".csv")])

        if not file_path:
            messagebox.showinfo('Info', 'No file selected.')
            return

        if self.db.import_csv(file_path):
            messagebox.showinfo('Success', f'Data imported from {file_path}')
            # Optionally, update the displayed data in your GUI after importing
            self.add_to_treeview()
        else:
            messagebox.showerror('Error', f'Failed to import data from {file_path}')

    def export_entries_to_json(self):
        accounts = self.db.fetch_accounts()
        json_data = []

        for account in accounts:
            account_dict = {
                'Account No.': account[0],
                'Name': account[1],
                'Address': account[2],
                'Balance': account[3],
                'Status': account[4]
            }
            json_data.append(account_dict)

        # Export to JSON file
        with open('Accounts.json', 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

        messagebox.showinfo('Success', 'Data exported to Accounts.json')



