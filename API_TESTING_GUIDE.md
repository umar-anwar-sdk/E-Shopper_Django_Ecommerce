# 🛍️ E-Shopper Complete API Testing Guide

## 📋 Table of Contents
1. [Overview](#overview)
2. [Setup Instructions](#setup-instructions)
3. [Authentication](#authentication)
4. [API Endpoints](#api-endpoints)
5. [Authorization & Roles](#authorization--roles)
6. [Testing Scenarios](#testing-scenarios)
7. [Postman Collection Usage](#postman-collection-usage)

---

## Overview

Complete API documentation for E-Shopper Django e-commerce project with:
- ✅ **JWT Authentication** - Secure token-based auth
- ✅ **Role-Based Authorization** - Admin, Vendor, Customer roles
- ✅ **Protected Product APIs** - Ownership enforcement
- ✅ **Vendor Management** - Brand/shop branding updates
- ✅ **Admin Dashboard** - Complete user/vendor management

**Base URL:** `http://localhost:8001/api`

---

## Setup Instructions

### 1. Start Development Server
```bash
cd /home/umer/Desktop/MY_git/E_Commer/E-Shopper_Django_Ecommerce
source venv/bin/activate
python manage.py runserver 0.0.0.0:8001
```

### 2. Import Collections in Postman
1. Open Postman
2. Click **Import** → **Upload Files**
3. Select both files:
   - `E-Shopper_Complete_API.postman_collection.json` - All API requests
   - `E-Shopper_Development.postman_environment.json` - Environment variables
4. Click **Import**

### 3. Configure Environment
- Select **E-Shopper Development** environment from dropdown
- Credentials are pre-configured:
  - **Admin:** admin@example.com / AdminPass123!@
  - **Vendor:** vendor@example.com / VendorTest123!@
  - **Customer:** customer@example.com / TestPass123!@

---

## Authentication

### 1. Register Customer
```http
POST /auth/register/
Content-Type: application/json

{
  "email": "newcustomer@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "9876543210",
  "password": "SecurePass123!@",
  "confirm_password": "SecurePass123!@"
}

Response: 201 Created
{
  "message": "Customer registered successfully!",
  "user": { ... },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### 2. Login (All Roles)
```http
POST /auth/login/
Content-Type: application/json

{
  "email": "admin@example.com",
  "password": "AdminPass123!@"
}

Response: 200 OK
{
  "message": "Login successful!",
  "user": {
    "id": 1,
    "email": "admin@example.com",
    "role": "admin",
    "first_name": "Admin",
    "last_name": "User"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### 3. Refresh Token
```http
POST /auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response: 200 OK
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 4. Logout
```http
POST /auth/logout/
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response: 200 OK
{
  "message": "Successfully logged out."
}
```

---

## API Endpoints

### 📦 PUBLIC ENDPOINTS (No Auth Required)

#### List All Products
```http
GET /products/
```
Response: 200 OK (Paginated list)
```json
{
  "count": 150,
  "next": "http://localhost:8001/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Product Name",
      "price": 5000,
      "vendor": "Vendor Name",
      "Availability": "In Stock"
    }
  ]
}
```

#### Get Product Detail
```http
GET /products/{id}/
```

#### Search Products
```http
GET /search/?keyword=laptop
```

---

### 🔐 PROTECTED ENDPOINTS (Auth Required)

### Customer Endpoints

#### Get Profile
```http
GET /auth/profile/
Authorization: Bearer {{customer_access_token}}
```

#### Update Profile
```http
PUT /auth/profile/
Authorization: Bearer {{customer_access_token}}
Content-Type: application/json

{
  "first_name": "Updated Name",
  "phone_number": "9999999999"
}
```

#### Get Customer Profile
```http
GET /auth/customer/profile/
Authorization: Bearer {{customer_access_token}}
```

---

### 🏪 VENDOR ENDPOINTS (Vendor Auth Required)

#### Create Product
```http
POST /products/
Authorization: Bearer {{vendor_access_token}}
Content-Type: application/json

{
  "name": "Laptop Pro",
  "details": "High performance laptop",
  "price": 52000,
  "Availability": "In Stock",
  "Condition": "New",
  "category_id": 1,
  "brand_id": 1
}

Response: 201 Created
{
  "id": 10,
  "name": "Laptop Pro",
  "price": 52000,
  "vendor": 2,
  "vendor_name": "Test Shop"
}
```

#### List Own Products
```http
GET /vendor/products/
Authorization: Bearer {{vendor_access_token}}

Response: 200 OK
{
  "count": 5,
  "results": [ ... ]
}
```

#### Update Own Product
```http
PATCH /products/{product_id}/
Authorization: Bearer {{vendor_access_token}}
Content-Type: application/json

{
  "price": 49999,
  "Availability": "In Stock"
}

Response: 200 OK
```

#### Delete Own Product
```http
DELETE /products/{product_id}/
Authorization: Bearer {{vendor_access_token}}

Response: 204 No Content
```

#### Get Vendor Profile
```http
GET /auth/vendor/profile/
Authorization: Bearer {{vendor_access_token}}
```

#### Update Vendor Branding
```http
PATCH /vendor/brand/
Authorization: Bearer {{vendor_access_token}}
Content-Type: application/json

{
  "shop_name": "New Shop Name",
  "shop_description": "Updated description"
}

Response: 200 OK
```

#### Vendor Dashboard
```http
GET /vendor/dashboard/
Authorization: Bearer {{vendor_access_token}}

Response: 200 OK
{
  "vendor_id": 2,
  "vendor_email": "vendor@example.com",
  "shop_name": "Test Shop",
  "total_products": 5,
  "total_brands": 3,
  "active": true
}
```

---

### 👥 ADMIN ENDPOINTS (Admin Auth Required)

#### Create Vendor
```http
POST /auth/admin/create-vendor/
Authorization: Bearer {{admin_access_token}}
Content-Type: application/json

{
  "email": "newvendor@example.com",
  "first_name": "Vendor",
  "last_name": "Name",
  "password": "VendorPass123!@",
  "shop_name": "New Shop",
  "shop_description": "Shop Description"
}

Response: 201 Created
```

#### List All Users
```http
GET /auth/admin/users/
Authorization: Bearer {{admin_access_token}}

Response: 200 OK
{
  "count": 50,
  "users": [ ... ]
}
```

#### Get User Details
```http
GET /auth/admin/users/{user_id}/
Authorization: Bearer {{admin_access_token}}
```

#### Delete User
```http
DELETE /auth/admin/users/{user_id}/
Authorization: Bearer {{admin_access_token}}

Response: 200 OK
```

#### List All Vendors
```http
GET /auth/admin/vendors/
Authorization: Bearer {{admin_access_token}}

Response: 200 OK
{
  "count": 10,
  "vendors": [ ... ]
}
```

#### Dashboard Statistics
```http
GET /auth/admin/stats/
Authorization: Bearer {{admin_access_token}}

Response: 200 OK
{
  "total_users": 150,
  "total_admins": 2,
  "total_vendors": 15,
  "total_customers": 133,
  "users_by_role": {
    "admin": 2,
    "vendor": 15,
    "customer": 133
  }
}
```

#### List All Products (Admin View)
```http
GET /admin/products/
Authorization: Bearer {{admin_access_token}}

Response: 200 OK
```

#### Create Product for Vendor (Admin)
```http
POST /products/
Authorization: Bearer {{admin_access_token}}
Content-Type: application/json

{
  "name": "Product Name",
  "details": "Description",
  "price": 5000,
  "Availability": "In Stock",
  "Condition": "New",
  "category_id": 1,
  "brand_id": 1,
  "vendor_id": 2
}

Response: 201 Created
```

#### Update Any Product (Admin)
```http
PATCH /products/{product_id}/
Authorization: Bearer {{admin_access_token}}
Content-Type: application/json

{
  "price": 4999
}

Response: 200 OK
```

#### Delete Any Product (Admin)
```http
DELETE /products/{product_id}/
Authorization: Bearer {{admin_access_token}}

Response: 204 No Content
```

---

## Authorization & Roles

### Role Permissions Matrix

| Action | Customer | Vendor | Admin |
|--------|----------|--------|-------|
| View Products | ✅ | ✅ | ✅ |
| Create Product | ❌ | ✅ Own | ✅ Any |
| Update Product | ❌ | ✅ Own | ✅ Any |
| Delete Product | ❌ | ✅ Own | ✅ Any |
| View Own Products | ❌ | ✅ | ✅ |
| View All Products | ❌ | ❌ | ✅ |
| Manage Users | ❌ | ❌ | ✅ |
| Create Vendor | ❌ | ❌ | ✅ |
| View Dashboard | ❌ | ✅ Vendor | ✅ Admin |
| Update Shop Details | ❌ | ✅ | ❌ |

### Permission Classes Used
```python
# Role-based permissions
IsAdminUserRole       # Admin only
IsVendorUserRole      # Vendor only
IsCustomerUserRole    # Customer only
IsAdminOrVendor       # Admin or Vendor

# Object-level permissions
IsVendorProductOwner  # Vendor owns product or Admin
IsOwnerOrAdmin        # Owner or Admin
```

---

## Testing Scenarios

### Scenario 1: Customer Registration & Shopping
1. **Register Customer** → Get tokens
2. **Login** → Get fresh tokens
3. **List Products** → Browse public products
4. **Update Profile** → Change name/phone
5. **Logout** → Invalidate tokens

### Scenario 2: Vendor Product Management
1. **Create Vendor** (As Admin) → Get vendor credentials
2. **Login as Vendor** → Get vendor tokens
3. **Create Product** → Add to inventory
4. **List Own Products** → View inventory
5. **Update Product** → Change price/details
6. **Vendor Dashboard** → View stats
7. **Update Branding** → Change shop details

### Scenario 3: Admin Management
1. **Login as Admin** → Get admin tokens
2. **Create Vendor** → Add new vendor
3. **List All Users** → View all customers/vendors
4. **Dashboard Stats** → View platform statistics
5. **Manage Products** → View/modify any product

### Scenario 4: Authorization Tests
1. **Customer Access Vendor Endpoint** → Should get 403 Forbidden
2. **No Token** → Should get 401 Unauthorized
3. **Invalid Token** → Should get 401 Unauthorized
4. **Vendor Delete Other's Product** → Should get 403 Forbidden

---

## Postman Collection Usage

### Running Pre-Built Flow

1. **Authentication Flow:**
   - Run "Login as Admin" (saves admin_access_token)
   - Run "Login as Vendor" (saves vendor_access_token)
   - Run "Register Customer" (saves customer_access_token)

2. **Product Workflow:**
   - Run "Create Product" (saves product_id)
   - Run "Update Own Product"
   - Run "List Vendor Products"

3. **Admin Tasks:**
   - Run "Create Vendor" (saves test_vendor_id)
   - Run "List All Users"
   - Run "Dashboard Stats"

### Using Test Scripts
Each request includes JS test scripts that:
- Verify response status codes
- Save tokens to environment automatically
- Extract entity IDs for subsequent requests

### Troubleshooting

**Token Expired:** Run login request again to refresh

**404 Not Found:** Update {{product_id}} or {{vendor_id}} with actual values

**403 Forbidden:** Check you're using correct role token (admin vs vendor)

**401 Unauthorized:** Run authentication flow to get fresh tokens

---

## Token Details

### Access Token
- **Lifetime:** 15 minutes
- **Contains:** user_id, email, role
- **Used for:** API requests
- **Header:** `Authorization: Bearer <access_token>`

### Refresh Token
- **Lifetime:** 7 days
- **Used for:** Getting new access tokens
- **Endpoint:** `POST /auth/token/refresh/`

### Token Refresh After Expiry
```bash
curl -X POST http://localhost:8001/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "{{refresh_token}}"}'
```

---

## Error Response Examples

### 401 Unauthorized (Invalid/Missing Token)
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden (Insufficient Permissions)
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 400 Bad Request (Invalid Data)
```json
{
  "email": ["User with this email already exists."],
  "password": ["This password is too weak."]
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

---

## Quick Testing Checklist

- [ ] Customer can register
- [ ] User can login
- [ ] Tokens are saved to environment
- [ ] Public products accessible without token
- [ ] Vendor can create product
- [ ] Vendor sees only own products
- [ ] Vendor cannot edit other's product
- [ ] Admin can see all products
- [ ] Admin can create vendor
- [ ] Customer cannot access vendor/admin endpoints
- [ ] Tokens refresh successfully
- [ ] Logout invalidates tokens

---

## Support & Issues

For API issues or questions:
1. Check token expiry (refresh if needed)
2. Verify correct role is being used
3. Check request body format (JSON)
4. Verify Authorization header format: `Bearer <token>`
5. Review error messages for validation errors

---

Generated: May 18, 2026
Version: 2.0.0 - Complete with Role-Based Authorization
