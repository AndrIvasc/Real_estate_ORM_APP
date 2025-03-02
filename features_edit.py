from db import session, Owner, Property, Address, Agency, City, Listing


def edit_owner():
    """
    Edits an existing owner's details (first name, last name, phone number).
    """
    print("\n--- Edit Owner ---")

    # Fetch all owners
    owners = session.query(Owner).all()
    if not owners:
        print("No owners found.")
        return

    # Display available owners
    for owner in owners:
        print(f"Owner ID: {owner.owner_id}, Name: {owner.first_name} {owner.last_name}, Phone: {owner.phone_number}")

    # Select an owner by ID
    owner_id = input("Enter the ID of the owner to edit: ")
    selected_owner = session.query(Owner).filter_by(owner_id=owner_id).first()
    if not selected_owner:
        print("Owner not found.")
        return

    # Prompt for new values (keep old values if input is empty)
    new_first_name = input(
        f"Enter new first name (current: {selected_owner.first_name}): ") or selected_owner.first_name
    new_last_name = input(f"Enter new last name (current: {selected_owner.last_name}): ") or selected_owner.last_name
    new_phone = input(
        f"Enter new phone number (current: {selected_owner.phone_number}): ") or selected_owner.phone_number

    # Update and commit changes
    selected_owner.first_name = new_first_name
    selected_owner.last_name = new_last_name
    selected_owner.phone_number = new_phone
    session.commit()
    print("Owner updated successfully!")


def edit_property():
    """
    Edits an existing property's details (area and registry number).
    """
    print("\n--- Edit Property ---")

    # Fetch all properties
    properties = session.query(Property).all()
    if not properties:
        print("No properties found.")
        return

    # Display available properties
    for property in properties:
        print(
            f"Property ID: {property.property_id}, Registry Number: {property.registry_number}, Area: {property.area_sqm} sqm")

    # Select a property by ID
    property_id = input("Enter the ID of the property to edit: ")
    selected_property = session.query(Property).filter_by(property_id=property_id).first()
    if not selected_property:
        print("Property not found.")
        return

    # Prompt for new values
    new_area = input(f"Enter new area (current: {selected_property.area_sqm} sqm): ") or selected_property.area_sqm
    new_registry_number = input(
        f"Enter new registry number (current: {selected_property.registry_number}): ") or selected_property.registry_number

    # Update and commit changes
    selected_property.area_sqm = float(new_area)
    selected_property.registry_number = new_registry_number
    session.commit()
    print("Property updated successfully!")


def edit_address():
    """
    Edits an existing address, including street address, postal code, and city.
    """
    print("\n--- Edit Address ---")

    # Fetch all addresses
    addresses = session.query(Address).all()
    if not addresses:
        print("No addresses found.")
        return

    # Display available addresses
    for address in addresses:
        city_name = session.query(City).filter_by(city_id=address.city_id).first().name
        print(
            f"Address ID: {address.address_id}, Street: {address.street_address}, City: {city_name}, Postal Code: {address.postal_code}")

    # Select an address by ID
    address_id = input("Enter the ID of the address to edit: ")
    selected_address = session.query(Address).filter_by(address_id=address_id).first()
    if not selected_address:
        print("Address not found.")
        return

    # Prompt for new values
    new_street = input(
        f"Enter new street address (current: {selected_address.street_address}): ") or selected_address.street_address
    new_postal = input(
        f"Enter new postal code (current: {selected_address.postal_code}): ") or selected_address.postal_code
    new_city = input(
        f"Enter new city name (current: {session.query(City).filter_by(city_id=selected_address.city_id).first().name}): ")

    # Update city if provided
    if new_city:
        city = session.query(City).filter_by(name=new_city).first()
        if not city:
            city = City(name=new_city)
            session.add(city)
            session.commit()
            print(f"City '{new_city}' added to the database.")
        selected_address.city_id = city.city_id

    # Update and commit changes
    selected_address.street_address = new_street
    selected_address.postal_code = new_postal
    session.commit()
    print("Address updated successfully!")


def edit_listing():
    """
    Edits an existing listing by modifying sale price and rental price.
    """
    print("\n--- Edit Listing ---")

    # Fetch all listings
    listings = session.query(Listing).all()
    if not listings:
        print("No listings found.")
        return

    # Display available listings
    for listing in listings:
        print(
            f"Listing ID: {listing.listing_id}, Property ID: {listing.property_id}, Agency ID: {listing.agency_id}, Sale Price: {listing.sale_price}, Rental Price: {listing.rental_price}")

    # Select a listing by ID
    listing_id = input("Enter the ID of the listing to edit: ")
    selected_listing = session.query(Listing).filter_by(listing_id=listing_id).first()
    if not selected_listing:
        print("Listing not found.")
        return

    # Prompt for new values
    new_sale_price = input(
        f"Enter new sale price (current: {selected_listing.sale_price}): ") or selected_listing.sale_price
    new_rental_price = input(
        f"Enter new rental price (current: {selected_listing.rental_price}): ") or selected_listing.rental_price

    # Update and commit changes
    selected_listing.sale_price = float(new_sale_price) if new_sale_price else None
    selected_listing.rental_price = float(new_rental_price) if new_rental_price else None
    session.commit()
    print("Listing updated successfully!")


def edit_agency():
    """
    Edits an existing agency's name and company code.
    """
    print("\n--- Edit Agency ---")

    # Fetch all agencies
    agencies = session.query(Agency).all()
    if not agencies:
        print("No agencies found.")
        return

    # Display available agencies
    for agency in agencies:
        print(f"Agency ID: {agency.agency_id}, Name: {agency.name}, Company Code: {agency.company_code}")

    # Select an agency by ID
    agency_id = input("Enter the ID of the agency to edit: ")
    selected_agency = session.query(Agency).filter_by(agency_id=agency_id).first()
    if not selected_agency:
        print("Agency not found.")
        return

    # Prompt for new values
    new_name = input(f"Enter new agency name (current: {selected_agency.name}): ") or selected_agency.name
    new_company_code = input(
        f"Enter new company code (current: {selected_agency.company_code}): ") or selected_agency.company_code

    # Update and commit changes
    selected_agency.name = new_name
    selected_agency.company_code = new_company_code
    session.commit()
    print("Agency updated successfully!")


def edit_city():
    """
    Edits an existing city's name.
    """
    print("\n--- Edit City ---")

    # Fetch all cities
    cities = session.query(City).all()
    if not cities:
        print("No cities found.")
        return

    # Display available cities
    for city in cities:
        print(f"City ID: {city.city_id}, Name: {city.name}")

    # Select a city by ID
    city_id = input("Enter the ID of the city to edit: ")
    selected_city = session.query(City).filter_by(city_id=city_id).first()
    if not selected_city:
        print("City not found.")
        return

    # Prompt for new name
    new_name = input(f"Enter new city name (current: {selected_city.name}): ") or selected_city.name

    # Update and commit changes
    selected_city.name = new_name
    session.commit()
    print("City updated successfully!")
