from db import session, Owner, Property, Address, Agency, City, Listing
from sqlalchemy.sql import func


def search_properties_by_city():
    """
    Searches for properties in a specified city and displays relevant details.
    Includes:
    - Property ID
    - Registry Number
    - Address & Postal Code
    - Average Sale & Rental Prices
    """
    print("\n--- Search Properties by City ---")
    city_name = input("Enter the city name to search: ").strip()

    # Validate city existence
    city = session.query(City).filter_by(name=city_name).first()
    if not city:
        print(f"No city found with the name '{city_name}'.")
        return

    # Query properties in the city with average sale/rental prices
    results = (session.query(Property.property_id,
                             Property.registry_number,
                             Property.area_sqm,
                             Address.street_address,
                             Address.postal_code,
                             func.avg(Listing.sale_price).label("average_sale_price"),
                             func.avg(Listing.rental_price).label("average_rental_price"))
               .join(Address, Property.address_id == Address.address_id)
               .join(Listing, Property.property_id == Listing.property_id)
               .filter(Address.city_id == city.city_id)
               .group_by(Property.property_id)
               .all())

    if not results:
        print(f"No properties found in '{city_name}'.")
        return

    # Display search results
    print(f"\nProperties in '{city_name}':")
    for property in results:
        price_per_sqm = (f"{round(property.average_sale_price / property.area_sqm, 2)} per sqm"
                         if property.average_sale_price and property.area_sqm > 0
                         else "N/A")

        print(f"Property ID: {property.property_id}, Registry Number: {property.registry_number}\n"
              f"  Address: {property.street_address}, Postal Code: {property.postal_code}\n"
              f"  Average Sale Price: {property.average_sale_price or 'N/A'} || ({price_per_sqm})\n"
              f"  Average Rental Price: {property.average_rental_price or 'N/A'}\n")


def view_prices_by_registry_number():
    """
    Displays property details and listing prices based on a given registry number.
    Includes:
    - Property Address & City
    - Area (sqm)
    - Sale & Rental Prices per Agency
    """
    print("\n--- View Property Prices by Registry Number ---")

    registry_number = input("Enter the property registry number: ").strip()

    # Query property details by registry number
    property_data = (session.query(Property.property_id,
                                   Property.registry_number,
                                   Property.area_sqm,
                                   Address.street_address,
                                   City.name.label("city"))
                     .join(Address, Property.address_id == Address.address_id)
                     .join(City, Address.city_id == City.city_id)
                     .filter(Property.registry_number == registry_number)
                     .first())

    if not property_data:
        print(f"No property found with registry number '{registry_number}'.")
        return

    # Display property details
    print(f"\nProperty Details:")
    print(f"  Registry Number: {property_data.registry_number}")
    print(f"  Address: {property_data.street_address}, City: {property_data.city}")
    print(f"  Area: {property_data.area_sqm} sqm")

    # Fetch listing prices from agencies
    listings = (session.query(Listing.sale_price, Listing.rental_price, Agency.name.label("agency_name"))
                .join(Agency, Listing.agency_id == Agency.agency_id)
                .filter(Listing.property_id == property_data.property_id)
                .all())

    if not listings:
        print("No listings available for this property.")
        return

    # Display listing details
    print("\nPrices at Different Agencies:")
    for listing in listings:
        sale_price = listing.sale_price if listing.sale_price else "N/A"
        rental_price = listing.rental_price if listing.rental_price else "N/A"

        price_per_sqm = (f"{round(listing.sale_price / property_data.area_sqm, 2)} per sqm"
                         if listing.sale_price and property_data.area_sqm > 0
                         else "N/A")

        print(f"  Agency: {listing.agency_name}")
        print(f"    Sale Price: {sale_price} || ({price_per_sqm})")
        print(f"    Rental Price: {rental_price}")


