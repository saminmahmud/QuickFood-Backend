# QuickFood - Online Food Delivery System

QuickFood is an online food delivery system that allows users to browse restaurants, view menus, place orders, and track their delivery status. Restaurant owners can manage their menus and view orders. The system implements JWT authentication and role-based access control to ensure secure access for both users and restaurant owners.

## Features

### 1. Authentication and Authorization
- **JWT Authentication**: Both users and restaurant owners authenticate using JSON Web Tokens (JWT) to ensure secure access.
- **Role-Based Access Control**:
  - **Restaurant Owner Role**: Full access to manage menus and view orders.
  - **User Role**: Limited access to browse restaurants, place orders, and track delivery status.

### 2. Restaurant and Menu Management (Restaurant Owner Only)
Restaurant owners have full control over the restaurant and menu information:
- **CRUD Operations**:
  - **Create**: Add new restaurants and menus (e.g., name, description, location, menu items).
  - **Read**: View all restaurant and menu details.
  - **Update**: Modify restaurant and menu details.
  - **Delete**: Remove restaurants and menus from the system.

### 3. Order Placement and Tracking (User)
Users can browse restaurants, view menus, place orders, and track deliveries:
- **Browse Restaurants**: View a list of restaurants with details such as name, description, and location.
- **View Menu**: See the menu of a selected restaurant, including item names, descriptions, and prices.
- **Place Order**: Place an order by selecting items and specifying quantities.
- **Order Confirmation**: Receive an order confirmation with restaurant name, items, and total cost.
- **Track Delivery**: Track the status of the order (Preparing, Out for Delivery, Delivered).

## System Logic

### 1. Role-Based Permissions
- Only restaurant owners can perform CRUD operations on restaurants and menus.
- Only users can place orders and track delivery status.

### 2. Order Logic
- **Order Placement**: Ensure users can place orders only if items are available.
- **Order Confirmation**: Prevent order confirmation without payment completion.
- **Delivery Status Update**: Allow restaurant owners to update the delivery status after order confirmation.

### 3. Efficient Querying
- Optimized queries for:
  - Available restaurants and menus for browsing.
  - Order for each user.
  - Delivery status for each order.

## Technology Stack

- **Backend**:
  - Django (Backend framework)
  - Django Rest Framework (DRF)
  - JWT (JSON Web Token for authentication)
  - PostgreSQL (Database)

- **Frontend**:
  - React (Frontend framework)
  - Tailwind CSS (For styling)
  - DaisyUI (Component library)

- **Payment Gateway**: 
  - SSLCOMMERZ payment gateway integrated for order payments.

## Deployment

- **Frontend (Live)**: [https://quick-food-omega.vercel.app/](https://quick-food-omega.vercel.app/)
- **Backend (Live)**: [https://quickfood-backend-3lxu.onrender.com/](https://quickfood-backend-3lxu.onrender.com)

## API Documentation

- **Swagger UI**: [https://quickfood-backend-3lxu.onrender.com/api/schema/swagger-ui/](https://quickfood-backend-3lxu.onrender.com/api/schema/swagger-ui/)
- **Redoc**: [https://quickfood-backend-3lxu.onrender.com/api/schema/redoc/](https://quickfood-backend-3lxu.onrender.com/api/schema/redoc/)

## Setup Backend

### 1. Clone the backend repositories to your local machine.

```bash
git clone https://github.com/saminmahmud/QuickFood-Backend.git
```

### 2. Navigate to the backend folder and install dependencies:

```bash
cd Quickfood-Backend
pip install -r requirements.txt
```
### 3. Set up your database (PostgreSQL) and configure the environment variables in .env.

```bash
SECRET_KEY=
DEBUG=True
STORE_ID=
STORE_PASSWORD=
DATABASE_PUBLIC_URL=
```

### 4. Run database migrations:
```bash
python manage.py migrate
```

### 5. Start the backend server:
```bash
python manage.py runserver
```

**Frontend**: [https://github.com/saminmahmud/QuickFood-Frontend.git](https://github.com/saminmahmud/QuickFood-Frontend.git)
