# Django Warehouse Management System

## Short Description
This Django application is warehouse management system that allows users to manage products, suppliers, and categories. It also handles inbound and outbound product movements and maintains the quantity of products in the inventory. Additionally, the warehouse management system also provides user management operations based on user roles.

## Use Cases
1. **Product Management**: Warehouse managers can add, update, and view products in the inventory.
2. **Supplier Management**: Warehouse managers can add suppliers.
3. **Category Management**: Warehouse managers can add product categories.
4. **Inbound Management**: Warehouse managers and operators can add inbound product movements, which increases the quantity of a product in the inventory.
5. **Outbound Management**: Warehouse managers and operators can add outbound product movements, which decreases the quantity of a product in the inventory.
6. **User Management**: Admin and warehouse managers can register new users with specific roles.

## How to Run Locally
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required packages using:
```
pip install -r requirements.txt
```
4. Run the migrations:
```
python manage.py makemigrations
```
```
python manage.py migrate
```
5. Create a superuser:
```
python manage.py createsuperuser
```
6. Run the server:
```
python manage.py runserver
```
7. Open your web browser and navigate to `http://127.0.0.1:8000/admin`.
8. Assign Warehouse manager role to superuser in the UserProfile table through the admin panel.
9. Navigate to `http://127.0.0.1:8000/` to access the system interface.