def advanced_search():
    """
    Allows searching for properties based on city and price range.
    User can enter:
    - Min/Max Sale Price
    - Min/Max Rental Price
    - City Name
    """
    print("\n--- Advanced Property Search ---")

    city_name = input("Enter the city name to search: ").strip()

    # Validate city existence
    city = session.query(City).filter_by(name=city_name).first()
    if not city:
        print(f"No city found with the name '{city_name}'.")
        return

    # Get optional price filters
    min_sale_price = input("Enter minimum sale price (leave blank for no minimum): ").strip()
    max_sale_price = input("Enter maximum sale price (leave blank for no maximum): ").strip()
    min_rental_price = input("Enter minimum rental price (leave blank for no minimum): ").strip()
    max_rental_price = input("Enter maximum rental price (leave blank for no maximum): ").strip()

    min_sale_price = float(min_sale_price) if min_sale_price else None
    max_sale_price = float(max_sale_price) if max_sale_price else None
    min_rental_price = float(min_rental_price) if min_rental_price else None
    max_rental_price = float(max_rental_price) if max_rental_price else None

    # Query properties matching criteria
    results = (session.query(Property.property_id,
                             Property.registry_number,
                             Property.area_sqm,
                             Address.street_address,
                             City.name.label("city"),
                             func.min(Listing.sale_price).label("cheapest_sale_price"),
                             func.min(Listing.rental_price).label("cheapest_rental_price"))
               .join(Address, Property.address_id == Address.address_id)
               .join(City, Address.city_id == City.city_id)
               .join(Listing, Property.property_id == Listing.property_id)
               .filter(Address.city_id == city.city_id)
               .filter((Listing.sale_price >= min_sale_price if min_sale_price is not None else True) &
                       (Listing.sale_price <= max_sale_price if max_sale_price is not None else True) &
                       (Listing.rental_price >= min_rental_price if min_rental_price is not None else True) &
                       (Listing.rental_price <= max_rental_price if max_rental_price is not None else True))
               .group_by(Property.property_id)
               .all())

    if not results:
        print(f"No properties found in '{city_name}' matching the specified criteria.")
        return

    # Display results
    print(f"\nProperties in '{city_name}' matching your criteria:")
    for property in results:
        cheapest_sale = property.cheapest_sale_price if property.cheapest_sale_price else "N/A"
        cheapest_rental = property.cheapest_rental_price if property.cheapest_rental_price else "N/A"

        print(
            f"Property ID: {property.property_id}, Registry Number: {property.registry_number}\n"
            f"  Address: {property.street_address}\n"
            f"  Cheapest Sale Price: {cheapest_sale}\n"
            f"  Cheapest Rental Price: {cheapest_rental}\n"
        )


from db import session, Owner, Property, Address, Agency, City, Listing
from sqlalchemy.sql import func


def show_all_owners_with_properties():
    """
    Displays all owners and their associated properties.

    Includes:
    - Owner Name & Phone Number
    - List of Properties (Registry Number, Address, City, Area)
    """
    print("\n--- All Owners and Their Properties ---")

    # Query all owners with their associated properties, addresses, and cities
    owners = (
        session.query(Owner, Property, Address, City)
        .join(Property, Owner.owner_id == Property.owner_id)
        .join(Address, Property.address_id == Address.address_id)
        .join(City, Address.city_id == City.city_id)
        .all()
    )

    if not owners:
        print("No owners or properties found.")
        return

    owner_properties = {}

    # Organizing data by owner
    for owner, property, address, city in owners:
        if owner.owner_id not in owner_properties:
            owner_properties[owner.owner_id] = {
                "owner_name": f"{owner.first_name} {owner.last_name}",
                "phone_number": owner.phone_number,
                "properties": []
            }
        owner_properties[owner.owner_id]["properties"].append({
            "registry_number": property.registry_number,
            "street_address": address.street_address,
            "city": city.name,
            "area_sqm": property.area_sqm
        })

    # Display all owners and their properties
    for owner_id, owner_info in owner_properties.items():
        print(f"\nOwner ID: {owner_id}, Name: {owner_info['owner_name']}, Phone: {owner_info['phone_number']}")
        print("  Properties:")
        for property in owner_info["properties"]:
            print(f"    Registry Number: {property['registry_number']}")
            print(f"      Address: {property['street_address']}, City: {property['city']}")
            print(f"      Area: {property['area_sqm']} sqm")


