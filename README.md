# 🏡 Real Estate Management System

A Python-based Real Estate Management System built with SQLAlchemy for managing property owners, properties, agencies, and listings in a structured database.

## 📌 Features

### ➕ Add Functions:
- Add Owners
- Add Properties
- Add Agencies
- Add Listings

### ✏️ Edit Functions:
- Edit Owners (name, phone number)
- Edit Properties (area, registry number, address)
- Edit Agencies (name, company code)
- Edit Listings (sale & rental price)
- Edit Addresses & Cities

### 📖 Read Functions:
- Search Properties by City
- View Property Prices by Registry Number
- Advanced Property Search (filters by city, sale & rental price range)

#### Show All Properties by:
- Agency
- Property Type
- Owners

### ❌ Remove Functions:
- Remove Owners
- Remove Properties
- Remove Listings

## 🛠️ Installation

# Clone the repository
git clone https://github.com/AndrIvasc/Real_estate_ORM_APP.git
cd real-estate-management

# Create and activate a virtual environment
python -m venv venv

# For Mac/Linux:
source venv/bin/activate

# For Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up the database
python db_setup.py

# Run the application
python main.py

## 🏗️ Database Schema

The system uses SQLAlchemy ORM with the following tables:

- **Owners** (id, first name, last name, phone number)
- **Cities** (id, name)
- **Addresses** (id, street, postal code, city_id)
- **Properties** (id, owner_id, address_id, area, registry number)
- **Agencies** (id, name, company code)
- **Listings** (id, property_id, agency_id, sale_price, rental_price)

## 🎯 Usage

- After running `main.py`, navigate through the interactive menu to add, edit, delete, and search properties with ease.

## 💡 Future Improvements

- User authentication to allow different roles (admin, agents, clients)
- GUI version using Flask or Django
- REST API for remote access

## 📜 License

- This project is open-source and available under the MIT License.

## 🙌 Contributing

- Feel free to fork the repository and submit pull requests! 🚀
