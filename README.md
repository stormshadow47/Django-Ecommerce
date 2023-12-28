# Django-Ecommerce
A Django-based Ecommerce platform designed for easy setup, user management, product listings, and order processing.

## Overview
This project is structured to include the following functionalities:

### User Functionalities:
- **User Authentication:** Users can register, log in, and manage their accounts.
- **Product Listing:** Browse and view available products.
- **Shopping Cart:** Add, update, and remove items from the cart.
- **Order Creation:** Place orders for selected items.

### Admin Functionalities:
- **Admin Authentication:** Admins can log in using JWT authentication to access the admin dashboard.
- **Product Management:** Perform CRUD operations for products (add, update, delete).
- **Order Management:** View and update order details, including order status.
- **User Management:** View registered users, deactivate or delete user accounts.
- **Category Management:** Manage product categories.
- **Email Notifications:** Send custom email notifications to users (order updates, promotional emails).

## Project Structure
### Apps
- **Users:** Manages user-related functionalities (registration, login, authentication).
- **Products:** Handles product-related functionalities (listing, management).
- **Cart:** Handles addition of products to shopping cart and displays individual and the total price.
- **Orders:** Manages order creation and management.

## Usage
1. **Installation**: Clone the repository and install the required dependencies.
```
git clone https://github.com/stormshadow47/Django-Ecommerce.git
cd ecom_project
pip install -r requirements.txt
```
2. **Enter Virtual Environment inside the project:**


```
.\ecom\Scripts\activate
```


3. **Running the server**: Run the Django development server.
```
python manage.py runserver
```

4. **Admin Dashboard:** Access the admin dashboard using your browser. Use admin credentials for authentication.
```
http://localhost:8000/admin/
```

# API Endpoints

## Project Level:
- 'api/users/' : User-related endpoints (registration, login, profile).
- 'api/products/' : Product-related endpoints (listing, details, creation).
- 'api/cart/' : Endpoints for cart-related functionalities(Adding products to cart, total price and checkout).
- 'api/orders/' : Order-related endpoints (creation, listing, details, status update).
  
## App Level:
### Users:
 **Admin:**
- 'admin/login/' (Admin login)
- 'admin/logout/' (Admin logout)
- 'admin/userlist/' (Admin display user list)
- 'admin/users/<int:user_id>/' (Admin display individual user detail)
- 'admin/send_custom_email/' (Admin send custom emails: order updates, promotions)

**User:**
- 'register/' (User account registration)
- 'login/' (User login)
- 'logout/' (user logout)
- 'password_reset/' (User password reset request)
- 'password_reset_confirm/uidb64/token/' (User password reset confirm)
- 'set_new_password/uidb64/token/' (User set new password)

### Products:
**Admin:**
- 'create/' (Admin create products)
- '<int:pk>/update/' (Admin update product details)
- '<int:pk>/delete/' (Admin delete product details)
- 'categories/' (Admin product category list view)
- 'categories/create/' (Admin create product category)
- 'categories/<int:pk>/' (Admin update product category)
- 'categories/<int:pk>/delete/' (Admin delete product category)

**User:**
- 'listview/' (User proudct list view)
- '<int:pk>/' (User product detail view)
- '<int:product_id>/reviews/' (User product review list)
- 'reviews/<int:review_id>/ (User product review detail)

## Cart:
**User:**
- 'view/<int:pk>/' (User cart list view)
- 'item/add/' (User add product to cart)
- 'item/update/<int:pk>/' (User update product in cart. example: quantity)
- 'delete/<int:pk>/' (User delete product from cart)

## Order:
**Admin:**
- 'listview/', (Admin list order history)
- 'detailview/<int:pk>/', (Admin list individiual order)
- 'status/<int:pk>/update/' (Admin update order status )

**User:**
- 'create/' (User place order)
- 'history/' (User list order history)
