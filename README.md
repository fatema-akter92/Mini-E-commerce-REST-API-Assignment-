# Mini E-commerce REST API

A production-ready RESTful API for an E-commerce platform built using **Django** and **Django REST Framework (DRF)**.

---

## Backend Key Features

1. **Category API**: Full CRUD operations for managing product categories.
2. **Product API**: Full CRUD operations for products with price, stock, category relationship, and images.
3. **Product Filtering & Searching**:
   - Search by name & description (`/api/products/?search=phone`)
   - Filter by category (`/api/products/?category=1`)
   - Filter by price range (`/api/products/?min_price=100&max_price=500`)
   -  Order by price (`/api/products/?ordering=price` or `/api/products/?ordering=-price`)
   -  Page-number pagination (10 items per page)
4. **User Authentication**:
   - Token-based authentication (`rest_framework.authtoken`)
   - User Registration (`/api/auth/register/`), Login (`/api/auth/login/`), Logout (`/api/auth/logout/`), and User Profile (`/api/auth/user/`)
5. **Order API**:
   - Logged-in users can place orders (`/api/orders/`).
   -  **Stock Validation & Auto-Deduction**: Validates stock prior to order creation and automatically decrements inventory.
   -  Auto-calculated total price based on product unit price $\times$ quantity.
   -  User isolation: Customers can only access their own order history.

---

##  Project Structure

```
mini_ecommerce_api/
├── manage.py
├── requirements.txt
├── postman_collection.json
├── README.md
├── ecommerce/                # Core Django configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── store/                    # E-commerce application module
    ├── models.py             # Category, Product, Order, Review
    ├── serializers.py        # DRF Serializers & Validation logic
    ├── views.py              # ViewSets & Auth APIViews
    ├── permissions.py        # IsAdminOrReadOnly & IsOrderOwner permissions
    ├── filters.py            # Product search & filtering backends
    ├── pagination.py         # Standard results set pagination
    ├── urls.py               # API route definitions
    └── tests/                # Automated test suite
        ├── test_auth.py
        ├── test_categories.py
        ├── test_products.py
        └── test_orders.py
```

---


The server will start at `http://127.0.0.1:8000/`.

---



## API Endpoints Quick Reference

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register/` | Register new user & receive token | ❌ No |
| `POST` | `/api/auth/login/` | Obtain token using username & password | ❌ No |
| `POST` | `/api/auth/logout/` | Revoke current user auth token | YES (Token) |
| `GET` | `/api/auth/user/` | Get current authenticated user info | YES (Token) |
| `GET` | `/api/categories/` | List all categories | ❌ No |
| `POST` | `/api/categories/` | Create a category | Admin Only |
| `GET` | `/api/categories/<id>/` | View category details | ❌ No |
| `PUT/PATCH` | `/api/categories/<id>/` | Update a category | Admin Only |
| `DELETE` | `/api/categories/<id>/` | Delete a category | Admin Only |
| `GET` | `/api/products/` | List & filter products | ❌ No |
| `POST` | `/api/products/` | Add a product | Admin Only |
| `GET` | `/api/products/<id>/` | View product details | ❌ No |
| `PUT/PATCH` | `/api/products/<id>/` | Update a product | Admin Only |
| `DELETE` | `/api/products/<id>/` | Delete a product | Admin Only |
| `POST` | `/api/orders/` | Place a new order | YES (Token) |
| `GET` | `/api/orders/` | View user's placed orders | YES (Token) |
| `GET` | `/api/orders/<id>/` | View single order details | YES (Token) |

---

## 💡 Example Queries

### Filtering & Searching Products
- **Search by keyword**: `GET /api/products/?search=phone`
- **Filter by category**: `GET /api/products/?category=1`
- **Filter by price range**: `GET /api/products/?min_price=50.00&max_price=250.00`
- **Order by price (ascending)**: `GET /api/products/?ordering=price`
- **Order by price (descending)**: `GET /api/products/?ordering=-price`

### Header format for Authenticated Requests
```http
Authorization: Token 9944b09199c62bcf9418ad846d3e4007654f3794
```
