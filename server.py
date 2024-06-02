import tkinter as tk
from tkinter import *
from tkinter import ttk
import psycopg2
from tkinter import messagebox

# PostgreSQL connection setup
def connect_to_db():
    try:
        conn = psycopg2.connect(
            database="links",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Connection Error", str(e))
        return None

# Main screen setup
screen = Tk()
screen.geometry('800x1100')
screen.configure(bg='#000000')
screen.resizable(0, 0)
screen.title("Links Library")

def add_record(table, url_entry, category_entry, question_entry):
    url = url_entry.get()
    category = category_entry.get()
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

def edit_record(tree, url_entry, category_entry, question_entry):
    try:
        selected_item = tree.selection()[0]
        old_values = tree.item(selected_item, 'values')
        url = url_entry.get()
        category = category_entry.get()
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

def open_popup():
    top = Toplevel(screen)
    top.title('Category Window')
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

    category_label = Label(entry_frame, text="Category", bg='#2b2b2b', fg='#ffffff')
    category_label.grid(row=1, column=0, padx=5, pady=5)
    category_entry = Entry(entry_frame, width=40)
    category_entry.grid(row=1, column=1, padx=5, pady=5)

    question_label = Label(entry_frame, text="Question", bg='#2b2b2b', fg='#ffffff')
    question_label.grid(row=2, column=0, padx=5, pady=5)
    question_entry = Entry(entry_frame, width=40)
    question_entry.grid(row=2, column=1, padx=5, pady=5)

    button_frame = Frame(top, bg='#2b2b2b')
    button_frame.pack(pady=10)

    add_btn = Button(button_frame, text='Add', command=lambda: add_record(table, url_entry, category_entry, question_entry),
                     bg='#4CAF50', fg='#ffffff', width=10)
    add_btn.grid(row=0, column=0, padx=5, pady=5)
    
    delete_btn = Button(button_frame, text='Delete', command=lambda: delete_record(table),
                        bg='#f44336', fg='#ffffff', width=10)
    delete_btn.grid(row=0, column=1, padx=5, pady=5)
    
    edit_btn = Button(button_frame, text='Edit', command=lambda: edit_record(table, url_entry, category_entry, question_entry),
                      bg='#2196F3', fg='#ffffff', width=10)
    edit_btn.grid(row=0, column=2, padx=5, pady=5)

category_label = Label(screen, text="Click here to add a new category", font="Tahoma 15",
                       fg="#FFFF69", bg='#000000')
category_label.pack(pady=10)

btn = Button(screen, text="Open", command=open_popup, bg='#673AB7', fg='#ffffff', font=("Tahoma", 12), width=20)
btn.pack(pady=10)

screen.mainloop()
