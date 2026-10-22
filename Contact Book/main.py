# Contact Book 
print("Contact Book")

contacts = []


def add_contact():
    name = input("Enter the name: ")
    phone = input("Enter the phone: ")
    contact = {"name": name, "phone": phone}
    contacts.append(contact)
    print("Contact added.")


def view_contacts():
    if not contacts:
        print("No contacts yet.")
    else:
        for index, contact in enumerate(contacts, start=1):
            print(f"{index}. {contact['name']} - {contact['phone']}")


def find_contact(name):
    for contact in contacts:
        if name.lower() == contact["name"].lower():
            return contact
    return None


def search_contact():
    name = input("Enter the name to find: ")
    contact = find_contact(name)
    if contact:
        print(f"{contact['name']} - {contact['phone']}")
    else:
        print("Contact not found.")


def delete_contact():
    name = input("Enter the contact name to delete: ")
    contact = find_contact(name)
    if contact:
        contacts.remove(contact)
        print("Contact deleted.")
    else:
        print("Contact not found.")


def main():
    while True:
        print("\n1. Add contact")
        print("2. View contacts")
        print("3. Search contact")
        print("4. Delete contact")
        print("5. Quit")

        choice = input("\nEnter your choice (1-5): ")

        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Please choose a number from 1 to 5.")


main()