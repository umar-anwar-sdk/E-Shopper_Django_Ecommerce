# Refactor Summary

## What changed
- Refactored DRF permission logic by extracting role checks into helper functions.
- Added Role-based permission decorators for Django template views.
- Secured cart and order APIs with authentication and authorization checks.
- Added admin vendor approval workflow and custom dashboard templates.
- Added category and brand CRUD APIs with admin-only write access.
- Centralized form validation and improved serializer quality.
- Created reusable session-based cart helper in `cart/cart.py`.
- Added API tests for authentication, permissions, product creation, and cart security.
- Generated a Postman collection for quick API validation.

## Key improvements
- Cleaned up duplicate serializer definitions in `home/serializers.py`.
- Replaced unsafe product creation with role-aware permission checks.
- Added admin and vendor dashboards using Tailwind-based templates.
- Prevented unapproved vendors from logging in or using protected resources.
- Added new model migration to fix product foreign key defaults.
- Ensured backward compatibility where possible while cleaning legacy API endpoints.

## Files added
- `authentication/constants.py`
- `authentication/decorators.py`
- `templates/dashboard/base.html`
- `templates/dashboard/admin/dashboard.html`
- `templates/dashboard/admin/vendor_approval.html`
- `templates/dashboard/vendor/dashboard.html`
- `POSTMAN_COLLECTION.json`
- `SETUP_INSTRUCTIONS.md`
- `REFACTOR_SUMMARY.md`

## Testing
- Ran `./venv/bin/python manage.py test --keepdb` successfully.
- Created migration file `home/migrations/0008_alter_product_category_alter_product_brand_and_more.py`.
