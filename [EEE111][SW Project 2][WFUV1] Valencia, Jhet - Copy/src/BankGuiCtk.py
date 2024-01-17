import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from BankDbSqlite import BankDbSqlite
import json
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from BankDbSqlite import BankDbSqlite

class BankGuiCtk(customtkinter.CTk):

    def __init__(self, dataBase=BankDbSqlite('AppDb.db')):
        super().__init__()
        self.db = dataBase

        self.title('Bank Management System')
        self.geometry('1090x900')
        self.config(bg='#FFFFF0')
        self.resizable(False, False)

        self.font1 = ('Georgia', 20, 'bold')
        self.font2 = ('Georgia', 12, 'bold')

        # Data Entry Form
        # 'Account' Label and Entry Widgets
        self.account_label = self.newCtkLabel('Account No.')
        self.account_label.place(x=800, y=40)
        self.account_entry = self.newCtkEntry()
        self.account_entry.place(x=800, y=80)

        # 'Name' Label and Entry Widgets
        self.name_label = self.newCtkLabel('Name')
        self.name_label.place(x=800, y=120)
        self.name_entry = self.newCtkEntry()
        self.name_entry.place(x=800, y=150)

        # 'Address' Label and Entry Widgets
        self.address_label = self.newCtkLabel('Address')
        self.address_label.place(x=800, y=190)
        self.address_entry = self.newCtkEntry()
        self.address_entry.place(x=800, y=220)

        # 'Balance' Label and Entry Widgets
        self.balance_label = self.newCtkLabel('Balance')
        self.balance_label.place(x=800, y=260)
        self.balance_entry = self.newCtkEntry()
        self.balance_entry.place(x=800, y=290)

        # 'Status' Label and Combo Box Widgets
        self.status_label = self.newCtkLabel('Status')
        self.status_label.place(x=800, y=330)
        self.status_cboxVar = StringVar()
        self.status_cboxOptions = ['Active', 'Terminated']
        self.status_cbox = self.newCtkComboBox(options=self.status_cboxOptions, 
                                    entryVariable=self.status_cboxVar)
        self.status_cbox.place(x=800, y=360)


        self.add_button = self.newCtkButton(text='Add Account',
                                onClickHandler=self.add_entry,
                                fgColor='#0096FF',
                                hoverColor='#00FFFF',
                                borderColor='#F0FFFF')
        self.add_button.place(x=800,y=675)

        self.new_button = self.newCtkButton(text='New Account',
                                onClickHandler=lambda:self.clear_form(True),
                                fgColor='#6082B6',
                                hoverColor='#00FFFF',
                                borderColor='#7DF9FF')
        self.new_button.place(x=800,y=425)

        self.update_button = self.newCtkButton(text='Update Account',
                                    onClickHandler=self.update_entry,
                                    fgColor='#6082B6',
                                    hoverColor='#00FFFF',
                                    borderColor='#7DF9FF')
        self.update_button.place(x=800,y=475)

        self.delete_button = self.newCtkButton(text='Delete Account',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#E40404',
                                    hoverColor='#AE0000',
                                    borderColor='#E40404')
        self.delete_button.place(x=800,y=725)

        self.export_button = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv,
                                    fgColor='#6082B6',
                                    hoverColor='#00FFFF',
                                    borderColor='#7DF9FF')
        self.export_button.place(x=800,y=575)

        self.import_button = self.newCtkButton(text='Import from CSV',
                                    onClickHandler=self.import_from_csv,
                                    fgColor='#6082B6',
                                    hoverColor='#00FFFF',
                                    borderColor='#7DF9FF')
        self.import_button.place(x=800,y=525)

        self.exportJSON_button = self.newCtkButton(text='Export to Json',
                                    onClickHandler=self.export_entries_to_json,
                                    fgColor='#6082B6',
                                    hoverColor='#00FFFF',
                                    borderColor='#7DF9FF')
        self.exportJSON_button.place(x=800,y=625)

        # Tree View for Database Entries
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#F0FFFF',
                        background='#000',
                        fieldlbackground='#00FFFF')

        self.style.map('Treeview', background=[('selected', '#00FFFF')])

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

        self.tree.place(x=40, y=60, width=900, height=875)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    # new Label Widget
    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#343434'
        widget_BgColor='#FFFFF0'

        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                    bg_color=widget_BgColor)
        return widget

    # new Entry Widget
    def newCtkEntry(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#1F51FF'
        widget_BorderWidth=2
        widget_Width=250

        widget = customtkinter.CTkEntry(self,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    border_color=widget_BorderColor,
                                    border_width=widget_BorderWidth,
                                    width=widget_Width)
        return widget

    # new Combo Box Widget
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_DropdownHoverColor='#0C9295'
        widget_ButtonColor='#0C9295'
        widget_ButtonHoverColor='#0C9295'
        widget_BorderColor='#1F51FF'
        widget_BorderWidth=2
        widget_Width=250
        widget_Options=options

        widget = customtkinter.CTkComboBox(self,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        border_color=widget_BorderColor,
                                        width=widget_Width,
                                        variable=entryVariable,
                                        values=options,
                                        state='readonly')
        
        # set default value to 1st option
        widget.set(options[0])

        return widget

    # new Button Widget
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#FFFFF0', hoverColor='#FF5002', bgColor='#FFFFF0', borderColor='#F15704'):
        widget_Font=self.font1
        widget_TextColor='#fff'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=260
        widget_Function=onClickHandler

        widget = customtkinter.CTkButton(self,
                                        text=text,
                                        command=widget_Function,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        hover_color=widget_HoverColor,
                                        bg_color=widget_BackgroundColor,
                                        border_color=widget_BorderColor,
                                        border_width=widget_BorderWidth,
                                        cursor=widget_Cursor,
                                        corner_radius=widget_CornerRadius,
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
        self.account_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.address_entry.delete(0, END)
        self.balance_entry.delete(0, END)
        self.status_cboxVar.set('Active')

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.account_entry.insert(0, row[0])
            self.name_entry.insert(0, row[1])
            self.address_entry.insert(0, str(row[2]))
            self.balance_entry.insert(0, str(row[3]))
            self.status_cboxVar.set(row[4])
        else:
            pass

    def add_entry(self):
        account=self.account_entry.get()
        name=self.name_entry.get()
        address=self.address_entry.get()
        balance=self.balance_entry.get()
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
            account = self.account_entry.get()
            self.db.delete_account(account)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Account has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an Account to update')
        else:
            account=self.account_entry.get()
            name=self.name_entry.get()
            address=self.address_entry.get()
            balance=self.balance_entry.get()
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



