# User Viewer

A command-line program that fetches users from a public API ([JSONPlaceholder](https://jsonplaceholder.typicode.com)) using Python and the `requests` library.

## Features
- List all users
- Find a user by ID (name, email, phone, city)
- Search users by name (ignores capital letters)
- Handles failed requests with friendly messages

## Concepts used
HTTP GET requests, status codes, JSON, lists and dictionaries, functions, `while` loops, `if/elif/else`, f-strings

## How to run
1. Install Python 3
2. Install the library:

```
   pip install requests
```

3. Run the program:

```
   python user_viewer.py
```

## Example

```
1. List all users
2. Find user by ID
3. Search users by name
4. Quit

Enter your choice (1-4): 2
Enter the user ID: 3
Name: Clementine Bauch
```