def show_all_properties_by_agency():
    """
    Displays all properties managed by real estate agencies.

    Includes:
    - Agency Name
    - List of Properties (Registry Number, Address, City, Sale & Rental Prices)
    """
    print("\n--- All Properties by Agency ---")

    # Query all agencies along with their listed properties
    agencies = (session.query(Agency, Property, Address, City, Listing.sale_price, Listing.rental_price)
                .join(Listing, Agency.agency_id == Listing.agency_id)
                .join(Property, Listing.property_id == Property.property_id)
                .join(Address, Property.address_id == Address.address_id)
                .join(City, Address.city_id == City.city_id)
                .all())

    if not agencies:
        print("No agencies or properties found.")
        return

    agency_properties = {}

    # Organizing data by agency
    for agency, property, address, city, sale_price, rental_price in agencies:
        if agency.agency_id not in agency_properties:
            agency_properties[agency.agency_id] = {
                "agency_name": agency.name,
                "properties": []
            }
        agency_properties[agency.agency_id]["properties"].append({
            "registry_number": property.registry_number,
            "street_address": address.street_address,
            "city": city.name,
            "area_sqm": property.area_sqm,
            "sale_price": sale_price,
            "rental_price": rental_price,
            "price_per_sqm": (round(sale_price / property.area_sqm, 2)
                              if sale_price and property.area_sqm > 0 else "N/A"),
        })

    # Display all agencies and their listed properties
    for agency_id, agency_info in agency_properties.items():
        print(f"\nAgency: {agency_info['agency_name']} (ID: {agency_id})")
        print("  Properties:")
        for property in agency_info["properties"]:
            print(f"    Registry Number: {property['registry_number']}")
            print(f"      Address: {property['street_address']}, City: {property['city']}")
            print(f"      Area: {property['area_sqm']} sqm")
            print(f"      Sale Price: {property['sale_price'] or 'N/A'} || ({property['price_per_sqm']} per sqm)")
            print(f"      Rental Price: {property['rental_price'] or 'N/A'}")


def show_all_properties():
    """
    Displays all properties in the database.

    Includes:
    - Registry Number
    - Address & City
    - Area (sqm)
    - Minimum Sale Price & Rental Price
    - Sale Price per Square Meter (if applicable)
    """
    print("\n--- All Properties ---")

    # Query all properties with their associated address, city, and price details
    properties = (session.query(Property,
                                Address,
                                City,
                                func.min(Listing.sale_price).label("sale_price"),
                                func.min(Listing.rental_price).label("rental_price"))
                  .join(Address, Property.address_id == Address.address_id)
                  .join(City, Address.city_id == City.city_id)
                  .outerjoin(Listing, Property.property_id == Listing.property_id)
                  .group_by(Property.property_id)
                  .all())

    if not properties:
        print("No properties found.")
        return

    # Display all properties
    for property, address, city, sale_price, rental_price in properties:
        price_per_sqm = (f"{round(sale_price / property.area_sqm, 2)} per sqm"
                         if sale_price and property.area_sqm > 0
                         else "N/A")

        print(f"\nRegistry Number: {property.registry_number}")
        print(f"  Address: {address.street_address}, City: {city.name}, Postal Code: {address.postal_code}")
        print(f"  Area: {property.area_sqm} sqm")
        print(f"  Sale Price: {sale_price or 'N/A'} || ({price_per_sqm})")
        print(f"  Rental Price: {rental_price or 'N/A'}")
