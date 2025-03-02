from db import session, Owner, Property, Address, Agency, City, Listing


def add_owner():
    """
    Adds a new owner to the database and optionally allows adding a property for them.
    """
    print("\n--- Add a New Owner ---")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    phone = input("Enter phone number: ")

    # Create and save a new owner
    owner = Owner(first_name=first_name, last_name=last_name, phone_number=phone)
    session.add(owner)
    session.commit()
    print("Owner added successfully.")

    # Optionally add a property for the newly added owner
    while True:
        add_property_prompt = input("Do you want to add a property for this owner? (yes/no): ").strip().lower()
        if add_property_prompt == "yes":
            add_property(owner.owner_id)
        elif add_property_prompt == "no":
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")


def add_property(owner_id=None):
    """
    Adds a new property to the database. If no owner ID is provided, the user is prompted to select one.
    """
    print("\n--- Add a New Property ---")

    # If owner_id is not provided, prompt the user to choose an existing owner
    if owner_id is None:
        owners = session.query(Owner).all()
        if not owners:
            print("No owners found. Please add an owner first.")
            return

        print("\nAvailable Owners:")
        for owner in owners:
            print(f"Owner ID: {owner.owner_id}, Name: {owner.first_name} {owner.last_name}, Phone: {owner.phone_number}")

        while True:
            try:
                owner_id = int(input("Enter the ID of the owner for this property: "))
                selected_owner = session.query(Owner).filter_by(owner_id=owner_id).first()
                if selected_owner:
                    break
                else:
                    print(f"No owner found with ID {owner_id}. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid numeric Owner ID.")

    # Collect property details
    street_address = input("Enter property street address: ")
    postal_code = input("Enter property postal code: ")
    city_name = input("Enter property city: ")
    area_sqm = float(input("Enter property area (sqm): "))
    registry_number = input("Enter unique property registry number: ")

    # Check if the city already exists, otherwise create a new city entry
    city = session.query(City).filter_by(name=city_name).first()
    if not city:
        city = City(name=city_name)
        session.add(city)
        session.commit()
        print(f"City '{city_name}' added to the database.")

    # Create and save the new address
    address = Address(street_address=street_address, postal_code=postal_code, city_id=city.city_id)
    session.add(address)
    session.commit()
    print(f"Address '{street_address}, {city_name}' added successfully!")

    # Create and save the new property
    property_obj = Property(owner_id=owner_id, address_id=address.address_id, area_sqm=area_sqm,
                            registry_number=registry_number)
    session.add(property_obj)
    session.commit()
    print("Property added successfully!")


def add_agency():
    """
    Adds a new real estate agency to the database.
    """
    print("\n--- Add a New Agency ---")
    name = input("Enter agency name: ")
    company_code = input("Enter agency company code: ")

    # Check if an agency with the same company code already exists
    existing_agency = session.query(Agency).filter_by(company_code=company_code).first()
    if existing_agency:
        print(f"Error: An agency with company code '{company_code}' already exists.")
        return

    # Create and save the new agency
    agency = Agency(name=name, company_code=company_code)
    session.add(agency)
    session.commit()
    print(f"Agency '{name}' added successfully!")


def add_listing():
    """
    Adds a new listing for a property, linking it to an agency.
    """
    print("\n--- Add a New Listing ---")

    # Display available properties for selection
    print("\nAvailable Properties:")
    properties = session.query(Property).all()
    if not properties:
        print("No properties available. Add a property first!")
        return

    for property in properties:
        print(f"Property ID: {property.property_id}, Registry Number: {property.registry_number}, "
              f"Area: {property.area_sqm} sqm")

    # Prompt user to select a property
    property_id = input("Enter the ID of the property for this listing: ")
    selected_property = session.query(Property).filter_by(property_id=property_id).first()
    if not selected_property:
        print(f"Error: No property found with ID {property_id}.")
        return

    # Display available agencies for selection
    print("\nAvailable Agencies:")
    agencies = session.query(Agency).all()
    if not agencies:
        print("No agencies available. Add an agency first!")
        return

    for agency in agencies:
        print(f"Agency ID: {agency.agency_id}, Name: {agency.name}")

    # Prompt user to select an agency
    agency_id = input("Enter the ID of the agency for this listing: ")
    selected_agency = session.query(Agency).filter_by(agency_id=agency_id).first()
    if not selected_agency:
        print(f"Error: No agency found with ID {agency_id}.")
        return

    # Get sale price and rental price (optional)
    sale_price = input("Enter the sale price (leave blank if not for sale): ")
    rental_price = input("Enter the rental price per month (leave blank if not for rent): ")

    # Convert inputs to float or None
    sale_price = float(sale_price) if sale_price.strip() else None
    rental_price = float(rental_price) if rental_price.strip() else None

    # Ensure at least one price is provided
    if sale_price is None and rental_price is None:
        print("Error: You must provide at least one price (sale or rental).")
        return

    # Create and save the new listing
    listing = Listing(
        property_id=selected_property.property_id,
        agency_id=selected_agency.agency_id,
        sale_price=sale_price,
        rental_price=rental_price
    )
    session.add(listing)
    session.commit()
    print("Listing added successfully!")
