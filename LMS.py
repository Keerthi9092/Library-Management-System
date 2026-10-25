
import tkinter as tk
from tkinter import messagebox, ttk

# Store books temporarily in a list
books = []
issued_books = []

# Main window
root = tk.Tk()
root.title("Library Management System")
root.geometry("900x600")
root.config(bg="#eaf0f6")

# Heading
heading = tk.Label(
    root,
    text="LIBRARY MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold"),
    bg="#263859",
    fg="white",
    pady=15
)
heading.pack(fill="x")

# Book details frame
frame = tk.LabelFrame(
    root,
    text="Book Details",
    font=("Arial", 12, "bold"),
    bg="#eaf0f6",
    padx=15,
    pady=15
)
frame.pack(fill="x", padx=20, pady=15)

# Input fields
tk.Label(frame, text="Book Name:", bg="#eaf0f6").grid(row=0, column=0, padx=10, pady=5)
book_name = tk.Entry(frame, width=25)
book_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Author:", bg="#eaf0f6").grid(row=0, column=2, padx=10, pady=5)
author = tk.Entry(frame, width=25)
author.grid(row=0, column=3, padx=10, pady=5)

tk.Label(frame, text="Quantity:", bg="#eaf0f6").grid(row=1, column=0, padx=10, pady=5)
quantity = tk.Entry(frame, width=25)
quantity.grid(row=1, column=1, padx=10, pady=5)

# Book table
table = ttk.Treeview(
    root,
    columns=("ID", "Book", "Author", "Quantity"),
    show="headings",
    height=10
)

table.heading("ID", text="Book ID")
table.heading("Book", text="Book Name")
table.heading("Author", text="Author")
table.heading("Quantity", text="Available Quantity")

table.column("ID", width=80)
table.column("Book", width=250)
table.column("Author", width=250)
table.column("Quantity", width=150)

table.pack(fill="x", padx=20, pady=10)


# Add book function
def add_book():

    name = book_name.get().strip()
    book_author = author.get().strip()
    qty = quantity.get().strip()

    if name == "" or book_author == "" or qty == "":
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        qty = int(qty)

        if qty <= 0:
            messagebox.showerror("Error", "Quantity must be positive")
            return

    except ValueError:
        messagebox.showerror("Error", "Enter a valid quantity")
        return

    book_id = len(books) + 1

    book = {
        "id": book_id,
        "name": name,
        "author": book_author,
        "quantity": qty
    }

    books.append(book)

    display_books()

    book_name.delete(0, tk.END)
    author.delete(0, tk.END)
    quantity.delete(0, tk.END)

    messagebox.showinfo("Success", "Book added successfully")


# Display books function
def display_books():

    for row in table.get_children():
        table.delete(row)

    for book in books:
        table.insert(
            "",
            tk.END,
            values=(
                book["id"],
                book["name"],
                book["author"],
                book["quantity"]
            )
        )


# Delete book function
def delete_book():

    selected = table.selection()

    if not selected:
        messagebox.showerror("Error", "Please select a book")
        return

    book_id = table.item(selected[0])["values"][0]

    for book in books:

        if book["id"] == book_id:

            if book["quantity"] == 0:
                messagebox.showerror(
                    "Error",
                    "All copies of this book are issued"
                )
                return

            books.remove(book)
            break

    display_books()

    messagebox.showinfo("Success", "Book deleted successfully")


# Search book function
def search_book():

    search_text = search_entry.get().lower()

    for row in table.get_children():
        table.delete(row)

    for book in books:

        if (
            search_text in book["name"].lower()
            or search_text in book["author"].lower()
        ):

            table.insert(
                "",
                tk.END,
                values=(
                    book["id"],
                    book["name"],
                    book["author"],
                    book["quantity"]
                )
            )


# Issue book function
def issue_book():

    selected = table.selection()

    if not selected:
        messagebox.showerror("Error", "Please select a book")
        return

    book_id = table.item(selected[0])["values"][0]

    for book in books:

        if book["id"] == book_id:

            if book["quantity"] <= 0:
                messagebox.showerror(
                    "Error",
                    "Book is not available"
                )
                return

            student = student_entry.get().strip()

            if student == "":
                messagebox.showerror(
                    "Error",
                    "Enter student name"
                )
                return

            book["quantity"] -= 1

            issued_books.append({
                "book_id": book["id"],
                "book_name": book["name"],
                "student": student
            })

            display_books()

            student_entry.delete(0, tk.END)

            messagebox.showinfo(
                "Success",
                "Book issued successfully"
            )

            break


# Return book function
def return_book():

    selected = table.selection()

    if not selected:
        messagebox.showerror("Error", "Please select a book")
        return

    book_id = table.item(selected[0])["values"][0]

    for issue in issued_books:

        if issue["book_id"] == book_id:

            for book in books:

                if book["id"] == book_id:

                    book["quantity"] += 1

                    issued_books.remove(issue)

                    display_books()

                    messagebox.showinfo(
                        "Success",
                        "Book returned successfully"
                    )

                    return

    messagebox.showerror(
        "Error",
        "No issued copy found for this book"
    )


# Buttons
button_frame = tk.Frame(root, bg="#eaf0f6")
button_frame.pack(pady=5)

tk.Button(
    button_frame,
    text="Add Book",
    command=add_book,
    bg="#27ae60",
    fg="white",
    width=15
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame,
    text="Delete Book",
    command=delete_book,
    bg="#e74c3c",
    fg="white",
    width=15
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame,
    text="Display Books",
    command=display_books,
    bg="#3498db",
    fg="white",
    width=15
).grid(row=0, column=2, padx=5)


# Search section
search_frame = tk.Frame(root, bg="#eaf0f6")
search_frame.pack(pady=10)

tk.Label(
    search_frame,
    text="Search:",
    bg="#eaf0f6"
).grid(row=0, column=0, padx=5)

search_entry = tk.Entry(search_frame, width=30)
search_entry.grid(row=0, column=1, padx=5)

tk.Button(
    search_frame,
    text="Search Book",
    command=search_book,
    bg="#8e44ad",
    fg="white"
).grid(row=0, column=2, padx=5)


# Student issue section
issue_frame = tk.LabelFrame(
    root,
    text="Issue / Return Book",
    bg="#eaf0f6",
    padx=10,
    pady=10
)
issue_frame.pack(fill="x", padx=20, pady=10)

tk.Label(
    issue_frame,
    text="Student Name:",
    bg="#eaf0f6"
).grid(row=0, column=0, padx=5)

student_entry = tk.Entry(issue_frame, width=25)
student_entry.grid(row=0, column=1, padx=5)

tk.Button(
    issue_frame,
    text="Issue Book",
    command=issue_book,
    bg="#f39c12",
    fg="white",
    width=15
).grid(row=0, column=2, padx=10)

tk.Button(
    issue_frame,
    text="Return Book",
    command=return_book,
    bg="#16a085",
    fg="white",
    width=15
).grid(row=0, column=3, padx=10)


# Run application
root.mainloop()
