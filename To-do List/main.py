# Mini To-Do Manager
# A simple terminal program to add, view and remove tasks.

print("Mini To-Do List")

tasks = []

while True:
    print(f"\nYou have {len(tasks)} task(s)")
    print("1. Add task")
    print("2. View tasks")
    print("3. Remove task")
    print("4. Quit")

    choice = input("\nChoose an option (1-4): ")

    # Add a task
    if choice == "1":
        task = input("Enter a task: ")
        tasks.append(task)
        print(f"{task} added to the list")

    # View all tasks
    elif choice == "2":
        if not tasks:
            print("No tasks yet.")
        else:
            print("Task List:")
            for index, task in enumerate(tasks, start=1):
                print(f"{index}. {task}")

    # Remove a task by its number
    elif choice == "3":
        if not tasks:
            print("No tasks to remove.")
        else:
            task_number = int(input("Enter task number to remove: "))
            if 1 <= task_number <= len(tasks):
                removed = tasks.pop(task_number - 1)
                print(f"Task removed: {removed}")
            else:
                print("That task number doesn't exist.")

    # Quit the program
    elif choice == "4":
        print("Goodbye!")
        break

    # Anything else
    else:
        print("Please choose a number from 1 to 4.")