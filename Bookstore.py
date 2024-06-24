'''A program enabling a bookstore clerk to manage an SQL database of 
stock, with options to add new books to the database, and search, update
and delete existing records.'''

# ---------- LIBRARIES ----------

import sqlite3

# ---------- FUNCTIONS ----------

def create_database():
    """
    Creates database 'ebookstore.db' and table 'book' to store book data 
    if they do not already exist.
    """
    with sqlite3.connect('ebookstore.db') as db:
        cursor = db.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS
            book(id INTEGER PRIMARY KEY, title TEXT, author TEXT, qty INTEGER)
               ''')
        db.commit()


def populate_database():
    """
    Populates database with initial records if not already populated.
    """
    books = [
        (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
        (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
        (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
        (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37),
        (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
    ]
    with sqlite3.connect('ebookstore.db') as db:
        cursor = db.cursor()
        cursor.execute('''SELECT COUNT(*) FROM book''')
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.executemany('''INSERT INTO book (id, title, author, qty) 
                        VALUES (?, ?, ?, ?)''', books)
            db.commit()


def enter_book():
    """
    Adds a new book record to 'book' table in the database.
    """
    with sqlite3.connect('ebookstore.db') as db:
        cursor = db.cursor()
        while True:
            id = (input("Enter book ID: "))
            if id.isnumeric():
                id = int(id)
                try:
                    cursor.execute('''SELECT COUNT(*) FROM book 
                                   WHERE id = ?''', (id,))
                    if cursor.fetchone()[0] > 0:
                        print(f"ID {id} already exists. Please enter a unique ID.")
                    else:
                        break 
                except sqlite3.Error as e:
                    print(f"An error occurred: {e}")
                    return   
            else:
                print("Please enter ID as an integer.")
        title = input("Enter book title: ")
        author = input("Enter name of author: ")
        while True:
            qty = input("Enter quantity in stock: ")
            if qty.isnumeric():
                qty = int(qty)
                break
            else:
                print("Please enter quantity as an integer.")
        
        cursor.execute('''INSERT INTO book 
                (id, title, author,qty)VALUES (?, ?, ?, ?)''', 
                (id, title, author, qty))
        db.commit()
        print(f"\n{title} has been added to the database. Full record:")
        print(f"id: {id} | title: {title} | author: {author} | qty: {qty}\n")
        print("-"*10)


def update_book():
    """
    Updates an existing book record in the database.
    """
    while True:
        while True:
            # Take user input for record to update.
            update_record = input('''
Record to update (enter ID, or enter 'done' to return to main menu): ''')
            if update_record.lower() == 'done':
                return
            if not update_record.isnumeric():
                print("Enter ID as an integer.")
                continue
            update_record = int(update_record)
            # Verify id against existing records.
            with sqlite3.connect('ebookstore.db') as db:
                cursor = db.cursor()
                cursor.execute('''SELECT COUNT(*) FROM book WHERE id = ?''',
                                (update_record,))
                if cursor.fetchone()[0] == 0:
                    print(f"ID {update_record} does not match any records.")
                else:
                    break

        # Take user input for field to update.
        while True:
            update_field = input('''
Enter field to update (id/title/author/qty), or enter 'done' to finish: 
    ''').lower()
            # Exit loop when updating is completed.
            if update_field == "done":
                break

            if update_field in ["id", "qty"]:
            # For id or qty field, ensure input is entered as an integer.
                while True:
                    new_value = input(f"Enter new {update_field}: ")
                    if new_value.isnumeric():
                        new_value = int(new_value)
                        break
                    else:
                        print(f"Enter new {update_field} as an integer.")
            elif update_field in["title", "author"]:
                new_value = input(f"Enter updated {update_field}: ")
            else:
                print("invalid field selection. Please try again")
                continue
                            
            # Commit changes to database.
            with sqlite3.connect('ebookstore.db') as db:
                cursor = db.cursor()
                cursor.execute(f'''UPDATE book SET {update_field} = ? 
                                WHERE id = ?''', (new_value, update_record))
                db.commit()
        # Confirm update and print emended record.
        if update_field != "done":
            print(f'''
The {update_field} of record {update_record} has been updated.''')
            cursor.execute('''SELECT * FROM book
                               WHERE id = ?''', (update_record,))
            updated_record = cursor.fetchone()
            print("Updated record:")
            print(updated_record)
            print("\n", "-"*10) # A border to separate outputs


def delete_book():
    """
    Removes an existing book record from the database based on input ID.
    """
    while True:
        # Ensure ID is entered as an integer.
        delete_id = input("Enter ID of book to delete: ")
        if not delete_id.isnumeric():
            print("Please enter ID as an integer.")
            continue
        delete_id = int(delete_id)

        with sqlite3.connect('ebookstore.db') as db:
            cursor = db.cursor()
            # Check input ID exists in database.
            cursor.execute('''SELECT COUNT(*) FROM book 
                       WHERE id = ?''', (delete_id,))
            if cursor.fetchone()[0] == 0:
                print(f"ID {delete_id} does not match any records.")
            # Delete selected record from database.
            else:
                cursor.execute('''DELETE FROM book WHERE id = ?''', (id))
                db.commit()
                print(f"\nRecord with ID {delete_id} has been deleted.")
                break


def search_books():
    """
    Selects records from the database based on input search field and 
    value (id, title or author).
    """
    while True:
        # Ensure valid field input.
        search_field = input("\nSearch by field (id/title/author): ").lower()
        if search_field in ["id", "title", "author"]:
            break
        else:
            print("\nInvalid field. Please try again.")
    
    # Ensure numeric input for ID.
    if search_field == "id":
        while True:
            search_value = input("\nSearch for ID: ")
            if search_value.isnumeric():
                search_value = int(search_value)
                break
            else:
                print("Enter search ID as an integer.")

    elif search_field in ["title", "author"]:
        search_value = input(f"\nSearch for {search_field}: ")

    # Retrieve results matching search inputs.
    with sqlite3.connect('ebookstore.db') as db:
        cursor = db.cursor()
        cursor.execute(f'''SELECT * FROM book 
                       WHERE {search_field} = ?''', (search_value,))
        results = cursor.fetchall()

        # Display any records matching search criteria.
        if results:
            print("\nSearch results:")
            for result in results:
                print("\n", result)
            print("\n", "-"*10) # A border to separate outputs.
        else:
            print("\nNo results found.")
            print("\n", "-"*10) # A border to separate outputs.

    
# ---------- MAIN PROGRAM ----------
    
# Create and populate database if it does not already exist.
create_database()
populate_database()

# Provide options menu for user.
while True:
    user_choice = input('''\nWould you like to:
    1. Enter book
    2. Update book
    3. Delete book
    4. Search books
    0. Exit                                        

    Enter selection: ''')
       
    if user_choice.isnumeric():
        user_choice = int(user_choice)
    else:
        print("Incorrect input - please enter selection as an integer.\n")
        print("-"*10) # A border to separate outputs.
        continue

    if user_choice == 1:
        enter_book()
    elif user_choice == 2:
        update_book()
    elif user_choice == 3:
        delete_book()
    elif user_choice == 4:
        search_books()
    elif user_choice == 0:
        print("\nGoodbye.\n", "-"*10)
        break
    else:
        print("Invalid selection - please try again.")
