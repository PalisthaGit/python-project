import requests


def get_all_users():
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    if response.status_code == 200:
        return response.json()
    return None


def get_user(user_id):
    response = requests.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
    if response.status_code == 200:
        return response.json()
    return None


def list_users():
    users = get_all_users()
    if users:
        for user in users:
            print(f"{user['id']}. {user['name']} - {user['email']}")
    else:
        print("Could not get users.")


def find_user():
    user_id = input("Enter the user ID: ")
    user = get_user(user_id)
    if user:
        print(f"Name: {user['name']}")
        print(f"Email: {user['email']}")
        print(f"Phone: {user['phone']}")
        print(f"City: {user['address']['city']}")
    else:
        print("User not found.")


def search_users():
    text = input("Enter the name to search: ")
    users = get_all_users()
    found = False
    if users:
        for user in users:
            if text.lower() in user["name"].lower():
                print(f"{user['id']}. {user['name']} - {user['email']}")
                found = True
    if not found:
        print("No users found.")


def main():
    while True:
        print("\n1. List all users")
        print("2. Find user by ID")
        print("3. Search users by name")
        print("4. Quit")

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            list_users()
        elif choice == "2":
            find_user()
        elif choice == "3":
            search_users()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Please choose a number from 1 to 4.")


main()