# Setup Instructions

1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Install dependencies if needed:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:
   ```bash
   ./venv/bin/python manage.py migrate
   ```

4. Create a superuser for admin access:
   ```bash
   ./venv/bin/python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   ./venv/bin/python manage.py runserver
   ```

6. Access the site:
   - Store: `http://localhost:8000/`
   - Django admin: `http://localhost:8000/admin/`
   - Custom admin dashboard: `http://localhost:8000/dashboard/admin/`
   - Vendor dashboard: `http://localhost:8000/dashboard/vendor/`

7. Run automated tests:
   ```bash
   ./venv/bin/python manage.py test
   ```

8. Postman collection:
   - Use `POSTMAN_COLLECTION.json` for API exploration.
   - Set `base_url` to `http://localhost:8000`.
   - Fill `access_token` and `refresh_token` after login.
