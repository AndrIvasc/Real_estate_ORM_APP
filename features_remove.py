from db import session, Owner, Property, Address, Agency, City, Listing


def remove_owner():
    """
    Owner record is removed with coresponding property and address records.
    """
    print("\n--- Remove Owner ---")
    owners = session.query(Owner).all()
    if not owners:
        print("No owners found.")
        return

    for owner in owners:
        print(f"Owner ID: {owner.owner_id}, Name: {owner.first_name} {owner.last_name}")

    owner_id = input("Enter the ID of the owner to remove: ")
    selected_owner = session.query(Owner).filter_by(owner_id=owner_id).first()
    if not selected_owner:
        print("Owner not found.")
        return

    properties = session.query(Property).filter_by(owner_id=owner_id).all()
    for property in properties:
        session.query(Listing).filter_by(property_id=property.property_id).delete()
        session.query(Address).filter_by(address_id=property.address_id).delete()
        session.delete(property)

    session.delete(selected_owner)
    session.commit()
    print("Owner and all associated properties removed successfully!")


def remove_property():
    """
    Removes property record with address. City record is left.
    """
    print("\n--- Remove Property ---")
    properties = session.query(Property).all()
    if not properties:
        print("No properties found.")
        return

    for property in properties:
        print(f"Property ID: {property.property_id}, Registry Number: {property.registry_number}")

    property_id = input("Enter the ID of the property to remove: ")
    selected_property = session.query(Property).filter_by(property_id=property_id).first()
    if not selected_property:
        print("Property not found.")
        return

    session.query(Listing).filter_by(property_id=property_id).delete()

    session.query(Address).filter_by(address_id=selected_property.address_id).delete()

    session.delete(selected_property)
    session.commit()
    print("Property and associated listings removed successfully!")


def remove_listing():
    """
    Listing record is removed.
    """
    print("\n--- Remove Listing ---")
    listings = session.query(Listing).all()
    if not listings:
        print("No listings found.")
        return

    for listing in listings:
        print(f"Listing ID: {listing.listing_id}, Property ID: {listing.property_id}, Agency ID: {listing.agency_id}")

    listing_id = input("Enter the ID of the listing to remove: ")
    selected_listing = session.query(Listing).filter_by(listing_id=listing_id).first()
    if not selected_listing:
        print("Listing not found.")
        return

    session.delete(selected_listing)
    session.commit()
    print("Listing removed successfully!")