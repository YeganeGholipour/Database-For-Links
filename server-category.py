import tkinter as tk
from tkinter import *
from tkinter import ttk
import psycopg2
from tkinter import messagebox

# PostgreSQL connection setup
def connect_to_db():
    try:
        conn = psycopg2.connect(
            database="your_database",
            user="your_username",
            password="your_password",
            host="your_host",
            port="your_port"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Connection Error", str(e))
        return None

# Main screen setup
screen = Tk()
screen.geometry('500x400')
screen.configure(bg='#000000')
screen.resizable(0, 0)
screen.title("Links Library")

def add_record(table, url_entry, category, question_entry):
    url = url_entry.get()
    question = question_entry.get()
    table.insert(parent='', index='end', values=(url, category, question))

    # Insert data into PostgreSQL
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO links (url, category, question) VALUES (%s, %s, %s)", (url, category, question))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("Success", "Record added to the database")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

def delete_record(tree):
    try:
        selected_item = tree.selection()[0]
        values = tree.item(selected_item, 'values')
        tree.delete(selected_item)

        # Delete data from PostgreSQL
        conn = connect_to_db()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("DELETE FROM links WHERE url=%s AND category=%s AND question=%s", (values[0], values[1], values[2]))
                conn.commit()
                cur.close()
                conn.close()
                messagebox.showinfo("Success", "Record deleted from the database")
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
    except IndexError:
        print("No item selected")

def edit_record(tree, url_entry, category, question_entry):
    try:
        selected_item = tree.selection()[0]
        old_values = tree.item(selected_item, 'values')
        url = url_entry.get()
        question = question_entry.get()
        tree.item(selected_item, values=(url, category, question))

        # Update data in PostgreSQL
        conn = connect_to_db()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("UPDATE links SET url=%s, category=%s, question=%s WHERE url=%s AND category=%s AND question=%s",
                            (url, category, question, old_values[0], old_values[1], old_values[2]))
                conn.commit()
                cur.close()
                conn.close()
                messagebox.showinfo("Success", "Record updated in the database")
            except Exception as e:
                messagebox.showerror("Database Error", str(e))
    except IndexError:
        print("No item selected")

def open_popup(category):
    top = Toplevel(screen)
    top.title(f'{category} Category Window')
    top.configure(bg='#2b2b2b')
    
    table_frame = Frame(top, bg='#2b2b2b')
    table_frame.pack(pady=10, padx=10)

    table = ttk.Treeview(table_frame, columns=('url', 'category', 'question'), show='headings')
    table.heading('url', text='URL')
    table.heading('category', text='Category')
    table.heading('question', text='Question')
    table.pack(side=LEFT)

    scrollbar = ttk.Scrollbar(table_frame, orient=VERTICAL, command=table.yview)
    table.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)

    entry_frame = Frame(top, bg='#2b2b2b')
    entry_frame.pack(pady=10, padx=10)

    url_label = Label(entry_frame, text="URL", bg='#2b2b2b', fg='#ffffff')
    url_label.grid(row=0, column=0, padx=5, pady=5)
    url_entry = Entry(entry_frame, width=40)
    url_entry.grid(row=0, column=1, padx=5, pady=5)

    question_label = Label(entry_frame, text="Question", bg='#2b2b2b', fg='#ffffff')
    question_label.grid(row=1, column=0, padx=5, pady=5)
    question_entry = Entry(entry_frame, width=40)
    question_entry.grid(row=1, column=1, padx=5, pady=5)

    button_frame = Frame(top, bg='#2b2b2b')
    button_frame.pack(pady=10)

    add_btn = Button(button_frame, text='Add', command=lambda: add_record(table, url_entry, category, question_entry),
                     bg='#4CAF50', fg='#ffffff', width=10)
    add_btn.grid(row=0, column=0, padx=5, pady=5)
    
    delete_btn = Button(button_frame, text='Delete', command=lambda: delete_record(table),
                        bg='#f44336', fg='#ffffff', width=10)
    delete_btn.grid(row=0, column=1, padx=5, pady=5)
    
    edit_btn = Button(button_frame, text='Edit', command=lambda: edit_record(table, url_entry, category, question_entry),
                      bg='#2196F3', fg='#ffffff', width=10)
    edit_btn.grid(row=0, column=2, padx=5, pady=5)

# Define the categories you want to manage
categories = ["OpenCV", "Django", "Linux"]

# Function to add new category buttons
def add_new_category():
    new_category = new_category_entry.get()
    if new_category and new_category not in categories:
        categories.append(new_category)
        create_category_buttons()

# Function to create buttons for each category
def create_category_buttons():
    for widget in category_buttons_frame.winfo_children():
        widget.destroy()

    for category in categories:
        btn = Button(category_buttons_frame, text=f"Open {category}", command=lambda c=category: open_popup(c),
                     bg='#673AB7', fg='#ffffff', font=("Tahoma", 12), width=20)
        btn.pack(pady=5)

# Frame for category buttons
category_buttons_frame = Frame(screen, bg='#000000')
category_buttons_frame.pack(pady=20)

create_category_buttons()

# Entry and button to add new category
new_category_frame = Frame(screen, bg='#000000')
new_category_frame.pack(pady=20)

new_category_lbl = Label(new_category_frame, text="New Category", bg='#000000', fg='#ffffff')
new_category_lbl.pack(side=LEFT, padx=5)

new_category_entry = Entry(new_category_frame, width=20)
new_category_entry.pack(side=LEFT, padx=5)

new_category_btn = Button(new_category_frame, text='Add Category', command=add_new_category,
                          bg='#4CAF50', fg='#ffffff')
new_category_btn.pack(side=LEFT, padx=5)

screen.mainloop()
