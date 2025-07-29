# Flask REST API Example

## Database & Migration Setup

This project uses SQLAlchemy for MySQL database migrations.

### Configure MySQL Connection

Edit your `.env` file and update with your MySQL credentials:

```
DB_USER=root
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=tonjoo_transaction
SQLALCHEMY_DATABASE_URI=mysql://root:password@localhost:3306/tonjoo_transaction
```

### SQLAlchemy Models

See `api/models/` for model definitions:

- `TransactionHeader`
- `TransactionDetail`
- `MsCategory`

### Database Migration with Flask-Migrate

This project uses Flask-Migrate for database migrations.

#### Setup

1. Initialize migration folder:

   ```bash
   flask db init
   ```

2. Generate migration:

   ```bash
   flask db migrate -m "Initial migration"
   ```

3. Apply migration:
   ```bash
   flask db upgrade
   ```

## Folder Structure

```
rest-api-py/
├── app.py
├── requirements.txt
├── api/
│   ├── __init__.py
│   ├── models/
│   └── ...
├── migrations/
├── seeders/
│   ├── category_seeder.py
│   ├── transaction_seeder.py
│   └── transaction_detail_seeder.py
```

## Setup & Run

1. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
2. Run the migration (create tables):
   ```bash
   flask db upgrade
   ```
3. (Optional) Seed the database using Flask-Seeder:
   ```bash
   flask seed run
   ```
4. Run the app:
   ```bash
   python3 app.py
   ```

The API will be available at `http://localhost:5050/api/`.
