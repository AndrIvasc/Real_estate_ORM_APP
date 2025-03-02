from features_add import add_owner, add_property, add_agency, add_listing
from features_edit import edit_owner, edit_agency, edit_listing, edit_city, edit_address, edit_property
from features_read import (search_properties_by_city, view_prices_by_registry_number, advanced_search,
                           show_all_owners_with_properties, show_all_properties_by_agency,
                           show_all_properties)
from features_remove import remove_owner, remove_property, remove_listing


def process_menu():
    """
    The main menu loop that handles user navigation across the system.
    """
    while True:
        main_menu()

        choice = input("Choose an option: ")
        if choice == "1":
            process_menu_add()
        elif choice == "2":
            process_menu_edit()
        elif choice == "3":
            process_menu_remove()
        elif choice == "4":
            process_menu_read()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


def main_menu():
    """
    Displays the main menu options.
    """
    print("\nReal Estate Management System")
    print("1. Add Menu...")
    print("2. Edit Menu...")
    print("3. Remove Menu...")
    print("4. Read Menu...")
    print("5. Exit")


def add_menu():
    """
    Displays the add menu options.
    """
    print("\nAdd Menu:")
    print("1. Add Owner")
    print("2. Add Property")
    print("3. Add Agency")
    print("4. Add Listing")
    print("5. Return to Main Menu")


def edit_menu():
    """
    Displays the edit menu options.
    """
    print("\nEdit Menu:")
    print("1. Edit Owner")
    print("2. Edit Property")
    print("3. Edit Agency")
    print("4. Edit Listing")
    print("5. Edit Address")
    print("6. Edit City")
    print("7. Return to Main Menu")


def remove_menu():
    """
    Displays the remove menu options.
    """
    print("\nRemove Menu:")
    print("1. Remove Owner")
    print("2. Remove Property")
    print("3. Remove Listing")
    print("4. Return to Main Menu")


def read_menu():
    """
    Displays the read menu options.
    """
    print("\nRead Menu:")
    print("1. Search properties by city")
    print("2. View prices by registry number")
    print("3. Advanced search")
    print("4. Show all properties by category")
    print("5. Return to Main Menu")


def show_all_menu():
    """
    Displays the menu for showing all properties by category.
    """
    print("\nShow All Properties by:")
    print("1. Agency")
    print("2. Property")
    print("3. Owners")
    print("4. Return to Read Menu")


def process_all_read():
    """
    Handles the user's selection for viewing all properties by category.
    """
    while True:
        show_all_menu()

        choice = input("Choose an option: ")
        if choice == "1":
            show_all_properties_by_agency()
        elif choice == "2":
            show_all_properties()
        elif choice == "3":
            show_all_owners_with_properties()
        elif choice == "4":
            print("Returning to Read Menu...")
            break
        else:
            print("Invalid choice. Please try again.")


def process_menu_add():
    """
    Handles user actions in the add menu.
    """
    while True:
        add_menu()

        choice = input("Choose an option: ")
        if choice == "1":
            add_owner()
        elif choice == "2":
            add_property()
        elif choice == "3":
            add_agency()
        elif choice == "4":
            add_listing()
        elif choice == "5":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice. Please try again.")


def process_menu_edit():
    """
    Handles user actions in the edit menu.
    """
    while True:
        edit_menu()

        choice = input("Choose an option: ")
        if choice == "1":
            edit_owner()
        elif choice == "2":
            edit_property()
        elif choice == "3":
            edit_agency()
        elif choice == "4":
            edit_listing()
        elif choice == "5":
            edit_address()
        elif choice == "6":
            edit_city()
        elif choice == "7":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice. Please try again.")


def process_menu_remove():
    """
    Handles user actions in the remove menu.
    """
    while True:
        remove_menu()

        choice = input("Choose an option: ")
        if choice == "1":
            remove_owner()
        elif choice == "2":
            remove_property()
        elif choice == "3":
            remove_listing()
        elif choice == "4":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice. Please try again.")


def process_menu_read():
    """
    Handles user actions in the read menu.
    """
    while True:
        read_menu()

        choice = input("Choose an option: ")
        if choice == "1":
            search_properties_by_city()
        elif choice == "2":
            view_prices_by_registry_number()
        elif choice == "3":
            advanced_search()
        elif choice == "4":
            process_all_read()
        elif choice == "5":
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice. Please try again.")
