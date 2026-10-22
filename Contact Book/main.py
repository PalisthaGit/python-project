# Contact Book
# A simple terminal program to add, view, search and delete contacts.

print("Contact Book")

contacts = []

while True:
    print("\n1. Add contact")
    print("2. View contacts")
    print("3. Search contact")
    print("4. Delete contact")
    print("5. Quit")

    choice = input("\nEnter your choice (1-5): ")

    # Add a contact
    if choice == "1":
        name = input("Enter the name: ")
        phone = input("Enter the phone: ")
        contact = {"name": name, "phone": phone}
        contacts.append(contact)
        print("\nContact was added.")

    # View all contacts
    elif choice == "2":
        if not contacts:
            print("No contacts yet.")
        else:
            print("\nContact List")
            for index, contact in enumerate(contacts, start=1):
                print(f"{index}. {contact['name']} - {contact['phone']}")

    # Search a contact by name (ignores capital letters)
    elif choice == "3":
        name = input("Enter name to search: ")
        found = False
        for contact in contacts:
            if name.lower() == contact["name"].lower():
                found = True
                print(f"{contact['name']} - {contact['phone']}")
                print("Contact found!")
        if not found:
            print("Contact not found.")

    # Delete a contact by name
    elif choice == "4":
        name = input("Enter name to delete: ")
        found = False
        for contact in contacts:
            if contact["name"].lower() == name.lower():
                found = True
                contacts.remove(contact)
                print("Contact deleted.")
                break
        if not found:
            print("Contact not found.")

    # Quit the program
    elif choice == "5":
        print("Goodbye!")
        break

    else:
        print("Please choose a number from 1 to 5.")