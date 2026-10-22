# Contact Book (with functions)

A command-line contact book built with Python. Each action is its own function, so the code is easy to read and reuse.

## Features
- Add a contact (name and phone)
- View all contacts (numbered)
- Search a contact by name (ignores capital letters)
- Update a contact's name, phone, or both (leave blank to keep the current value)
- Delete a contact by name
- Friendly messages when a contact is not found

## How it works
Contacts are stored in a list of dictionaries:

```python
contacts = [
    {"name": "Ram", "phone": "9800000000"},
    {"name": "Sita", "phone": "9811111111"},
]
```

The `find_contact(name)` function is shared by Search, Update and Delete, so the search logic is written only once.

## Concepts used
Functions, parameters and return values, lists of dictionaries, `while` and `for` loops, `enumerate()`, `if/elif/else`, string methods (`.lower()`), f-strings

## How to run
1. Install Python 3
2. Download `contact_book.py`
3. Open a terminal in that folder and run:

```
   python contact_book.py
```

## Example

```
1. Add contact
2. View contacts
3. Search contact
4. Delete contact
5. Update contact
6. Quit

Enter your choice (1-6): 1
Enter the name: Ram
Enter the phone: 9800000000
Contact added.
```

## Possible improvements
- Save contacts to a file so they are not lost when the program closes
- Turn this into a web API with FastAPI